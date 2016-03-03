# COMMENT: funcs.py too generic name, maybe filter_raw_sidenames.py?

def filter_raw_sidenames(raw_region_name:str, reference_regions:list):
    #QUESTION: ":str" это что-то очень новое или очень старое? где можно почитать про объявление типа в питоне?
    
    """
    Converts a raw region title to reference region title
    Inputs:
        reference_regions - list of reference region titles
        raw_region_name - string with raw region title
    Output:
        string with reference region titles
           or
        None  (if no one matched)
    """
    # COMMENT: if output is string, better return empty string "" when not found  
    
    def purifying(region):
        return region.replace("округов", "округа").replace("в том числе","").replace(" ", "").strip("0123456789")

    matched_reference_names = []
    raw_region_name = purifying(raw_region_name)
    
    for ref_region in reference_regions:
    
        # QUESTION: is this a duplicate of purifing? 
        #           why not ref_region = purifying(ref_region)
        #           better without extra new variable *r*         
        r = ref_region.replace(" ", "").replace("округов", "округа")
        
        # raw_region_name name matches reference name exactly 
        if r==raw_region_name:
            return region #exact match
            
        else:
            if r in raw_region_name:
                matched_reference_names.append(region)
    
    #  if only one is similar            
    if len(matched_reference_names)==1:
        return matched_reference_names[0]
        
    # return longest matched region    
    elif len(matched_reference_names)>0:
        return max(matched_reference_names, key = len) 
    
    # returning None if no one match
    return ""

if __name__=="__main__":
    from sample_regions1 import regions
    #QUESTION: what is  sample_regions1? file seems missing
    
    from region_titles import reference_regions    
    
    sample_reference = list(regions.values())
    row_regions = sorted(list(regions.keys()))
    assert set(sample_reference)==set(reference_regions), "references not match"

    for r in row_regions:
        # cannot understand the intent of ___repr__()
        print(filter_raw_sidenames(r, reference_regions).__repr__(),"::", r.__repr__())
        
