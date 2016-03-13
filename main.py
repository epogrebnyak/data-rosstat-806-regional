"""Retrieve data from many Excel files in folder and write standardized sheets to two output Excel files."""

import os 
import pandas as pd
from definitions import definitions 
from getter import get_dataframe_by_definition as get_df
from config import ROOT_DATA_FOLDER, OUTPUT_XLS_1 


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
        # HELP NEEDED 2: if uncommented, this (1) affects formatting of following sheet     
        #                                   (2) causes 'out of memory' warnings when opening file  
        # get_varname_df().to_excel(writer, sheet_name='varnames')        
        for df in df_list:
            sn = df['varname'][0]
            df.to_excel(writer, sheet_name=sn)
        
# repackaging - definitions must have 'sheet' specified
definitions = [d for d in definitions if d['sheet'] is not None]

# alter folder in defintions  
for i, d in enumerate(definitions):
    definitions[i]['folder'] = os.path.join(ROOT_DATA_FOLDER, d['folder'])

# main import 
dfs = [get_df(d) for d in definitions]
       
#save all dataframes to xl
write_to_xl(dfs, file = OUTPUT_XLS_1)

# TODO:
# make Russia file (1 sheet)
# make fed districts file (num_var sheets)
# make regions file (num_var sheets)

# HELP NEEDED 1:
# format all sheets *rosstat_806_regional.xls* as *formatting_rosstat_806_regional.xls*:
# - 1st column date format
# - 1st row font, alignment and word warpping
# - width of columns