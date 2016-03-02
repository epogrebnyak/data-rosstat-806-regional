source_def_sample = {   'varname':'PPI_PROM_ytd', 
     'folder':'xl_sample', 
   'filename':'industrial_prices.xls',
      'sheet':'пром.товаров',
     'anchor':'B5', 'anchor_value': 96.6}
     
# 1. Excel sheet reader: read_sheet(xl_filename, xl_sheet) will yield tuple (value, region, date)
# - in (value, region, date):
#  -- 'value' is self-explanatory
#  -- 'region' must be in *testable_region_names*
#  -- 'date' is first day of month 

# Sheet properties:
# - data values start at B4 of B5 - can be autodetected
# - starting date can be assumed alwauys to be is Jan 2009
# - region names are dirty - contain some variations of original name. need filter function for substitution


from datetime import date
import pandas as pd
from sidebar import actual_sidebar_list, testable_region_names

def yearmon(year, month):
     return date(year, month, 1) 

def filter_raw_sidenames(sidename):
     """Obtain valid row name from raw string. 
        Valid rows names are *sidebar.testable_region_names*"""
     pass
  
for a,v in zip(actual_sidebar_list, testable_region_names):
   pass
   # must pass assert below:
   #assert v == filter_raw_sidenames(a)       

def read_sheet(xl_filename, xl_sheet):
     """Read data from Excel sheet and yield it as a stream of datapoints"""
     # sample values
     yield (96.6,  "Российская Федерация", yearmon(2009, 1))
     yield (101.5, "Российская Федерация", yearmon(2009, 2))
     yield (104.4, "Российская Федерация", yearmon(2009, 3))
     yield (107.0, "Российская Федерация", yearmon(2009, 4))
     yield (118,   "Чукотский авт.округ",  yearmon(2015, 12))
     
gen = read_sheet(xl_filename=source_def_sample['filename'], xl_sheet=source_def_sample['sheet'])
assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))

# --- end of Excel reader

# 2. One Dataframe form Excel sheet: get_dataframe(xl_filename, xl_sheet)

def get_dataframe(xl_filename, xl_sheet):
     """Return dataframe corresponding to Excel sheet""" 
     list_of_dicts = [{'val':val, 'region':reg, 'dates':dt} for val, reg, dt in read_sheet(xl_filename, xl_sheet)]
     df = pd.DataFrame(list_of_dicts)
     # note: may also need to change index class to DateIndex as in 
     # pd.DatetimeIndex(df.dates, freq = "M")
     return df.pivot(columns='region', values='val', index='dates') 

df = get_dataframe(xl_filename=source_def_sample['filename'], xl_sheet=source_def_sample['sheet'])
     
# Tests - tests for dataframe check the following:
# - class of output is dataframe
assert isinstance(df, pd.DataFrame)

# - dataframe column list 
# todo: df.columns must have same content as testable_region_names
# assert

for col in df.columns:
   assert col in  testable_region_names

# - dataframe index
# index starts with Jan 2009
assert df.index[0].year == 2009
assert df.index[0].month == 1

# todo: other checks for index

# - selected values in dataframe:
assert df['Российская Федерация']['2009-01-01'] == 96.6

# check bottom-right 
assert df['Чукотский авт.округ']['2015-12-01'] == 118

# - something else to be tested ?



# BELOW IS NOT TODO:

# 3. Three dataframes from Excel sheet:
#    - Russian Federation (rf)
#    - federal district (okr)  
#    - regions (without) (reg)
# See sidebar.py for district names. Must add district composition 

# tests to pass:
# 3.1 for summable values summ by regions equals Russian Federation total 
# 3.2 for summable values summ by districts equals Russian Federation total 
# 3.3 with summation matrix for summable values summ by region in district equals district total 


def get_regions_dataframe(source_def):
    """Return pandas DataFrame containing variable from *source_def* by REGION"""
    pass
    
def get_okrug_dataframe(source_def):
    """Return pandas DataFrame containing variable from *source_def* by FEDERAL DISTRICT (okrug)"""
    pass

def get_rf_dataframe(source_def):
    """Return pandas DataFrame containing variable from *source_def* by RUSSIA TOTAL"""
    pass

reg = get_regions_dataframe(source_def_sample)
okr = get_okrug_dataframe(source_def_sample)
rf  = get_rf_dataframe(source_def_sample)
