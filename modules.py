# -*- coding: utf-8 -*-

import os
import pandas as pd


def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if pattern in name:
                result.append(os.path.join(root, name))
    return result


def read_data(data):
    doc_nm = pd.read_excel(data, skiprows=0, skip_footer=1000)
    doc_com = pd.read_excel(data, skiprows=1, skip_footer=1000)
    doc_y = pd.read_excel(data, skiprows=2, skip_footer=1000)

    # test if file reads to DataFrame
    assert isinstance(doc_nm, pd.DataFrame)
    assert isinstance(doc_com, pd.DataFrame)
    assert isinstance(doc_y, pd.DataFrame)

    doc_name = "".join([i for i in doc_nm.keys()[0] if not i.isdigit()])
    doc_comment = doc_com.keys()[0]
    doc_years = [ii for ii in doc_y.keys() if 'год' in ii]

    datafile = pd.read_excel(data, skiprows=3, skip_footer=7)

    # Remove digits from the months names
    new_names = []
    for ii in datafile.keys():
        name = ''
        for jj in ii:
            if jj.isalpha():
                name = name + jj
        new_names.append(name)
    datafile.rename(columns=dict(zip(datafile.keys(), new_names)), inplace=True)

    # Replace space on the end of the region name if exists
    for nm in datafile['Unnamed']:
        new = "".join([i for i in nm if not i.isdigit()])
        datafile.replace(nm, new, inplace=True)
        if nm[-1] == ' ':
            nnm = nm[:-1]
            datafile.replace(nm, nnm, inplace=True)

    return doc_name, doc_comment, doc_years, datafile


# # read data
# doc_name, doc_comment, doc_years, datafile = read_data('230-232 ' + source_definitions[2]['filename'])
#
# # todo:
# # - summable regions
#
# # - regions by district
# districts = []
# districts_rows = []
# for row, nm in enumerate(datafile['Unnamed']):
#     if 'федеральный округ' in nm:
#         districts.append(nm)
#         districts_rows.append(row)
#
# center_district = datafile.iloc[districts_rows[0]:districts_rows[1]].reset_index(drop=True)
# north_west_district = datafile.iloc[districts_rows[1]:districts_rows[2]].reset_index(drop=True)
# south_district = datafile.iloc[districts_rows[2]:districts_rows[3]].reset_index(drop=True)
# north_caucasus_district = datafile.iloc[districts_rows[3]:districts_rows[4]].reset_index(drop=True)
# volga_district = datafile.iloc[districts_rows[4]:districts_rows[5]].reset_index(drop=True)
# ural_district = datafile.iloc[districts_rows[5]:districts_rows[6]].reset_index(drop=True)
# siberia_district = datafile.iloc[districts_rows[6]:districts_rows[7]].reset_index(drop=True)
# far_eastern_district = datafile.iloc[districts_rows[7]:districts_rows[8]].reset_index(drop=True)
# crimea_district = datafile.iloc[districts_rows[8]:].reset_index(drop=True)
#
# # Test districts names
# assert testable_district_names[0] in center_district['Unnamed'][0]
# assert testable_district_names[1] in north_west_district['Unnamed'][0]
# assert testable_district_names[2] in south_district['Unnamed'][0]
# assert testable_district_names[3] in north_caucasus_district['Unnamed'][0]
# assert testable_district_names[4] in volga_district['Unnamed'][0]
# assert testable_district_names[5] in ural_district['Unnamed'][0]
# assert testable_district_names[6] in siberia_district['Unnamed'][0]
# assert testable_district_names[7] in far_eastern_district['Unnamed'][0]
# assert testable_district_names[8] in crimea_district['Unnamed'][0]
#
#
# # Test regions names
# for test_dist, dist in zip(testable_district_names, districts):
#     assert test_dist in dist
#
# # Test if all regions are in datafile
# for test_nm, nm in zip(testable_region_names, datafile['Unnamed'].values):
#     assert test_nm in nm
#
# # Test years
# for test_ye, ye in zip(years, doc_years):
#     assert str(test_ye) in ye