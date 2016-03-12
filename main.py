"""Retrieve data from many Excel files in folder and write standardized sheets to two output Excel files."""

import os 
import pandas as pd
from definitions import definitions 
from getter import get_dataframe_by_definition as get_df
from config import ROOT_DATA_FOLDER, OUTPUT_XLS_1 

# repackaging - definitions must have 'sheet' specified
definitions = [d for d in definitions if d['sheet'] is not None]

# alter folder in defintions  
for i, d in enumerate(definitions):
    definitions[i]['folder'] = os.path.join(ROOT_DATA_FOLDER, d['folder'])

# main import 
dfs = [get_df(d) for d in definitions]

def write_to_xl(df_list, file):
    with pd.ExcelWriter(file) as writer:
        for df in df_list:
            df.to_excel(writer, sheet_name=df['varname'][0])
        # also need to write variable names    
        # self.df_vars().to_excel(writer, sheet_name='variables')
        
#save all dataframes to xl
write_to_xl(dfs, file = OUTPUT_XLS_1)