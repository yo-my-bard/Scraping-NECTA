"""
Upon crawling the NECTA website, specific tables of interest need to be fetched for each URL.
This module has functions that take URLs with HTML tables, combines them, and return data
that is in a usable format for analyses (i.e. not letter grades). For other nice features,
see adding_regions module and future modules! Or submit a pull request!

"""

import pandas as pd
import numpy as np
import time
from sqlstore import storeinDB


def getframe(list):
    """
    Get the dataframe from a pandas.read_html list return.

    :param list:
    :return: pandas dataframe

    """
    for e in list:
        return e

def merge_all(table_urls):
    """
    Merge all NECTA HTML tables into a single pandas dataframe.
    Warning: this is a long process. Still in the process of finding ways to make this function faster.
    Hold-up is due mostly to having to respect the NECTA server.

    :param table_urls: list of all NECTA URLs to get tables from
    :return: single pandas dataframe of all tables

    """
    combo = []
    index = 0
    indexlist = []
    for i in table_urls:
        try:
            time.sleep(3)
            table = pd.read_html(i, header=0)
            a = getframe(table)
            column = a.loc[:, "SUBJECTS"]
            for cell in column:
                #Discovered that some rows have specific asterisked cells. It took a while, but found some
                #error handling around it. Without this, the merge fails and it won't tell you until hours later.
                if "*" in cell:
                    raise ValueError("This is an incomplete table, asterisk in grade values")
            combo.append(a)
            index += 1
            time.sleep(2)
        except Exception as e:
            print((index, e))
            indexlist.append([index, i])
            index += 1
            time.sleep(60)
            continue
    combo_df = pd.concat(combo, ignore_index=True)
    print([indexlist])
    storeinDB(indexlist) #The expectation is some URLs will fail, use the provided SQL retrieval module to
#                         to retrieve them again later. This function stores them for future use.
    return combo_df

def make_pretty(data):
    """
    Transform the dataframe from NECTA HTML dataframes.
    Anonymize the data, use subjects as features, change to analysis-friendly values.
    Rename the save file every time to avoid overwriting previously saved data.
    :param data: NECTA dataframe
    :return: analysis-friendly file
    """
    data["Kiswahili"], data["English"], data["Maarifa"], data["Hisabati"], data["Science"], data["Average Grade"] = zip(*data["SUBJECTS"].str.split(",").tolist())
    del data["SUBJECTS"]
    del data["CANDIDATE NAME"]
    subjects = ["Kiswahili", "English", "Maarifa", "Hisabati", "Science", "Average Grade"]
    for e in subjects:
        data[e] = data[e].map(lambda x: str(x)[-1])
    grade_value = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "X": np.nan}
    sex = {"F": 1, "M": 0}
    for i in subjects:
        data.replace({i: grade_value}, inplace=True)
    data.replace({"SEX": sex}, inplace=True)
    data.to_csv() #Save data in your preferred format, to your preferred directory. Rename this file every time you call
    #              this function.
    return print("It's pretty now!")
