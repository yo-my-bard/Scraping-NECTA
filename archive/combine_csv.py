"""

Once you have cleaned up your data and have run the best_data module a couple of times, you will likely
have multiple CSV files because of the iterations you had to run. Use this module to combine into one iteration.
Disclaimer: have not tested this logic for other data formats.

"""
import glob
import pandas as pd


path = r'' #Use your path to the directory with all CSVs
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
csvs= []
for file_ in allFiles:
    df = pd.read_csv(file_)
    csvs.append(df)
frame = pd.concat(csvs)
frame.drop(["Unnamed: 0"], axis=1, inplace=True)
frame['CalcAverage'] = (frame.Kiswahili + frame.English + frame.Maarifa + frame.Hisabati + frame.Science)/5
frame.rename(columns={"Average Grade": "Average_Grade"}, inplace=True)
frame.to_csv("", index=False) #Save to your preferred format, and directory.
