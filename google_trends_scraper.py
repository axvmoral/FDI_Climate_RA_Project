r'''
This module implements a web scraper that I designed to scrape Google Trends
data on user inputted keywords for target countries stored in a user inputted
dataset containing country names over a user inputted time frame. The module
creates a timeseries of the average of interest in these keywords over each
country, and exports it as an xlsx file. It also plots this average for every
keyword.
'''

__author__ = 'Axel V. Morales Sanchez'


import seaborn as sb # for plotting
import matplotlib.pyplot as plt # to show plot
import pandas as pd # to manipulate/store data
import pytrends # to scrape Google Trends Data
from pytrends.request import TrendReq # to connect to Google Trends
import json # to load json data

fname = input('Enter CSV File Name of Countries \n> ')
column = input('Enter Column Name of Country Names \n>')

target_countries = pd.read_csv(fname)[column]
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

timeframe = input('Enter Time Frame \n>')

l = []
conn = TrendReq()
for country in iso2_codes:
  conn.build_payload(kw_list, cat=0, timeframe=timeframe, geo=country, gprop='')
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
