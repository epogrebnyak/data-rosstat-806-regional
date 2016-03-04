# COMMENT: funcs.py too generic name, maybe filter_raw_sidenames.py?
# ok, renamed

def filter_raw_sidenames(raw_region_name:str, reference_regions:list):
    #QUESTION: ":str" это что-то очень новое или очень старое? где можно почитать про объявление типа в питоне?
    # Это хинты (подсказка какой тип данных) подробнее здесь https://www.python.org/dev/peps/pep-0484/
    """
    Converts a raw region title to reference region title
    Inputs:
        reference_regions - list of reference region titles
        raw_region_name - string with raw region title
    Output:
        string with reference region titles
           or
        ""  (if no one matched)
    """
    # COMMENT: if output is string, better return empty string "" when not found
    # Ok
    
    def purifying(raw_region):
        return raw_region.replace("округов", "округа").replace("в том числе","").replace(" ", "").strip("0123456789")

    matched_reference_names = []
    raw_region_name = purifying(raw_region_name)
    
    for ref_region in reference_regions:
    
        # QUESTION: is this a duplicate of purifing? 
        #           why not ref_region = purifying(ref_region)
        #           better without extra new variable *r*
        # it is preparing etalon region name for matching, 
        #r = ref_region.replace(" ", "").replace("округов", "округа")
        r = purifying(ref_region)
        # raw_region_name name matches reference name exactly 
        if r==raw_region_name:
            return ref_region #exact match
            
        else:
            if r in raw_region_name:
                matched_reference_names.append(ref_region)
    
    #  if only one is similar            
    if len(matched_reference_names)==1:
        return matched_reference_names[0]
        
    # return longest matched region    
    elif len(matched_reference_names)>1:
        return max(matched_reference_names, key = len) 
    
    # returning empty string if no one match
    return ""

if __name__=="__main__":
    
    
    #QUESTION: what is  sample_regions1? file seems missing
    #COMMENT - I noticed sys.path.append(os.path.dirname(os.path.dirname(__file__))) in other file, not best practive unless VERY needed. 
    #Suggested import: from test.sample_regions import ...  - make it importable from package  
    # fixed

    from sample_regions_tests.sample_regions_2 import regions as raw_regions
    from reference_region_names import reference_region_names    

    for r in raw_regions:
        # cannot understand the intent of ___repr__()
        # it is to see the difference between strings like "область" and "область ". without this you cannot see spaces in strings
        print(filter_raw_sidenames(r, reference_region_names).__repr__(),"::", r.__repr__())
        
