from xls_read import read_by_definition, yearmon

source_def_sample = {
        'varname':'PPI_PROM_ytd', 
        'folder':'xl_sample', 
        'filename':'industrial_prices.xls',
        'sheet':'пром.товаров',
        'anchor':'B5', 'anchor_value': 96.6}

def_dict_2 = {'varname':'SHIPMENTS', 
     'folder':'xl_sample', 
   'filename':'shipment.xls',
      'sheet':'Млн.рублей',
     'anchor':'B6', 'anchor_value': 5331853.711}    
        
def test_first_value():        
    gen = read_by_definition(source_def_sample) 
    assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))
    
def test_auto_search():
    gen1 = read_by_definition(source_def_sample, True)
    gen2 = read_by_definition(source_def_sample, False)    
    assert next(gen1) == next(gen2)
    
    gen1 = read_by_definition(def_dict_2 , True)
    gen2 = read_by_definition(def_dict_2 , False)    
    assert next(gen1) == next(gen2)