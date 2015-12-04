# Russian regional economic datasets

##Pseudocode for data import 

1. RAR file downloaded manually 
2. Unpack RAR file to local folder
3. Define a list of imported Excel sheets as a list of source definitions
4. Source definition is: (assinged varname, folder, filename, sheet, optional anchor cell)  
  - *assinged varname* must match variables used in <https://github.com/epogrebnyak/rosstat-kep-data>
 - *optional anchor cell* is usually B5 or B6. It is always B column. 
5. Emit a stream of (assinged varname, rown, coln, value) from sheet.
6. Convert *coln* to date, based on fact that all date ranges start with Jan 2009 (column B = Jan 2009, column C = Feb 2009, etc): ```dt = col_to_date(coln, source_def)```
7. Convert *rown* to region name ```region_name = row_to_region_name(rown, source_def)``` making comparison to reference list of regions.
  - *reference list of regions* is 
8. Emit four streams (assinged varname, region_name, date, value) 
```    
df1 = df_get_all_rows(source_def)
df2 = df_get_summable_regions(source_def)
df4 = df_get_districts(source_def)
df4 = df_get_RF(source_def)
```
9. ```rf_df = df_get_all_RF()```
10. Save all obtained dataframes as sheets in resulting files: RF + districts + summable regions

Additional comments:
- may substitute coln, rown with colx, rowx


## Source URL
<http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1246601078438>

# Информация для ведения мониторинга социально-экономического положения субъектов Российской Федерации

Материал содержит важнейшие социально-экономические показатели по регионам России, формируемые Росстатом в соответствии с распоряжением Правительства Российской Федерации от 15 июня 2009г. №806-р для мониторинга процессов в реальном секторе экономики, финансово-банковской и социальной сферах субъектов Российской Федерации, а также другие статистические данные, характеризующие текущее социально-экономическое положение субъектов Российской Федерации: индексы промышленного производства, продукции сельского хозяйства, строительства, оборота розничной торговли, платных услуг населению, инвестиций в основной капитал, потребительских цен. Включены показатели, характеризующие финансовую деятельность организаций, просроченную задолженность по заработной плате, денежные доходы населения, а также данные о структуре занятости и ее динамике.
    Представленная информация позволяет оценивать ежемесячные изменения в экономике и социальной сфере субъектов Российской Федерации. 
    Приводятся данные оперативной отчетности, которые уточняются в последующих выпусках. 

«Информация для ведения мониторинга социально-экономического положения субъектов Российской Федерации» выпускается ежемесячно с апреля 2009 года.
График публикации в 2015 году: <http://www.gks.ru/gis/images/graf-oper2015.htm>
