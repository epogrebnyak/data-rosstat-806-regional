# Russian regional economic datasets

##Pseudocode for data import 

Started implementation at [pseudo.py](pseudo.py)

TODO: need test for import results, checking the following - 
```
def_dict0 = {'varname':'PPI_PROM_ytd', 
     'folder':'11 цены производителей', 
   'filename':'индексы цен производителей промышленных товаров.xlsm',
      'sheet':'пром.товаров',
     'anchor':'B5', 'anchor_value': 96.6} 

# df_get_summable_regions
df1 = df_get_all_rows_from_sheet(def_dict0)

# check anchor cell, upper-left corner
assert df1.iloc[0,0] == def_dict0['anchor_value']

# check rows names are equal to testable_sidebar_doc if testign for df_get_summable_regions
# ...

# check some random hardcoded values from datafra,me, including lower right corner
# ...

```

TODO: seprate preparation and algorighm - save publication in 'sourcefiles' folder + unpack + name + import test

```
def get_filename(def_dict):
   return os.path.join(project_root_folder, 'sourcefiles', ...,  def_dict['folder'], def_dict['filename'])
   
assert os.path.exists(get_filename(def_dict0))   

```


1. RAR file downloaded manually 
2. Unpack RAR file to local folder
3. Define a list of imported Excel sheets as a list of source definitions
4. Source definition is: (assinged varname, folder, filename, sheet, optional anchor cell)  
  - *assinged varname* must match/be similar to variables used in <https://github.com/epogrebnyak/rosstat-kep-data>
  - *optional anchor cell* is usually B5 or B6. It is always B column. 
5. Emit a stream of (assinged varname, rown, coln, value) from sheet - use xlrd?
  - may substitute coln, rown with colx, rowx
6. Convert *coln* to date, based on fact that all date ranges start with Jan 2009 (column B = Jan 2009, column C = Feb 2009, etc): ```dt = col_to_date(coln, source_def)```
7. Convert *rown* to region name ```region_name = row_to_region_name(rown, sheet)``` making comparison to reference list of regions + substitute some region names
   - also mask/subset stream of (assinged varname, rown, coln, value) based on desired output - see below
   - may need to construct a substitution dictionary based on testable_sidebar_doc and sidebar_doc
   - also check if all rownames are like sidebar_doc, otherwise add to dict
8. Get dataframes as below:
```    
df1 = df_get_all_rows_from_sheet(source_def)
df2 = df_get_summable_regions(source_def)
df3 = df_get_districts(source_def)
df4 = df_get_RF(source_def)
```
Note: from every sheet can also read a flat stream like (varname, region_name, date, value). 

9. Extend to full dataset as ```rf_df = df_get_all_RF()```
10. Save:
 - all obtained dataframes as sheets in resulting files as tables  RF + districts + summable regions
 - as all-RF data by variable and by date
 - suggested pattern in xls (for SA) - TODO- must save to project
 - list of variables as varnames.md
