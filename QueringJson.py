import jmespath
import json
import pandas as pd
import numpy as np

def drop_duplicate(duplicated):
    ls_without_duplicates = []
    duplicated_list = duplicated.copy()
    for item in duplicated_list:
        if item not in ls_without_duplicates:
            ls_without_duplicates.append(item)
    return ls_without_duplicates

def drop_duplicate_new(duplicated):
    unique = []
    for i in range(0,len(duplicated)):
        d = 0
        for j in range(0,i):
            if (duplicated[i] == duplicated[j]):
                d = 1
                break
        if (d == 0):
            unique.append(duplicated[i])
    return unique

def read_file(name_file):
    with open(name_file, "r",encoding='utf8') as read_file:
        json_file = json.load(read_file)
    return json_file

def extract_store_closed(json_file):
    stores_closed = json_file
    expression_webcode = "[*].params[0].value"
    expression_names = "[*].params[1].value"

    store_webcodes_duplicated = \
        jmespath.search(expression_webcode, stores_closed)
    #store_webcodes = drop_duplicate(store_webcodes_duplicated)
    store_webcodes = store_webcodes_duplicated
    store_names_duplicated = \
        jmespath.search(expression_names, stores_closed)
    # store_names = drop_duplicate(store_names_duplicated)
    store_names = store_names_duplicated

    stores_closed_dic = dict()
    stores_closed_dic['Webcode'] = store_webcodes
    stores_closed_dic['StoreName'] = store_names

    return stores_closed_dic

name_file = "2022-05-10_ClosedStoresV3.json"
stores_closed_json = read_file(name_file)
print(extract_store_closed(stores_closed_json))

stores_closed_dic = extract_store_closed(stores_closed_json)
excel_name = name_file.strip(".json") + '.xlsx'
df_stores_closed = pd.DataFrame(stores_closed_dic)
df_stores_closed.to_excel(excel_name, index=False)

print('Excel has been gerated')


