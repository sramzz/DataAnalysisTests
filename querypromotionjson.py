import json
import pandas as pd
import jmespath


def read_file(name_file):
    with open(name_file, "r",encoding='utf8') as read_file:
        json_file = json.load(read_file)
    return json_file
# -----
#reading files
name_file = '2022-06-30_ProductErrors.json'
data = read_file(name_file)
#-----
# Expressions or Queries
expression_stores = "[*].metadata.storeId"
expression_timeordered = "[*].metadata.timedOrderTime"
expression_device = "[*].device"
expression_toppings = "[*].products[*].length(toppings[*])"
expression_toppings_detail = "[*].products[*].toppings[*]"
expression_coupon = "[*].products[*].coupon"
expression_isdelivery = "[*].metadata.isDelivery"
expression_num_prods = "[*].length(products[*].id)"
expression_email = "[*].customer.emailAddress"
expression_phone = "[*].customer.phoneNumber"
expression_products = "[*].products[*].id"


#-----
# # testing
# expression_num_attempts = "[*].products[*].length(id)"
# expression_num_prods = "[?customer.emailAddress == 'irenealonsonavajo@gmail.com'].products[*] | length(@)"
# expression_num_prods = "[985].customer.emailAddress"
# num_attempts = jmespath.search(expression_num_attempts, data)
# len(num_attempts)
# num_attempts[985]
#-----
# Saving results in a dictionary
promotion_errors = dict()
stores_webcodes = jmespath.search(expression_stores, data)
time_ordered = jmespath.search(expression_timeordered, data)
device = jmespath.search(expression_device, data)
num_toppings = jmespath.search(expression_toppings, data)
toppings = jmespath.search(expression_toppings_detail, data)
coupon = jmespath.search(expression_coupon, data)
isdelivery = jmespath.search(expression_isdelivery, data)
num_prods = jmespath.search(expression_num_prods, data)
email_address = jmespath.search(expression_email, data)
phone_number = jmespath.search(expression_phone, data)
products = jmespath.search(expression_products, data)
promotion_errors['Webcode'] = stores_webcodes
promotion_errors['EmailAddress'] = email_address
promotion_errors['PhoneNumber'] = phone_number
promotion_errors['TimeOrdered'] = time_ordered
promotion_errors['Device'] = device
promotion_errors['NumToppings'] = num_toppings
promotion_errors['Coupon'] = coupon
promotion_errors['IsDelivery'] = isdelivery
promotion_errors['Products'] = products
promotion_errors['Toppings'] = toppings
promotion_errors['Num_Prods'] = num_prods

#-----
# Exporting to Excel
excel_name = name_file.strip(".json") + '2.xlsx'
df_promotion_errors = pd.DataFrame(promotion_errors)
df_promotion_errors['NumCoupons'] = df_promotion_errors['Coupon'].str.len()
# # removing the [] from the coupon
# df_promotion_errors['Coupon'] = df_promotion_errors\
#     ['Coupon'].apply(lambda x:','.join(map(str,x)))
df_promotion_errors.to_excel(excel_name, index=False)
