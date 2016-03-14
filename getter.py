from datetime import date
import pandas as pd
import os

from xls_read import read_sheet, read_by_definition, yearmon
from regions import Regions

filter_region_name = Regions.filter_region_name
reference_region_names = Regions.names()
rf_name = Regions.rf_name()
district_names = Regions.district_names()
summable_regions = Regions.summable_regions()

def get_dataframe(datapoints_stream):
    """Return dataframe corresponding to datapoints stream."""        
    list_of_dicts = [{'val':x[0], 'region':x[1], 'dates':x[2]} for x in datapoints_stream]
    df = pd.DataFrame(list_of_dicts)
    df = df.pivot(columns='region', values='val', index='dates')[reference_region_names]
    df.index = pd.DatetimeIndex(df.index)
    return df

def get_dataframe_by_definition(def_dict):
    """Return dataframe corresponding to definition dict."""   
    file_path = os.path.join(def_dict['folder'], def_dict['filename'])
    if 'anchor' in def_dict.keys():
        gen = read_sheet(file_path, def_dict['sheet'], def_dict['anchor']) 
    else:
        gen = read_sheet(file_path, def_dict['sheet'])
    try:
       df = get_dataframe(gen)[Regions.names()]
    except:
       raise ValueError(file_path)    
    df.insert(0, 'varname', def_dict['varname'])
    return df 
    
def get_regions_dataframe(def_dict):
    """Return pandas DataFrame containing variable from *def_dict* by REGION"""
    return get_dataframe_by_definition(def_dict)[summable_regions]
    
def get_okrug_dataframe(def_dict):
    """Return pandas DataFrame containing variable from *def_dict* by FEDERAL DISTRICT (okrug)"""
    return get_dataframe_by_definition(def_dict)[district_names]
    
def get_rf_dataframe(def_dict):
    """Return pandas DataFrame containing variable from *def_dict* by RUSSIA TOTAL"""
    return get_dataframe_by_definition(def_dict)[rf_name]

def to_excel(def_dict):
    df = get_dataframe_by_definition(def_dict)
    # check must not overwrite
    filename = def_dict['varname'] + ".xls"
    df.transpose().to_excel(filename)
    
if __name__ == "__main__":

    from config import XL_SAMPLE_FOLDER

    def_dict_1 = {'varname':'PPI_PROM_ytd', 
     'folder': XL_SAMPLE_FOLDER, 
   'filename':'industrial_prices.xls',
      'sheet':'пром.товаров',
     'anchor':'B5', 'anchor_value': 96.6}

    df = get_dataframe_by_definition(def_dict_1)
    to_excel(def_dict_1)
    
    # make definition for shipments.xls + tests below      
    def_dict_2 = {'varname':'SHIPMENTS', 
     'folder': XL_SAMPLE_FOLDER, 
   'filename':'shipment.xls',
      'sheet':'Млн.рублей',
     'anchor':'B6', 'anchor_value': 5331853.711}     

    reg = get_regions_dataframe(def_dict_2)
    okr = get_okrug_dataframe(def_dict_2)
    rf  = get_rf_dataframe(def_dict_2)

    # + test_anchor()    
    
# tests to pass:
# 3.1 for summable values summ by regions equals Russian Federation total 
    p = abs(reg.sum(axis = 1) - rf)
    # QUESTION:
    print("\nSummable regions do not match Russia total: OK, Crimea reporting effect for these dates")
    print(p[p > 0.1]) 
    
# 3.2 for summable values summ by districts equals Russian Federation total 
    print("\nRussia total does not match for several dates: OK, Crimea reporting effect for these dates")
    z = abs(okr.sum(axis = 1) - rf)
    print(z[z > 0.1])
    
# 3.3 with summation matrix for summable values summ by region in district equals district total
    print("\nSumm by districts - seems to match")
    # todo: concat diff by distrist into one dataframe *diffs* 
    from regions import Regions
    for r in Regions.district_names():
        cols = Regions.region_by_district(r)
        diff = round(reg[cols].sum(axis = 1) - okr[r], 1)
        print ('\n', r)
        # partial indexing
        print (diff["2015-12-01"])
    
    # todo: need summation matrix by region
