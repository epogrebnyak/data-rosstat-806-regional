import os
from datetime import date
import xlrd

# не нашел аналога в пандас, в xlrd есть только (1, 2) -> 'C2', также есть свой "велосипед"
from xlsxwriter.utility import xl_rowcol_to_cell # (1, 2) -> 'C2'
from xlsxwriter.utility import xl_cell_to_rowcol # 'C2' -> (1, 2)

from reference_region_names import reference_region_names
from filter_raw_sidenames import filter_raw_sidenames

def yearmon(year, month):
     return date(year, month, 1)

def read_sheet(xl_filename, xl_sheet, anchor):
    wb = xlrd.open_workbook(xl_filename)
    cur_sheet = wb.sheet_by_name(xl_sheet)

    # starting position
    r0,c0 = xl_cell_to_rowcol(anchor)
    start_year = int(cur_sheet.cell(r0-2,c0).value.split()[0])
    #extraction first column data
    raw_regions = cur_sheet.col_values(0, start_rowx=r0, end_rowx=None)
    regions = filter(None, (filter_raw_sidenames(r, reference_region_names) for r in raw_regions))
    #extracting data left-right, up-down
    for r,region in enumerate(regions,r0):
        for m,c in enumerate(range(c0,cur_sheet.ncols)):
            year, month = start_year + m//12, m%12 + 1
            #cur_sheet.cell(r,c).value may be float or str 
            yield (cur_sheet.cell(r,c).value,region,yearmon(year, month) ) 


if __name__=="__main__":
    source_def_sample = {
        'varname':'PPI_PROM_ytd', 
        'folder':'xl_sample', 
        'filename':'industrial_prices.xls',
        'sheet':'пром.товаров',
        'anchor':'B5', 'anchor_value': 96.6}
    file_path = os.path.join(source_def_sample['folder'], source_def_sample['filename'])
    gen = read_sheet(file_path, source_def_sample['sheet'], source_def_sample['anchor'])    
    assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))
    for i in range(10):
        print(next(gen))
