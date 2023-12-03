#Creator: Santiago Ramz
#Importing libraries
import os
import numpy as np
import pandas as pd
import datetime as date
import re

#Setting the working directory
os.getcwd()
os.chdir("C:/Users/SantiagoRamirezCasta/Desktop/PromotionsPH/SantiagoSolves")
#Read file
df_bible = pd.read_excel("S4D PH PROMOCIONES FALTANTES.xlsx")

#df_bible = pd.read_csv("NewBible.csv",encoding = "utf-8")
#Stripping those horrific spaces that CDD likes to put
df_cols = df_bible.select_dtypes(object).columns #the columns with text
df_bible[df_cols] = df_bible[df_cols].apply(lambda x: x.str.strip())

#Order by  PM_CODE then by STORE_NAME
df_bible = df_bible.sort_values(by=['PM_CODE',"STORE NAME"],ascending=[True,True])

#Give a format to the prices
pd.set_option('display.float_format','{:.3f}'.format)
condition_format_price = (df_bible['Value'] >= 1000.00)
df_bible.loc[condition_format_price,'Value'] = df_bible['Value']/1000
df_bible['Value'].unique()

#GOAL: Get the store on which each promotion is applied, the days when this one is active
#MOST IMPORTANT: Get the product to which the promotion applies
#Getting the stores and the promotions
pmcodes = df_bible.PM_CODE.unique()
stores = df_bible.iloc[:,2].unique()
promotexts = df_bible.iloc[:,3].unique()
#Adding a column that tells if the coupon has expired or not
df_bible.columns #checking what is the index of the column with the expiring date
df_bible.dtypes #checking the data types of each column
df_bible['coupon_expired?'] = np.where(df_bible.iloc[:,7] <= date.datetime(2021, 5, 17),True,False)

#GETTING ALL INFORMATION
#We are gonna save the data of each promotion depending on the store
#Create a dict in which we'll save the data
promotions = {"Webcode":[],"PromoCode":[],"StartDate":[],"EndDate":[], \
"Menu/Offer":[],"Price1":[],"PromoText":[],"Benefits":[],"DaysActive":[], \
"OrderType":[],"SalesChannel":[],"UsedWithOtherCpns":[],"DiscountPercentage":[], \
"DiscountFlat":[],"Gifts":[],"ProductExceptions":[],"Products":[],"CodeProducts":[], \
"Size":[],"CodeSize":[],"Units":[]}
new_store = {"PromoCode":[],'Stores0':[],'Stores1':[],'Stores2':[],'Stores3':[],'Stores4':[]}
#The basic approach is to filter the bible by promotion and then by information needed
#then take the unique values
for pm_code_index in range(len(pmcodes)):
    #Assigning the coupon. Filter by coupon
    condition_pmcode = (df_bible.PM_CODE == pmcodes[pm_code_index]) #coupon
    df_pm_code = df_bible[condition_pmcode]
    #Webcode
    webcode_promotion = df_pm_code.iloc[0,3]
    webcode_promotion = webcode_promotion.tolist()
    promotions["Webcode"].append(webcode_promotion)
    #Pmcode
    promocode = pmcodes[pm_code_index]
    promotions["PromoCode"].append(promocode)
    new_store['PromoCode'].append(promocode)
    #Startdate
    startdate_promotion = df_pm_code.iloc[0,6]
    promotions["StartDate"].append(startdate_promotion)
    #Enddate
    enddate_promotion = df_pm_code.iloc[0,7]
    promotions["EndDate"].append(enddate_promotion)
    #Menu
    menu_promotion = df_pm_code.iloc[0,15]
    promotions["Menu/Offer"].append(menu_promotion)
    #benefits
    benefits1 = df_pm_code.iloc[:,8].unique()
    promotions["Benefits"].append(benefits1)
    #Price and Stores
    price1 = df_pm_code.iloc[:,12].loc[df_pm_code['Piece'] == "Precio_Fijo"].unique()

    #search for the price outputting the unique values of the stores
    #there are multile pricing levels, search those and save the stores too
    if len(price1) != 0:
        counter = 0
        #Check how many pricing levels there are, based on this save the stores to where it belongs
        for price_index,price_level in enumerate(price1):
            condition_price = ((df_pm_code['Piece'] == 'Precio_Fijo') & (df_pm_code['Value'] == price_level))
            stores_promotion = df_pm_code.iloc[:,2].loc[condition_price].unique()
            store_column_name = f'Stores{counter}'
            if store_column_name not in new_store:
                new_store[store_column_name]  = []
            new_store[store_column_name].append(stores_promotion.tolist())
            # print(len(stores_promotion),new_store[store_column_name])
            counter += 1
        #Fill up the other fields of the other stores
        for i in range(price_index+1,6):
            store_column_name = f'Stores{i}'
            if store_column_name not in new_store:
                new_store[store_column_name]  = []
            new_store[store_column_name].append(["NaN"])
        #Fill up the prices
        promotions["Price1"].append(price1)
    else:#the bible does not provide price
        #Search if there are more than 1 benefit texts
        #Search if there is a price in the benefit text
        #Extract that price and save it with the stores to where it belongs
        benefit_list = benefits1.tolist()
        price_extracted = []
        for benefit_index,benefit in enumerate(benefit_list):
            #check if there is a price in the text of the benefit
            match_benefit = bool(re.search(r'(\d*\,?\d{1,2}(€| euros))',benefit))
            condition_benefits = ((df_pm_code.iloc[:,8] == benefit))
            #save the stores
            stores_promotion = df_pm_code.iloc[:,2].loc[condition_benefits].unique()
            store_column_name = f'Stores{benefit_index}'
            if store_column_name not in new_store:
                new_store[store_column_name]  = []
            new_store[store_column_name].append(stores_promotion.tolist())
            if match_benefit: #if there is a price in the text then save the price
                price_regex = re.compile(r'(\d*\,?\d{1,2}(€| euros))').findall(benefit)[0][0]
                price_regex = float(price_regex.strip("€ euros").replace(',','.'))
                price_extracted.append(price_regex)
            else: #no price, save 0
                price_extracted.append(0)
        #Fill up the rest of the store fields
        for i in range(benefit_index+1,6):
            store_column_name = f'Stores{i}'
            if store_column_name not in new_store:
                new_store[store_column_name]  = []
            new_store[store_column_name].append(["NaN"])
        promotions["Price1"].append(price_extracted)

    #promotext
    promotext1 = df_pm_code.iloc[:,5].unique()
    promotions["PromoText"].append(promotext1)

    #Days
    condition_days1 = ((df_pm_code['Piece'] == "Dia_y_Hora") & \
        (df_pm_code['Operator'] != 'No influye') & (df_pm_code['Value'] != 8) & \
            (df_pm_code['Value'] != 9))
    days_promotion1 = df_pm_code.Value.loc[condition_days1].unique()
    # print(days_promotion1,pmcodes[pm_code_index])
    promotions["DaysActive"].append(days_promotion1)

    #Ordertype
    ordertype1 = df_pm_code.iloc[:,14].loc[df_pm_code['Piece'] == "Forma_Solicitud"].unique()
    promotions["OrderType"].append(ordertype1)

    #SalesChannel
    saleschannel1 = df_pm_code.iloc[:,14].loc[df_pm_code['Piece'] == "Forma_Entrega"].unique()
    promotions["SalesChannel"].append(saleschannel1)

    #UsedWithOtherCpns?
    accrueable = df_pm_code.iloc[:,12].loc[df_pm_code['Piece'] == "Acumulable"].unique()
    promotions["UsedWithOtherCpns"].append(accrueable)

    #DiscountPercentage
    condition_discount_percentage = ((df_pm_code['Level'] == "Descuento importe total") & \
        (df_pm_code['Operator'] == "%"))
    DiscountPercentage1 = df_pm_code['Value'].loc[condition_discount_percentage].unique()
    promotions["DiscountPercentage"].append(DiscountPercentage1)

    #DiscountFlat
    condition_discount_flat = ((df_pm_code['Level'] == "Descuento importe total") & \
         (df_pm_code['Operator'] == "="))
    DiscountFlat1 = df_pm_code['Value'].loc[condition_discount_flat].unique()
    promotions["DiscountFlat"].append(DiscountFlat1)

    #Gifts
    condition_gifts = (df_pm_code['Level'] == "Regalos") & (df_pm_code['Piece'] == "Grupos")
    gifts1 = df_pm_code.iloc[:,13].loc[condition_gifts].unique()
    promotions["Gifts"].append(gifts1)

    #ProductExceptions
    product_exeptions1 = df_pm_code.iloc[:,13].loc[df_pm_code['Level'] == "Productos Excluidos"].unique()
    promotions["ProductExceptions"].append(product_exeptions1)

    #Products
    condition_products = (df_pm_code['Piece'] == "Grupo") & (df_pm_code['Level'] == "Producto")
    products_promotion = df_pm_code.iloc[:,14].loc[condition_products].unique()
    promotions["Products"].append(products_promotion)
    code_products_promotion = df_pm_code.iloc[:,13].loc[condition_products].unique()
    code_products_promotion = code_products_promotion.tolist()
    promotions["CodeProducts"].append(code_products_promotion)

    #Size
    condition_size = (df_pm_code['Piece'] == "Tamaño") & (df_pm_code['Level'] == "Producto")
    product_size_promotion = df_pm_code.iloc[:,14].loc[condition_size].unique()
    promotions["Size"].append(product_size_promotion)
    code_product_size_promotion = df_pm_code.iloc[:,13].loc[condition_size].unique()
    code_product_size_promotion = code_product_size_promotion.tolist()#this makes the forma readible later on
    promotions["CodeSize"].append(code_product_size_promotion)

    #Units
    condition_units = (df_pm_code['Piece'] == "Unids") & (df_pm_code['Level'] == "Producto")
    product_units_promotion = df_pm_code.iloc[:,12].loc[condition_units].unique()
    promotions["Units"].append(product_units_promotion)

#Saving the data in a dataframe
df_promotions = pd.DataFrame.from_dict(promotions,orient='index')
#Transposing the df then it looks nice
df_promotions = df_promotions.T
#Adding the stores to the promotions
# save_stores = pd.DataFrame()
for k in list(new_store.keys()):
    # len(new_store[k])#making sure all the columns have the same rows
    # save_stores[k] = pd.Series(new_store[k])#testing other df
    df_promotions[k] = pd.Series(new_store[k])

#exporting
df_promotions.to_excel('newestpromotions_v1.xlsx')