"""Retrieve data from many Excel files in folder and write standardized sheets to two output Excel files."""

import os 
import pandas as pd
from definitions import definitions 
from getter import get_dataframe_by_definition as get_df
from config import ROOT_DATA_FOLDER, OUTPUT_XLS
from regions import Regions
            
def clean_definitions(definitions):            
    # repackaging - definitions must have 'sheet' specified
    definitions = [d for d in definitions if d['sheet'] is not None]

    # alter folder in defintions  
    for i, d in enumerate(definitions):
        try:
            definitions[i]['folder'] = os.path.join(ROOT_DATA_FOLDER, d['folder'])
        except:
            raise ValueError(d)
    
    return definitions

def get_var_desc(def_dict):
    vn = def_dict['filename'].replace("-","").replace(".xls","").strip('0123456789').strip()
    return def_dict['varname'], vn, def_dict['subtitle'] 
   
def get_varname_df(defs = definitions):
    zf = pd.DataFrame(columns=('varname', 'file', 'unit'))
    for i, d in enumerate(defs):
        zf.loc[i] = get_var_desc(d)
    return zf        
    
def write_to_xl(df_list, file):
    with pd.ExcelWriter(file) as writer:
        # WARNING: if uncommented, this (1) affects formatting of following sheets (1st column not formatted as dates)     
        #                               (2) causes 'out of memory' warnings when opening file  
        # get_varname_df().to_excel(writer, sheet_name='varnames')        
        for df in df_list:
            try:
               sn = df['varname'][0]
            except:
               raise Exception(df) 
            df.to_excel(writer, sheet_name=sn)

def to_xl_sheet(df, tag, sheet):
    msg(tag)
    with pd.ExcelWriter(OUTPUT_XLS[tag]) as writer:
        df.to_excel(writer, sheet_name=sheet)            
            
def to_xl_book(df_list, tag):
    msg(tag)
    write_to_xl(df_list, file = OUTPUT_XLS[tag])
        
def msg(tag):
    print("Writing", OUTPUT_XLS[tag])         

def import_xl_data(defs = definitions):
    defs = clean_definitions(defs)
    dfs = [get_df(d) for d in defs]
    for df in dfs:
        df.to_csv(os.path.join('csv', df['varname'][0]) + ".csv", encoding = "utf-8") 
    return dfs         

def get_csv_file_list():
    return list(os.walk('csv'))[0][2]

def import_csv_data():
    return [pd.read_csv(os.path.join('csv', fn), index_col = 0) for fn in get_csv_file_list()] 

    
if __name__ == "__main__":
    
    jobs = '123456'
    
    # this import preserves series order 
    dfs = import_xl_data()
    
    # this import is faster, but series is alphabetic
    # dfs = import_csv_data()
    
    # output 1: save all dataframes to xls by sheet - one df per sheet    
    if '1' in jobs:
        to_xl_book(dfs, tag = 'by_sheet')    
    
    # output 2: concat all dataframes to one xls sheet
    if '2' in jobs:
        r = pd.concat(dfs)
        to_xl_sheet(r, tag = 'one_page', sheet = "regions")
    
    # output 3: make Russia file (1 sheet)    
    rf = Regions.rf_name()
    if '3' in jobs:               
        # note: must have pandas 17 or higher for 'rename'
        df_rf = pd.concat([d[rf].rename(d['varname'][0]) for d in dfs], axis = 1)
        to_xl_sheet(df_rf, tag = 'rf', sheet = 'rf')          
        
    # output 4: make fed districts file (num_var sheets)
    if '4' in jobs:
        cols = ['varname'] + [Regions.rf_name()] + Regions.district_names() 
        dfs2 = [d.reindex(columns=cols) for d in dfs]
        to_xl_book(dfs2, tag = 'districts')        
    
    # output 5: make regions only file (num_var sheets)  
    if '5' in jobs:    
        cols = ['varname'] + [Regions.rf_name()] + Regions.summable_regions()
        dfs3 = [d.reindex(columns=cols) for d in dfs] 
        to_xl_book(dfs3, tag = 'summable')        

    # output 6: write regions only file (num_var sheets)
    if '6' in jobs:
        to_xl_sheet(df = get_varname_df(), tag = 'varnames', sheet = 'varnames') 

