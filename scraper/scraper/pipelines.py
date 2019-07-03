# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd
import numpy as np

class MakeDataFrame(object):
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

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open(spider.custom_settings['FEED_URI'][7:], 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item['url'], item['region'], item['district']
