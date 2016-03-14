from collections import OrderedDict

"""
Wrapper class for:
    reference region names 
    Код ОКАТО и ОКТМО	
    Код ISO 3166-2 и ГОСТ 7.67-2003 (https://goo.gl/szxGMG)

Usage:
    import Regions
    Regions.filter_region_name(raw_region_name:str)
    
    Regions.district_names()  # == district_names, all  methods are classmethods, no instanse is needed
    Regions.summable_regions()  # == summable_regions
    Regions.rf_name()
    Regions.names() # == reference_region_names
    
    Regions.sorted_names()
    Regions.code_table()
        ('Белгородская область', '14', 'RU-BEL')
        ('Брянская область', '15', 'RU-BRY')
        ('Владимирская область', '17', 'RU-VLA')
        ('Воронежская область', '20', 'RU-VOR')
        ('Ивановская область', '24', 'RU-IVA')
        ('Калужская область', '29', 'RU-KLU')
        ('Костромская область', '34', 'RU-KOS')


    Regions.code(region_name)  # returns code for defined region
    Regions.code('г. Москва')
        ('45', 'RU-MOW')
"""

"""
Apparent todo: 
- похоже нет аналога region_by_district https://github.com/epogrebnyak/rosstat-806-regional/blob/master/regions.py#L211

- можете пояснить что нам дает "all  methods are classmethods, no instanse is needed" - не нужно создавать объект класса и 
  запись короче или есть какая-то более глубокая причина?

- с summable_regions может быть проблема по годам - до 2015 это одни, c 2015 могут быть другие (области c 2015 года разбиты по регионы, 
  хочется воспользоваться этой информацией), сделать:
  
  Regions.summable_regions(year = None)
  Regions.summable_regions(2015) - выдает округа и область без округов на Архантельску и Тюмени
  Regions.summable_regions() или Regions.summable_regions(2009)- выдает список только по областям
  
- в приницпе также может быть утроен region_by_district(2015)
  
- Regions.code('г. Москва') по нему несколько пожеланий 

  0. Коды ОКАТО сделать типом int

  1. резултатом должен быть словарь типа  ('name':'Белгородская область', 'int_code':14, 'en_abbr':'RU-BEL')
  
  2. сделать Regions.code() универсальным по входному параметру - Regions.code('Белгородская область'), Regions.code(14), 
     Regions.code('RU-BEL') возвращают один и тот же словарь. Разбор типа параметра - если начинается с русских букв, 
     если int и если начинается с 'RU-', если не подходит то ValueError
     
- (потом /not todo) найти в ГОСТе или придумать коды для федеральных округов

"""


class Regions:
    __REGIONS__ = OrderedDict((
        # namekey, (type(F,D,R), is_summable, code_OKATO, code_ISO)
        ("Российская Федерация" , ("F", False) ), 
        ("Центральный федеральный округ" , ("D", False) ), 
        ("Белгородская область" , ("R", True, "14", "RU-BEL")),
        ("Брянская область" , ("R", True, "15", "RU-BRY")),
        ("Владимирская область" , ("R", True, "17", "RU-VLA")),
        ("Воронежская область" , ("R", True, "20", "RU-VOR")),
        ("Ивановская область" , ("R", True, "24", "RU-IVA")),
        ("Калужская область" , ("R", True, "29", "RU-KLU")),
        ("Костромская область" , ("R", True, "34", "RU-KOS")),
        ("Курская область" , ("R", True, "38", "RU-KRS")),
        ("Липецкая область" , ("R", True, "42", "RU-LIP")),
        ("Московская область" , ("R", True, "46", "RU-MOS")),
        ("Орловская область" , ("R", True, "54", "RU-ORL")),
        ("Рязанская область" , ("R", True, "61", "RU-RYA")),
        ("Смоленская область" , ("R", True, "66", "RU-SMO")),
        ("Тамбовская область" , ("R", True, "68", "RU-TAM")),
        ("Тверская область" , ("R", True, "28", "RU-TVE")),
        ("Тульская область" , ("R", True, "70", "RU-TUL")),
        ("Ярославская область" , ("R", True, "78", "RU-YAR")),
        ("г. Москва" , ("R", True, "45", "RU-MOW")),
        ("Северо-Западный федеральный округ" , ("D", False) ), 
        ("Республика Карелия" , ("R", True, "86", "RU-KR")),
        ("Республика Коми" , ("R", True, "87", "RU-KO")),
        ("Архангельская область" , ("R", True, "11", "RU-ARK")),
        ("Ненецкий авт. округ" , ("R", False, "111/118", "RU-NEN")),
        ("Архангельская область без авт. округа" , ("R", False, "11", "RU-ARK") ), 
        ("Вологодская область" , ("R", True, "19", "RU-VLG")),
        ("Калининградская область" , ("R", True, "27", "RU-KGD")),
        ("Ленинградская область" , ("R", True, "41", "RU-LEN")),
        ("Мурманская область" , ("R", True, "47", "RU-MUR")),
        ("Новгородская область" , ("R", True, "49", "RU-NGR")),
        ("Псковская область" , ("R", True, "58", "RU-PSK")),
        ("г. Санкт-Петербург" , ("R", True, "40", "RU-SPB")),
        ("Южный федеральный округ" , ("D", False) ), 
        ("Республика Адыгея" , ("R", True, "79", "RU-AD")),
        ("Республика Калмыкия" , ("R", True, "85", "RU-KL")),
        ("Краснодарский край" , ("R", True, "3", "RU-KDA")),
        ("Астраханская область" , ("R", True, "12", "RU-AST")),
        ("Волгоградская область" , ("R", True, "18", "RU-VGG")),
        ("Ростовская область" , ("R", True, "60", "RU-ROS")),
        ("Северо-Кавказский федеральный округ" , ("D", False) ), 
        ("Республика Дагестан" , ("R", True, "82", "RU-DA")),
        ("Республика Ингушетия" , ("R", True, "26", "RU-IN")),
        ("Кабардино-Балкарская Республика" , ("R", True, "83", "RU-KB") ), 
        ("Карачаево-Черкесская Республика" , ("R", True, "91", "RU-KC") ), 
        ("Республика Северная Осетия - Алания" , ("R", True, "90", "RU-SE") ), 
        ("Чеченская Республика" , ("R", True, "96", "RU-CE") ), 
        ("Ставропольский край" , ("R", True, "7", "RU-STA")),
        ("Приволжский федеральный округ" , ("D", False) ), 
        ("Республика Башкортостан" , ("R", True, "80", "RU-BA")),
        ("Республика Марий Эл" , ("R", True, "88", "RU-ME")),
        ("Республика Мордовия" , ("R", True, "89", "RU-MO")),
        ("Республика Татарстан" , ("R", True, "92", "RU-TA")),
        ("Удмуртская Республика" , ("R", True, "94", "RU-UD") ), 
        ("Чувашская Республика" , ("R", True, "97", "RU-CU") ), 
        ("Пермский край" , ("R", True, "57", "RU-PER")),
        ("Кировская область" , ("R", True, "33", "RU-KIR")),
        ("Нижегородская область" , ("R", True, "22", "RU-NIZ")),
        ("Оренбургская область" , ("R", True, "53", "RU-ORE")),
        ("Пензенская область" , ("R", True, "56", "RU-PNZ") ),  
        ("Самарская область" , ("R", True, "36", "RU-SAM")),
        ("Саратовская область" , ("R", True, "63", "RU-SAR")),
        ("Ульяновская область" , ("R", True, "73", "RU-ULY")),
        ("Уральский федеральный округ" , ("D", False) ), 
        ("Курганская область" , ("R", True, "37", "RU-KGN")),
        ("Свердловская область" , ("R", True, "65", "RU-SVE")),
        ("Тюменская область" , ("R", True, "71", "RU-TYU")),
        ("Ханты-Мансийский авт. округ - Югра" , ("R", False, "7110/718", "RU-KHM")),
        ("Ямало-Ненецкий авт. округ" , ("R", False, "7114/719", "RU-YAN")),
        ("Тюменская область без авт. округов" , ("R", False, "71", "RU-TYU") ), 
        ("Челябинская область" , ("R", True, "75", "RU-CHE")),
        ("Сибирский федеральный округ" , ("D", False) ), 
        ("Республика Алтай" , ("R", True, "84", "RU-AL")),
        ("Республика Бурятия" , ("R", True, "81", "RU-BU")),
        ("Республика Тыва" , ("R", True, "93", "RU-TY")),
        ("Республика Хакасия" , ("R", True, "95", "RU-KK")),
        ("Алтайский край" , ("R", True, "1", "RU-ALT")),
        ("Забайкальский край" , ("R", True, "76", "RU-ZAB")),
        ("Красноярский край" , ("R", True, "4", "RU-KYA")),
        ("Иркутская область" , ("R", True, "25", "RU-IRK")),
        ("Кемеровская область" , ("R", True, "32", "RU-KEM")),
        ("Новосибирская область" , ("R", True, "50", "RU-NVS")),
        ("Омская область" , ("R", True, "52", "RU-OMS")),
        ("Томская область" , ("R", True, "69", "RU-TOM")),
        ("Дальневосточный федеральный округ" , ("D", False) ), 
        ("Республика Саха (Якутия)" , ("R", True, "98", "RU-SA")),
        ("Камчатский край" , ("R", True, "30", "RU-KAM")),
        ("Приморский край" , ("R", True, "5", "RU-PRI")),
        ("Хабаровский край" , ("R", True, "8", "RU-KHA")),
        ("Амурская область" , ("R", True, "10", "RU-AMU")),
        ("Магаданская область" , ("R", True, "44", "RU-MAG")),
        ("Сахалинская область" , ("R", True, "64", "RU-SAK")),
        ("Еврейская авт. область" , ("R", True, "99", "RU-YEV")),
        ("Чукотский авт. округ" , ("R", True, "77", "RU-CHU")),
        ("Крымский федеральный округ" , ("D", False) ), 
        ("Республика Крым" , ("R", True, "35", "RU-CR")),
        ("г. Севастополь" , ("R", True, "67", "RU-SEV")),
    ))


    @classmethod    
    def filter_region_name(cls, raw_region_name:str):
        # COMMENT: raw_region_name:str is type annotation as in https://www.python.org/dev/peps/pep-0484/
        
        """
        Converts a raw region name to reference region name
        Inputs:
            reference_regions - list of reference region names
            raw_region_name - string with raw region name
        Output:
            string with reference region name
               or
            ""  (if no one matched)
        """
        reference_regions = cls.names()
        
        def prefilter(raw_region):
            return raw_region.replace("округов", "округа").replace("в том числе","").strip("0123456789").replace(" ", "")
        
        # rationale: we need names with spaces as the result of this function
        reverse_dict = {prefilter(r):r for r in Regions.names()}
        
        matched_reference_names = []
        raw_region_name = prefilter(raw_region_name)
        
        for ref_region in [prefilter(r) for r in reference_regions]:
        
            #exact match   
            if ref_region==raw_region_name:
                return reverse_dict[ref_region] 
                
            #partial match    
            else:
                if ref_region in raw_region_name:
                    matched_reference_names.append(reverse_dict[ref_region])
        
        #  only one reference name is similar to raw_region           
        if len(matched_reference_names)==1:
            return matched_reference_names[0]
            
        # return longest matched region    
        ## EP/QUESTION: in what cases is this the case? 'Тюменская область без авт. округов'?
        ##              is it a secure matching procedure?
        ## Yes. in matched_reference_names my be titles only from *reference_region_names*
        elif len(matched_reference_names)>1:
            return max(matched_reference_names, key = len) 
        
        # returning empty string if there is no match
        return ""


    @classmethod
    def names(cls):
        return list(cls.__REGIONS__.keys())

    @classmethod
    def sorted_names(cls):
        return sorted(cls.names())
    
    @classmethod
    def code_table(cls):
        return [(r,data[2], data[3]) for r,data in cls.__REGIONS__.items() if data[0]=="R" and  "без авт." not in r]

    @classmethod
    def district_names(cls):
        return [r for r, data in cls.__REGIONS__.items() if data[0]=="D"]

    @classmethod
    def summable_regions(cls):
        return [r for r, data in cls.__REGIONS__.items() if data[1]]

    @classmethod
    def rf_name(cls):
        return "Российская Федерация"

    @classmethod
    def code(cls, arg):
        out_code = lambda r,data:{'name':r, 'code':data[2], 'en_abbr':data[3]} 
        code_OKATO, code_ISO = None, None
        if arg in cls.__REGIONS__:
            if cls.__REGIONS__[arg][0]=="R":
                return out_code(arg, cls.__REGIONS__[arg])
            else:
                return None
        else:
            for r, data in cls.__REGIONS__.items():
                if data[0]!= "R":
                    continue
                elif arg==data[3] or any(str(arg)==d for d in data[2].split("/")):
                    return out_code(r, data)
                    
                
        
        return cls.__REGIONS__[region.strip()][2:]

    @classmethod
    def region_by_district(cls,district):
        assert district in cls.district_names()
        regions = []
        found = False
        for r, data in cls.__REGIONS__.items():
            if r==district:
                found=True
                continue
            elif found and data[0]=="D": #if found next district name
                return regions
            elif found and data[1]:
                regions.append(r)
        return regions
            
                


#self testing        
if __name__=="__main__":
    from regions import district_names, rf_name, reference_region_names, summable_regions, filter_region_name, region_by_district
    assert filter_region_name("   г.Москва  5")==Regions.filter_region_name("   г. Москва  4")
    print("Code testing")

    print(Regions.code("Брянская область"))
    print(Regions.code("г. Севастополь"))
    print(Regions.code(77))
    print(Regions.code(4))
    print(Regions.code(7110))  #"7110/718", "RU-KHM"
    print(Regions.code("RU-SA"))
    print(Regions.code("Российская Федерация"))
    print(Regions.code("Крымский федеральный округ"))
          
 
    print(Regions.code('г. Москва'))
    print(*Regions.code_table(), sep="\n")
    
    print(set(district_names)-set(Regions.district_names()))
    print(set(Regions.district_names())-set(district_names))
    assert district_names == Regions.district_names()
    assert rf_name == Regions.rf_name()

    print(set(summable_regions)-set(Regions.summable_regions()))
    print(set(Regions.summable_regions())-set(summable_regions))

    
    print(set(reference_region_names)-set(Regions.names()))
    print(set(Regions.names())-set(reference_region_names))

    print("District testing")
    for d in Regions.district_names():
    
        print(d)
        for r in Regions.region_by_district(d):
            print(r in region_by_district[d], "\t", r )
        assert region_by_district[d]==Regions.region_by_district(d)

    assert reference_region_names == Regions.names()
    assert summable_regions == Regions.summable_regions()
