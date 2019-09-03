# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd
import numpy as np
import re

class PsleMakeDataFrame(object):
    def process_item(self, item, spider):
        try:
            df = pd.read_html(item['tables'][0], header=0)[0]
            df = self._delete_asterisk(df)
            df = self._make_pretty(df)
            item['tables'] = [df.to_dict()]
        except Exception as e:
            print(e)
            item['is_error'] = True
            return item
        return item
    
    def _delete_asterisk(self, dataframe):
        """
        Discovered that some rows have specific asterisked cells. It took a while, but found some
        error handling around it.

        Args:
        dataframe: Use dataframe that was crawled

        Returns:
        The same dataframe without the asterisked cells
        """
        find_index = 0
        column = dataframe.loc[:, "SUBJECTS"]
        for cell in column:
            if "*" in cell:
                dataframe.drop(dataframe.index[find_index], inplace=True)
                find_index -= 1 #TODO: Use continue here?
            find_index += 1
        return dataframe
    
    def _make_pretty(self, data):
        """
        Transform the dataframe from NECTA HTML dataframes.
        Anonymize the data, use subjects as features, change to analysis-friendly values.
        Rename the save file every time to avoid overwriting previously saved data.
        
        Args:
        data: NECTA dataframe
        
        Returns:
        analysis-friendly dataframe
        """
        data["Kiswahili"], data["English"], data["Maarifa"], data["Hisabati"], data["Science"], data["Average_Grade"] = zip(*data["SUBJECTS"].str.split(",").tolist())
        del data["SUBJECTS"]
        del data["CANDIDATE NAME"]
        subjects = ["Kiswahili", "English", "Maarifa", "Hisabati", "Science", "Average_Grade"]
        for e in subjects:
            data[e] = data[e].map(lambda x: str(x)[-1])
        grade_value = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "X": np.nan}
        sex = {"F": 1, "M": 0}
        for i in subjects:
            data.replace({i: grade_value}, inplace=True)
        data.replace({"SEX": sex}, inplace=True)
        data['Calculated_Average'] = (data.Kiswahili + data.English + data.Maarifa + data.Hisabati + data.Science)/5
        return data

class PsleJsonWriter(object):

    def open_spider(self, spider):
        self.file = open(spider.custom_settings['FEED_URI'][7:], 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item['url'], item['region'], item['district'] #this is what the console prints out

class AcseeMakeDataFrame(object):

    def process_item(self, item, spider):
        item['errors'] = []
        item['rankings_table'] = None
        item['div_performance_table'] = None
        item['subject_performance_table'] = None

        try:
            alevel = pd.read_html(item['html'], header=0, flavor='bs4')[0]
            #Listify the list of subject grades, grades for each row in Detailed Subjects column
            alevel.loc[:,"DETAILED SUBJECTS"] = alevel.loc[:,"DETAILED SUBJECTS"].apply(lambda x: self._list_subjects(x))
            #Split the grades and make columns for them
            alevel = self._make_subject_columns(alevel)
            #Tidy up grade data
            alevel = self._clean_grades(alevel)
            alevel.insert(0, 'exam_center', item['exam_center'])

            item['result_table'] = alevel.to_dict()
        except Exception as e:
            item['errors'].append(('result_table', str(e)))
            item['is_error'] = True
        
        if item['exam_center'].lower()[0] != 'p': #Private exam centers don't have the meta-data tables.
            #Rankings Table
            try:
                rankings_table = pd.read_html(item['html'], header=0, flavor='bs4')[2] #TODO: bug - pandas 0.24.2 throws IndexError without a non-Falsey header arg, 0.23.4 did not
                first_row = [rankings_table.copy().columns.tolist()] #save the original first row
                rankings_table.columns = ['category', 'rank'] #create new column names
                new_rankings_table = pd.DataFrame(first_row, columns=rankings_table.columns).append(rankings_table) #Make a complete df
                new_rankings_table.reset_index(drop=True, inplace=True) #Have to reset index so to_dict works properly
                new_rankings_table.insert(0, 'exam_center', item['exam_center'])
                item['rankings_table'] = new_rankings_table.to_dict()
            except Exception as e:
                item['errors'].append(('rankings_table', str(e)))
                item['is_error'] = True

            #Division Performance Table
            try:
                dev_perform_table = pd.read_html(item['html'], flavor='bs4', header=0)[4]
                dev_perform_table.insert(0, 'exam_center', item['exam_center'])
                item['div_performance_table'] = dev_perform_table.to_dict()
            except Exception as e:
                item['errors'].append(('div_performance_table', str(e)))
                item['is_error'] = True

            #Subject Performance Table
            try:
                subj_perform_table = pd.read_html(item['html'], flavor='bs4', header=0)[6]
                subj_perform_table.insert(0, 'exam_center', item['exam_center'])
                item['subject_performance_table'] = subj_perform_table.to_dict()
            except Exception as e:
                item['errors'].append(('subject_performance_table', str(e)))
                item['is_error'] = True

        if not item['is_error']: #If there was no error in pipeline, reduce file size and empty html
            item['html'] = None
        
        #COMMENT OUT -- use for when you are testing an issue that isn't the html, ruins output
        #item['html'] = None

        return item
        
    def _list_subjects(self, cell):
        subject_list = [subject.replace("'", '') for subject in re.split("'\s", cell)]
        return subject_list

    def _pull_subject(self, subj):
        return re.search(r'(^[A-Za-z\/]*)', subj).group()

    def _make_subject_columns(self, df):
        #Slightly inspired by this: https://stackoverflow.com/questions/44663903/pandas-split-column-of-lists-of-unequal-length-into-multiple-columns
        for row in df.itertuples():
            for subject in row[5]:
                df.loc[row[0], self._pull_subject(subject)] = subject
        return df

    def _clean_grades(self, df):
        df.iloc[:, 5:] = df.iloc[:, 5:].fillna("!") #TODO: is there another better marker for N/A? document this
        df.iloc[:, 5:] = df.iloc[:, 5:].applymap(lambda x: x[-1])
        del df["DETAILED SUBJECTS"]
        return df

class AcseeJsonWriter(object):

    def open_spider(self, spider):
        self.file = open(spider.custom_settings['FEED_URI'][7:], 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item['exam_center'], item['url'] #what console spits out
