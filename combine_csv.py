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
check = 0
for file_ in allFiles:
    df = pd.read_csv(file_, index_col=None, header=0)
    if check==0:
        column = df.columns
    csvs.append(df)
frame = pd.concat(csvs, ignore_index=True)
frame = frame.ix[:, column]
frame.to_csv("") #Save to your preferred format, and directory.
