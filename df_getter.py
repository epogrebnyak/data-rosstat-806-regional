"""Get dataframe from Excel file based on definition dictionary including folder, filename, sheet and anchor_cell."""

from datetime import date
import pandas as pd
import os

from regions import filter_region_name
from xls_read import read_sheet, read_by_definition, yearmon

from regions import reference_region_names, rf_name, district_names, summable_regions

def get_dataframe(datapoints_stream):
    """Return dataframe corresponding to datapoints stream."""        
    list_of_dicts = [{'val':x[0], 'region':x[1], 'dates':x[2]} for x in datapoints_stream]
    df = pd.DataFrame(list_of_dicts)
    # note: may also need to change index class to DateIndex 
    # pd.DatetimeIndex(df.dates, freq = "M")
    return df.pivot(columns='region', values='val', index='dates')[reference_region_names] 

def get_dataframe_by_definition(def_dict):
    """Return dataframe corresponding to definition dict."""   
    file_path = os.path.join(def_dict['folder'], def_dict['filename'])
    gen = read_sheet(file_path, def_dict['sheet'], def_dict['anchor']) 
    # may want to add variable name as a column
    return get_dataframe(gen)[reference_region_names]
    
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
    filename = def_dict['varname'] + ".xls"
    # do not overwrite datasource file itself
    if filename == def_dict['filename']:
       raise FileExistsError(filename)       
    else:
       df.transpose().to_excel(filename)
       
    
if __name__ == "__main__":

    def_dict_1 = {'varname':'PPI_PROM_ytd', 
     'folder':'xl_sample', 
   'filename':'industrial_prices.xls',
      'sheet':'пром.товаров',
     'anchor':'B5', 'anchor_value': 96.6}

    df = get_dataframe_by_definition(def_dict_1)
    to_excel(def_dict_1)
    
    # make definition for shipments.xls + tests below      
    def_dict_2 = {'varname':'SHIPMENTS', 
     'folder':'xl_sample', 
   'filename':'shipment.xls',
      'sheet':'Млн.рублей',
     'anchor':'B6', 'anchor_value': 5331853.711}     

    reg = get_regions_dataframe(def_dict_2)
    okr = get_okrug_dataframe(def_dict_2)
    rf  = get_rf_dataframe(def_dict_2)

# tests to pass:
# 3.1 for summable values summ by regions equals Russian Federation total 
    p = abs(reg.sum(axis = 1) - rf)
    #print(p[p > 0.1]) 
    
# 3.2 for summable values summ by districts equals Russian Federation total 
    z = abs(okr.sum(axis = 1) - rf)
    #print(z[z > 0.1])
    
# 3.3 with summation matrix for summable values summ by region in district equals district total
    # todo: need summation matrix by region
    
    from regions import region_by_district
    df = get_dataframe_by_definition(def_dict_2)
    for dist, regs in region_by_district.items():
        z = df[regs].fillna(0).sum(axis = 1) - df[dist]
        if sum(abs(z)) > 10:
           print(dist, sum(abs(z)))
           
    to_excel(def_dict_2)
       
       