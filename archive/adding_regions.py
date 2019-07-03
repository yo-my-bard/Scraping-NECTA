"""

This module was built to maintain the regional associations for each student.
The usage of regular expression can actually produce associations at a more granular level
with districts. Theoretically, because the data used represents schools, the geographical
data can be more granular still (latitude/longitude coordinates). Look for future features on this
when I return to this project or submit a pull request!

"""

import pandas as pd
import numpy as np
import re


table = pd.DataFrame()
subjects = ["Kiswahili", "English", "Maarifa", "Hisabati", "Science"]
table = pd.read_csv() #Insert appropriate CSV directory, or read from your data source

#Make the column, set all its values to NaN

table['Region'] = np.nan

#An inelegant assignment of the regular expressions

regex = re.compile(r'^PS01')
regex2 = re.compile(r'^PS02')
regex3 = re.compile(r'^PS03')
regex4 = re.compile(r'^PS04')
regex5 = re.compile(r'^PS05')
regex6 = re.compile(r'^PS06')
regex7 = re.compile(r'^PS07')
regex8 = re.compile(r'^PS08')
regex9 = re.compile(r'^PS09')
regex10 = re.compile(r'^PS10')
regex11 = re.compile(r'^PS11')
regex12 = re.compile(r'^PS12')
regex13 = re.compile(r'^PS13')
regex14 = re.compile(r'^PS14')
regex15 = re.compile(r'^PS15')
regex16 = re.compile(r'^PS16')
regex17 = re.compile(r'^PS17')
regex18 = re.compile(r'^PS18')
regex19 = re.compile(r'^PS19')
regex20 = re.compile(r'^PS20')
regex21 = re.compile(r'^PS21')
regex24 = re.compile(r'^PS24')
regex25 = re.compile(r'^PS25')
regex26 = re.compile(r'^PS26')
regex27 = re.compile(r'^PS27')


region_abbr = {regex: 'ARU', regex2: 'DAR', regex3: 'DOD', regex4: 'IRI', regex5: 'KAG',
               regex6: 'KIG', regex7: 'KIL', regex8: 'LIN', regex9: 'MAR', regex10: 'MBE',
               regex11: 'MOR', regex12: 'MTW', regex13: 'MWA', regex14: 'PWA', regex15: 'RUK',
               regex16: 'RUV', regex17: 'SHI', regex18: 'SIN', regex19: 'TAB', regex20: 'TAN',
               regex21: 'MAN', regex24: 'GEI', regex25: 'KAT', regex26: 'NJO', regex27: 'SIM'}


#Change all NaN values in Region column to corresponding Region for the student

for key, value in region_abbr.items():
    table['Region'][table.loc[:, ('CAND. NO')].str.match(key)] = value

table.to_csv() #Save in your preferred format, to your preferred directory
