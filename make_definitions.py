import os
import xlrd
from xls_read import seek_origin

DEFINITIONS_FILENAME = "definitions.py"

EXT = ".xls"

FORBIDDEN = {
'323-328 численность ЭАН. занят и безраб.xls',
"365-367 численность работников на предприятиях малого и среднего бизнеса.xls",
}

RECORD_TEMPLATE = """{sb}
 'varname':'{varname}', 
 'folder':'{folder}', 
 'filename':'{filename}',
 'sheet':'{column_data}',
 'anchor_value': {value}
{eb},
"""

def analyze_sheet(xl_filename):
    """Read Excel file and yield data for each definitions entry"""
    wb = xlrd.open_workbook(xl_filename)
    for cur_sheet in wb.sheets(): 
        #cur_sheet = sheet# wb.sheet_by_name(sheet)
        r0,c0 = seek_origin(cur_sheet)
        yield {"value" : cur_sheet.cell(r0,c0).value,
               "column_data" : cur_sheet.cell(r0-3,c0-1).value,
               "left" : cur_sheet.cell(r0,c0-1).value,
               "above" : cur_sheet.cell(r0-1,c0).value,
               "title" : cur_sheet.name,
               }


root_folder = os.path.join("xl_sample", "info_stat_01_2016")


#(filename, filedir (no fullpath))
xls_files  = []
for root, dirs, files in os.walk(root_folder):
    for name in files:
        #print(tuple((name, os.path.split(root)[-1])))
        if name.endswith(EXT):
            xls_files.append(tuple((name, os.path.split(root)[-1])))
        
out = []
c = 0
for f in xls_files:
    if f[0] in FORBIDDEN:
        continue
    l_file = "".join(("\n",
                     "# {} Processing file: {}\n".format(c,f[0]),
                     "#", "_"*77,"\n")
                    )

    print(l_file)
    out.append(l_file)
    for sheet in analyze_sheet(os.path.join(root_folder, f[1], f[0])):
        l_sheet = '# Sheet name: "{}"'.format(sheet["title"])
        l_debug = '# Debugging.  left:"{}", above "{}")'.format(sheet["left"],sheet["above"])
        print(l_sheet)
        print(l_debug)
        lines = RECORD_TEMPLATE.format(varname="Profit_%d"%c,
                                           folder=f[1],
                                           filename=f[0],
                                           column_data=sheet["column_data"],
                                           value = sheet["value"],
                                           sb="{",
                                           eb = "}"
                                       )
        print(lines)
        
        out.append(l_sheet)
        out.append(l_debug)
        out.append(lines)
        c+=1

with open(DEFINITIONS_FILENAME,"w", encoding="utf-8") as f:
    print("definition=[", file=f)
    for l in out:
        print(l, file=f)
    print("]\n", file=f)




    



