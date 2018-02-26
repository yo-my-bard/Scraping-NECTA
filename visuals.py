"""

An example script of putting together visuals using the combined data file.

"""
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.style.use('ggplot')
plt.interactive(False)
table = pd.DataFrame()
subjects = ["Kiswahili", "English", "Maarifa", "Hisabati", "Science"]
table = pd.read_csv('/Users/Muse/Documents/GitHub/ImportingNECTA/CompleteDatasets/necta_psle_2014.csv') #Use the directory with your combined data file

plt.figure()

#hist = table[subjects].plot.hist(alpha = 0.5, bins=5, stacked=False)
#hist2 = table['CalcAverage'].plot.hist(alpha = 0.5, bins=10, stacked=False)
#hist3 = table['Average_Grade'].plot.hist(alpha = 0.5, bins=5, stacked=False)


#scatter = table.plot.scatter(x='Kiswahili', y='CalcAverage')
#scatter2 = table.plot.scatter(x='English', y='CalcAverage')
#scatter3 = table.plot.scatter(x='Science', y='CalcAverage')

plt.show()
