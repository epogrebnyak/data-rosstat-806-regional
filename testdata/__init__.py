test_regions_dict = {}
"""
key = xls filename
value = raw list of region
"""
for n in range(2,16):
    sample = __import__('sample_regions_{0}'.format(n), globals(), locals(), ['name','raw_regions'], 1)
    test_regions_dict[sample.name]=sample.regions
