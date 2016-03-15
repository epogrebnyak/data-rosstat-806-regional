import os
ROOT_DATA_FOLDER = os.path.join("xls", "info_stat_01_2016")

XL_SAMPLE_FOLDER = os.path.join('xls', 'sample')

CSV_FOLDER = 'csv'

output_folder = os.path.join("xls", "debug_output")
OUTPUT_XLS = {  'by_sheet':  os.path.join(output_folder, "rosstat_806_regional.xls")
              , 'one_page':  os.path.join(output_folder, "rosstat_806_regional_one_page.xls")
              , 'rf':        os.path.join(output_folder, "rosstat_806_RF.xls")
              , 'districts': os.path.join(output_folder, "rosstat_806_districts.xls")
              , 'summable':  os.path.join(output_folder, "rosstat_806_summmable_regions.xls")
              , 'varnames':  os.path.join(output_folder, "varnames.xls")
              }
