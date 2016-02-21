source_def_sample = {   'varname':'PPI_PROM_ytd', 
     'folder':'xl_sample', 
   'filename':'industrial_prices.xls',
      'sheet':'пром.товаров',
     'anchor':'B5', 'anchor_value': 96.6}
     
# region names
import sidebar

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
okr = get_okrug__dataframe(source_def_sample)
rf  = get_rf_dataframe(source_def_sample)

#TODO 1:
#write asserts for reg, okr and rf that check import was properly done

# tests check the following:
# - class of output is dataframe  
# - dataframe column list 
# - dataframe index
# - selected values in dataframe
#   -- anchor value is found 
#   -- several other values are referenced by region and date the value equals to test value  
# - something else?
