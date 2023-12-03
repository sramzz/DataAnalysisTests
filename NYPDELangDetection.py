from LanguageDetect import detect_language
import pandas as pd
content_items = pd.read_excel('G:/My Drive/NYP/DE/Tranlations/ContentToTranslate.xlsx',\
    sheet_name = 'Sheet1', header = 0)

#First remove strange symbols and then find the language
#you gotta run the code 10 times and if the result is different
#the text is ambiguos
content_items["ValueTransformed"] = \
    content_items["Value"].replace\
        (to_replace='[^A-Za-z0-9 ]', regex=True,value='')
content_items["Language"] = content_items["ValueTransformed"].\
    apply(detect_language)
content_items["Lang"],content_items["LangProb"] = zip(*content_items["Language"])

content_items.to_excel('G:/My Drive/NYP/DE/Tranlations/2022-04-12_ContentLanguageCategories.xlsx',index=False)
