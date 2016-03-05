from xls_read import read_by_definition, yearmon

source_def_sample = {
        'varname':'PPI_PROM_ytd', 
        'folder':'xl_sample', 
        'filename':'industrial_prices.xls',
        'sheet':'пром.товаров',
        'anchor':'B5', 'anchor_value': 96.6}

def test_first_value():        
    gen = read_by_definition(source_def_sample) 
    assert next(gen) == (96.6,  "Российская Федерация", yearmon(2009, 1))