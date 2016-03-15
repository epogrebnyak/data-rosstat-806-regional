import os
from debug_config import ROOT_DATA_FOLDER, OUTPUT_XLS
from definitions import definitions
#from getter import get_dataframe_by_definition as get_df
from xls_read import read_by_definition


# select non standart defs
defs = [d for d in definitions if d.get("reader", 'default')!='default']


print(defs[0])
gen = read_by_definition(defs[0]) 
    #assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))
for i in range(30):
    print(next(gen))

