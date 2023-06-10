'''
Thus module exports a subset of mergedFDIClimateAnnual1956_112_processed_wdi.dta 
with log average disaster numbers for specified disaster types for each country
that is not considered an offshore account haven.
'''

__author__ = 'Axel V. Morales Sanchez'

import pandas as pd
import numpy as np
from functools import reduce


def conv_to_log(disaster: str):
  df = pd.read_stata('C:/Users/axvmo/Documents/UCSC/FDI Climate Project/Data/mergedFDIClimateAnnual1956_112_processed_wdi.dta',
                     columns=['country', 'ofc', 'year', disaster])
  df = df.loc[df['ofc'] == 0, ['country', disaster]
              ].groupby(by=['country']
                        ).agg('mean', numeric_only=True
                              ).reset_index()
  df.loc[df[disaster] != 0, disaster].apply(np.log)
  return df

if __name__ == '__main__':
  disaster_types = ['disaster_m', 'climatological_m',
                    'meteorological_m', 'hydrological_m']
  l = [conv_to_log(disaster) for disaster in disaster_types]
  df = reduce(lambda x, y: pd.merge(x, y, on='country'), l)
  df.to_excel('C:/Users/axvmo/Documents/UCSC/FDI Climate Project/Data/log_avg_disasters.xlsx')
