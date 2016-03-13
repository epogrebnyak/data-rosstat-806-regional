import os
ROOT_DATA_FOLDER = os.path.join("xls", "info_stat_01_2016")

 
OUTPUT_XLS = {  'full':      os.path.join("output", "rosstat_806_regional.xls")
              , 'rf':        os.path.join("output", "rosstat_806_RF.xls")
              , 'districts': os.path.join("output", "rosstat_806_districts.xls")
              , 'summable':  os.path.join("output", "rosstat_806_summmable_regions.xls")
              , 'varnames':  os.path.join("output", "varnames.xls")
              }