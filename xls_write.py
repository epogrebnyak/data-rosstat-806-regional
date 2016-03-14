import pandas as pd

def correct_file_ext(fname):
    # filename extension checking
    if fname.endswith(".xls"):
        return fname.replace(".xls",".xlsx")
    elif fname.endswith(".xlsx"):
        return fname
    else:
        raise ValueError("Incorrect filename: {}".format(fname))
        
def set_styles(wb):
    # setting excel workbook styles, once for a book
    fmt_data = wb.add_format({'bold': False,
                              "font_name": "Arial",
                              'font_color': 'blue',
                              'font_size': 10,
                              'align':'right',
                              })
    fmt_index = wb.add_format({'bold': True,
                               "font_name": "Arial",
                               'font_color': 'red',
                               'font_size': 10,
                               'align':'center',
                               'num_format': 'mm.yy',
                               'border':1
                               })
    fmt_varname = wb.add_format({'bold': False,
                               "font_name": "Arial",
                               'font_color': 'green',
                               'font_size': 10,
                               'align':'left',
                               })

    fmt_header = wb.add_format({'bold': False,
                               "font_name": "Arial",
                               'font_color': 'magenta',
                               'font_size': 8,
                               'align':'left',
                               'valign':'top',
                               'text_wrap' :True,
                               'border':1
                               })

    return {"header" : fmt_header,
            "index" : fmt_index,
            "data" : fmt_data,
            "varname" : fmt_varname}

   
# private function, don't call from outside
def __write_sheet(writer, df, sheet_name, styles):
        # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, index=False, header =False,
                startcol=1, # first column is reserved for inserting index_data
                startrow=1, # first row is reserved for inserting column_data
                sheet_name = sheet_name)
    ws = writer.sheets[sheet_name]
    
    ## Setup sheets cols and row sizes
    ws.set_column('A:A', 18.0)
    ws.set_column('C:DA', 12.0, styles['data'])
    ws.set_column('B:B', 15.0, styles['varname'])
    ws.set_row(0, 33.0) 
    
    # Adding df.index as a first column
    ws.write_column("A2", df.index.to_datetime(), styles['index'])
    #print(df.columns)
    ws.write_row("A1", ["dates"]+df.columns.tolist(), styles['header'])
    
def setup_book(xls_fname:str):
    xls_fname = correct_file_ext(xls_fname)
    writer = pd.ExcelWriter(xls_fname, engine='xlsxwriter')
    styles = set_styles(writer.book)
    return writer, styles 

def write_one_sheet(df:pd.DataFrame, xls_fname:str, sheet_name:str):

    writer, styles = setup_book(xls_fname)
    __write_sheet(writer, df, sheet_name, styles)
    writer.save()

def write_book(df_list, xls_fname:str):
    writer, styles = setup_book(xls_fname)
    for df in df_list:
        try:
            sheet_name = df['varname'][0]
        except:
            raise Exception(df)
        __write_sheet(writer, df, sheet_name, styles)
    writer.save()
