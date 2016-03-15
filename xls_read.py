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
from debug_config import ROOT_DATA_FOLDER, OUTPUT_XLS

from regions import Regions
filter_region_name = Regions.filter_region_name

def yearmon(year, month):
    return date(year, month, 1)
     
def filter_cellvalue(x):
    if isinstance(x, (float, int)):
        return x # Maybe is better to return float(x) ?
    else:
        return np.nan
    
def seek_origin(sheet,):
    TOKENS = ("январ","Iквартал")
    test_tokens = lambda cc: any((t in cc) for t in TOKENS)
    def gen_coords():
        for n in range(20):
            r,c = n,0
            while True:
               yield (r,c)
               if c==n:
                   break
               r-=1
               c+=1
    coords = gen_coords()
    while True:
        r,c = next(coords)
        current_cell = sheet.cell(r,c).value
        if isinstance(current_cell, str) and test_tokens(current_cell.replace(" ","")):
            return (r+1,c)
            
def read_sheet(xl_filename, xl_sheet, anchor=None):
    """Wrapper to read sheet and display filename on error."""
    try: 
        return  _read_sheet(xl_filename, xl_sheet, anchor)
    except:
        raise ValueError(xl_filename)    
    
def _read_sheet(xl_filename, xl_sheet, anchor=None):
    """Read data from Excel sheet and yield it as a stream of datapoints."""
    
    # determine a start position         
    wb = xlrd.open_workbook(xl_filename)
    cur_sheet = wb.sheet_by_name(xl_sheet)

    # starting position
    if not anchor:
        r0,c0 = seek_origin(cur_sheet)
    else:    
        r0,c0 = xl_cell_to_rowcol(anchor)
    
    # strat year is two rows up from r0,c0
    start_year = int(cur_sheet.cell(r0-2,c0).value.split()[0])
    try:
       assert start_year == 2009 or start_year == 2010
    except:
       raise ValueError(xl_filename)
       
    # ValueError: xls\info_stat_01_2016\01 промышленность\047-049 рыба живая, свежая или охлажденная.xls
    # starts with 2010
    
    #extraction first column data
    raw_regions = cur_sheet.col_values(0, start_rowx=r0, end_rowx=None)
    regions = filter(None, [filter_region_name(r) for r in raw_regions])
    
    #extracting data left-right, up-down
    for r, region in enumerate(regions,start=r0):
        for m, c in enumerate(range(c0,cur_sheet.ncols)):
            year, month = start_year + m//12, m%12 + 1
            #cur_sheet.cell(r,c).value may be float or str - must filter value
            val = filter_cellvalue(cur_sheet.cell(r,c).value)
            yield (val,region,yearmon(year, month)) 


def _read_sheet_q(xl_filename, xl_sheet, anchor=None):
    """Read data from Excel sheet and yield it as a stream of datapoints."""
    
    # determine a start position         
    wb = xlrd.open_workbook(xl_filename)
    cur_sheet = wb.sheet_by_name(xl_sheet)

    # starting position
    if not anchor:
        r0,c0 = seek_origin(cur_sheet)
    else:    
        r0,c0 = xl_cell_to_rowcol(anchor)
    
    # strat year is two rows up from r0,c0
    start_year = int(cur_sheet.cell(r0-2,c0).value.split()[0])
    try:
       assert start_year == 2009 or start_year == 2010
    except:
       raise ValueError(xl_filename)
    
    #extraction first column data
    raw_regions = cur_sheet.col_values(0, start_rowx=r0, end_rowx=None)
    regions = filter(None, [filter_region_name(r) for r in raw_regions])
    
    #extracting data left-right, up-down
    for r, region in enumerate(regions,start=r0):
        for m, c in enumerate(range(c0,cur_sheet.ncols)):
            year, quarter = start_year + m//4, m%4 + 1
            print("year, quarter ", year, quarter )
            #cur_sheet.cell(r,c).value may be float or str - must filter value
            val = filter_cellvalue(cur_sheet.cell(r,c).value)
            yield (val,region,yearmon(year, 1+3*(quarter-1)))
            yield (val,region,yearmon(year, 2+3*(quarter-1)))
            yield (val,region,yearmon(year, 3+3*(quarter-1)))

proxy_reader = {"default": read_sheet,
                "quarter": _read_sheet_q}
            
def read_by_definition(def_dict, use_anchor = False):
    file_path = os.path.join(ROOT_DATA_FOLDER, def_dict['folder'], def_dict['filename'])
    reader = proxy_reader[def_dict.get("reader", 'default')]
    if use_anchor:
        return reader(file_path, def_dict['sheet'], def_dict['anchor'])
    else:
        return reader(file_path, def_dict['sheet'])
    
if __name__=="__main__":
    source_def_sample = {
     'varname':'PROD_IND_YOY',
     'folder':'01 промышленность',
     'filename':'005-013 индекс промышленного производства.xls',
     'subtitle':'В % к соответствующему месяцу предыдущего года',
     'sheet':" к соотв. месяцу",
     'anchor_value': 81.7
    }
    
    gen = read_by_definition(source_def_sample) 
    #assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))
    for i in range(10):
        print(next(gen))
