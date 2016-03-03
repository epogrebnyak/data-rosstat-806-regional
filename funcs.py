def filter_raw_sidenames(test_region:str, etalon_region_titles:list):
    """
    converts a raw region title to etalon region title
    Inputs:
        etalon_region_titles - list of etalon region titles
        test_region    - string with raw region title
    Output:
        string with etalon region titles
           or
        None  (if no one matched)
    """
    def purifying(region):
        return region.replace("округов", "округа").replace("в том числе","").replace(" ", "").strip("0123456789")

    found = []
    test_region = purifying(test_region)
    for region in etalon_region_titles:
        r = region.replace(" ", "").replace("округов", "округа")
        if r==test_region:
            return region #exact match
        else:
            if r in test_region:
                found.append(region)
    if len(found)==1:
        return found[0] #  if only one is similar
    elif len(found)>0:
        return max(found, key = len) # return longest matched region
    # returning None if no one match

if __name__=="__main__":
    from sample_regions1 import regions
    from region_titles import etalon_region_titles
    ##
    sample_etalon = list(regions.values())
    row_regions = sorted(list(regions.keys()))
    assert set(sample_etalon)==set(etalon_region_titles), "Etalons not match"

    for r in row_regions:
        print(filter_raw_sidenames(r, etalon_region_titles).__repr__(),"::", r.__repr__())
        
