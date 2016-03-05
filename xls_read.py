# Excel sheet reader: read_sheet(xl_filename, xl_sheet) will yield tuple (value, region, date)
# - in (value, region, date):
#  -- 'value' is self-explanatory
#  -- 'region' must be in *reference_region_names*
#  -- 'date' is first day of month 

# Sheet properties:
# - data values start at B4 of B5 - can be autodetected
# - starting date can be assumed alwauys to be is Jan 2009
# - region names are dirty - contain some variations of original name. need filter function for substitution

# Test: 
#    - search function for anchor     

import os
from datetime import date
import xlrd
import numpy as np

from xlsxwriter.utility import xl_rowcol_to_cell # (1, 2) -> 'C2'
from xlsxwriter.utility import xl_cell_to_rowcol # 'C2' -> (1, 2)

from regions import filter_region_name

def yearmon(year, month):
    return date(year, month, 1)
     
def filter_cellvalue(x):
    if isinstance(x, float) or isinstance(x, int):
        return x
    else:
        return np.nan 
     
def read_sheet(xl_filename, xl_sheet, anchor=None):
    """Read data from Excel sheet and yield it as a stream of datapoints"""
    
    wb = xlrd.open_workbook(xl_filename)
    cur_sheet = wb.sheet_by_name(xl_sheet)
    
    if not anchor:  
       # todo: must have some code for searching upper-left corner of data region on sheet     
       anchor = "B5"
    
    # starting position
    r0,c0 = xl_cell_to_rowcol(anchor)
    
    # two rows up from r0,c0
    start_year = int(cur_sheet.cell(r0-2,c0).value.split()[0])
    assert start_year == 2009
    
    #extraction first column data
    raw_regions = cur_sheet.col_values(0, start_rowx=r0, end_rowx=None)
    regions = filter(None, [filter_region_name(r) for r in raw_regions])
    
    #extracting data left-right, up-down
    for r, region in enumerate(regions,start=r0):
        for m, c in enumerate(range(c0,cur_sheet.ncols)):
            year, month = start_year + m//12, m%12 + 1
            #cur_sheet.cell(r,c).value may be float or str 
            val = filter_cellvalue(cur_sheet.cell(r,c).value)
            yield (val,region,yearmon(year, month)) 
            
def read_by_definition(def_dict):
    file_path = os.path.join(def_dict['folder'], def_dict['filename'])
    return read_sheet(file_path, def_dict['sheet'], def_dict['anchor'])
    
if __name__=="__main__":
    source_def_sample = {
        'varname':'PPI_PROM_ytd', 
        'folder':'xl_sample', 
        'filename':'industrial_prices.xls',
        'sheet':'пром.товаров',
        'anchor':'B5', 'anchor_value': 96.6}
    
    gen = read_by_definition(source_def_sample) 
    assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))
    for i in range(1000):
        print(next(gen))
