# User Input:
# Either topic or individual word
# (Topic) Words to pull data from
# Compile data into one data set (time series)
# Export as CSV to working directory

import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import pytrends
from pytrends.request import TrendReq
import json

fname = input('Enter CSV File Name of Countries \n> ')

target_countries = pd.read_csv(fname)['country']
json_crosswalk = json.load(open('data/countries_en.json'))
iso2_codes = []
for country in target_countries:
   iso2_codes.append(json_crosswalk[country])

kw_list = []
while True:
    kw = input("Keyword:        (Enter '0' to proceed) \n> ")
    if kw == str(0):
        break
    else:
        kw_list.append(kw)

l = []
conn = TrendReq()
for country in iso2_codes:
  conn.build_payload(kw_list, cat=0, timeframe='today 5-y', geo=country, gprop='')
  df = conn.interest_over_time()
  df['iso2'] = country
  l.append(df.reset_index())
interest_data = pd.concat(l).groupby(['date']).mean(numeric_only=True)
del interest_data['isPartial']
interest_data.to_excel(r'\data\google_trends_output.xlsx')

sb.set_theme(style="darkgrid")
ax = sb.lineplot(data=interest_data)

legend = ax.legend()

for i in range(len(kw_list)):
    ax.lines[i].set_linestyle("-")
    legend.get_lines()[i].set_linestyle("-")

plt.show()
