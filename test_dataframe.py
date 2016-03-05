source_def_sample = {'varname':'PPI_PROM_ytd', 
     'folder':'xl_sample', 
   'filename':'industrial_prices.xls',
      'sheet':'пром.товаров',
     'anchor':'B5', 'anchor_value': 96.6} 
     
import pandas as pd

from df_getter import get_dataframe_by_definition
from regions import reference_region_names
   
df = get_dataframe_by_definition(source_def_sample)
   
# Tests - tests for dataframe check the following:
# - class of output is dataframe
def test_class():
    assert isinstance(df, pd.DataFrame)

# Dataframe column list 
# todo: df.columns must have same content as testable_region_names

def test_columns():
    for col in df.columns:
       assert col in  reference_region_names

# Dataframe index
# index starts with Jan 2009
def test_start_index():
    assert df.index[0].year == 2009
    assert df.index[0].month == 1

# Selected values in dataframe:
def test_values():
    assert df['Российская Федерация']['2009-01-01'] == 96.6
    # check bottom-right 
    assert df['Чукотский авт. округ']['2015-12-01'] == 118