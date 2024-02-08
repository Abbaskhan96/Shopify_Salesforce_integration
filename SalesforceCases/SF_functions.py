import sys
sys.path.append("./ShopifyCases")
from shopify_functions import product_adding_to_list, payment_non_exists_id, order_info_shopify
from simple_salesforce import Salesforce 
import json
import ast
import random
import requests

def convert_to_list(string):

    try:
        items=[item.strip() for item in string.split(";")] 

        return str(items).strip()
    
    except:
        #The exception is for the empty values of the field
        pass

def search_products_sf(sf):
    #calling provided product names list
    product_names = product_adding_to_list()

    #creating dictionary for storing the response
    product_dict = {}
    

    #Loop through the product naems
    for name in product_names:
    #Query with product name
        
        metafields_names="Light_conditions__c, Soil_Moisture__c, Plant_Type__c, Flower_Color__c, Soil_Type__c, Animal_Resistant__c, Bloom_Type__c, Wildlife_Benefits__c, Plant_Height__c"
           
        #from testCases import sf_multivariants_SKU
        from shopify_functions import multi_variants_SKU, variants_more_than_1

        global multi_variants_SKU, sf_multivariants_SKU, variants_more_than_1
        #print("sf_multivariants_SKU",sf_multivariants_SKU)
        
        query_plant_collection= f"SELECT Species_Product__r.Species_Shopify_MetaObject_Id__c FROM Product_Bundling__c WHERE Collection_Product__r.Name= '{name}'"
                
        if name not in variants_more_than_1:
            #print(f'the plant {name} has no variants')
            
            #metafields_names="Light_conditions__c, Soil_Moisture__c, Plant_Type__c, Flower_Color__c, Soil_Type__c, Animal_Resistant__c, Bloom_Type__c, Wildlife_Benefits__c, Plant_Height__c"
            query = f"SELECT StockKeepingUnit, Shopify_Id__c, {metafields_names} FROM Product2 WHERE  Name = '{name}' AND Is_Parent_Product__c=true "
            #query = f"SELECT StockKeepingUnit, Shopify_Id__c, {metafields_names} FROM Product2 WHERE Name = '{name}'"
            product_dict= sf_all_data(sf,query,query_plant_collection, product_dict, name, False)
            

        else:
            #creating list for storing all sf variants response
            sum_of_variants=[]
            for i, sku in enumerate(multi_variants_SKU[name]):
                #query_var= f"SELECT StockKeepingUnit, Shopify_Id__c, {metafields_names} FROM Product2 WHERE isActive=true StockKeepingUnit = '{sku}'"
                query_var= f"SELECT StockKeepingUnit, Shopify_Id__c, {metafields_names} FROM Product2 WHERE Name = '{name}' AND Is_Parent_Product__c=true"
                #print(query_var)
                #query_var=f"SELECT Collection_Product__r.Name, Collection_Product__r.{metafields_names}, Species_Product__r.Plant_Profile__r.Name, Species_Product__r.Plants_in_this_collection__c FROM Product_Bundling__c Where Collection_Product__r.Name='Buttonbush Shrub'"
                product_dict_multivariant=sf_all_data(sf,query_var, query_plant_collection, product_dict, name, True, sum_of_variants, len(multi_variants_SKU[name]))            
            product_dict=product_dict_multivariant
                
    return product_dict




def find_common_subvalues(list_of_dicts, subkey, name):

    common_list={}
    for subkey in subkey:
        if subkey in list_of_dicts[0][name]['metafields']:
        # initialize a set with the first subvalue
            list_of_dicts[0][name]["metafields"][subkey]=list_of_dicts[0][name]["metafields"][subkey].replace('""]','"]')
            list_of_dicts[0][name]["metafields"][subkey]=list_of_dicts[0][name]["metafields"][subkey].replace('"",','",')
            list_of_dicts[0][name]["metafields"][subkey]=list_of_dicts[0][name]["metafields"][subkey].replace('+"','')
            
            common = set(ast.literal_eval(list_of_dicts[0][name]["metafields"][subkey]))
            
            # loop through the rest of the dictionaries
        for d in list_of_dicts[1:]:
            
            if subkey in d[name]["metafields"]:
                
                d[name]['metafields'][subkey]= str(d[name]['metafields'][subkey])
                d[name]["metafields"][subkey]=d[name]["metafields"][subkey].replace('""]','"]')
                d[name]["metafields"][subkey]=d[name]["metafields"][subkey].replace('"",','",')
                d[name]["metafields"][subkey]=d[name]["metafields"][subkey].replace('+"','')
                common = common.intersection(ast.literal_eval(d[name]['metafields'][subkey]))
                common_str= str(common)
                common_list.update({subkey: common_str})
        # return the common set as a list
    
    list_of_dicts[-1][name]['metafields']=common_list
    return list_of_dicts[-1]


def common_variants_values(var_response, name):
    
    output_list_of_json=[]
    
    for list_val in var_response:
        for all_str in list_val:
            single_str= all_str

        #replcing single quotes for JSON
        single_str=single_str.replace("'",'\\"')
        single_str= single_str.replace(' "','"')
        json_response= json.loads(single_str)
        #print("...JSON")
        
        output_list_of_json.append(json_response)

    new_dict = {}
    subkey=["light_conditions", "soil_moisture", "plant_type", "flower_colour", "soil_type", "animal_resistant", "bloom_type", "wildlife_benefits", "plant_height","plants_in_this_collection"]
    #for subkey in subkey:
    product_dict=find_common_subvalues(output_list_of_json, subkey, name)
    #print(name)
    
    return product_dict
    #print(bloom_type)
    

def sf_all_data(sf,query,plant_collection,product_dict, name, Bool:bool, sum_of_variants=None,  sku_list=None):
    #response = sf.query_all(query)
    response = sf.query_all(query)
    records = response['records']
    
    plant_collection_response= sf.query_all(plant_collection)
    plant_collection_records= plant_collection_response['records']    
    #print(plant_collection_records[0])

    #for record in plant_collection_records:
    #    print(record['Species_Product__r']['Species_Shopify_MetaObject_Id__c'])

    plant_collection_records=[record['Species_Product__r']['Species_Shopify_MetaObject_Id__c'] for record in plant_collection_records]
    
    #print(plant_collection_records)
    if records:
        #print(records)
        sku = records[0]['StockKeepingUnit']
        product_id= str(records[0]['Shopify_Id__c'])
        metafield={
            "light_conditions":convert_to_list((records[0]['Light_conditions__c'])),
            "soil_moisture":convert_to_list((records[0]['Soil_Moisture__c'])),
            "plant_type":convert_to_list((records[0]['Plant_Type__c'])),
            "flower_colour":convert_to_list((records[0]['Flower_Color__c'])),
            "soil_type":convert_to_list((records[0]['Soil_Type__c'])),
            "animal_resistant":convert_to_list((records[0]['Animal_Resistant__c'])),
            "bloom_type":convert_to_list((records[0]['Bloom_Type__c'])),
            "wildlife_benefits":convert_to_list((records[0]['Wildlife_Benefits__c'])),
            "plant_height":convert_to_list((records[0]['Plant_Height__c']))
            }
        metafield["plants_in_this_collection"]=str(plant_collection_records)

        #print("metafield in sf..", metafield["plants_in_this_collection"])
        product_dict[name] = {"SKU": sku, "product_id": product_id, "metafields": metafield}

        empty_keys_to_delete=[]
        for key, value in product_dict[name]["metafields"].items():
            if value==None:
                empty_keys_to_delete.append(key)
        for i in empty_keys_to_delete: 
            del product_dict[name]["metafields"][i]


        
        if Bool:
            
            product_dict= json.dumps(product_dict)
            
            sum_of_variants.append([product_dict])
            
            #print(sku_list, len(sum_of_variants))
            if len(sum_of_variants) == (sku_list):
                product_dict_multivariant= common_variants_values(sum_of_variants, name)
                return product_dict_multivariant
       
    return product_dict



#====================| O R D E R |==========================================================|||


# Keeping mind that for every existing customer order the Billing First Name, Last Name is selected as Shipping First Name Last name in Salesforce
# Sandbox
# & in shopify when new customer created with unique email his customer first name, last name will be duplicate from Billing First Name, Last Name
# However when the same customer create another order his customer first name, last name will be selected aw provided in JSON data payload


order_info={}

def search_order_sforce(sf, customer_order_number):

  
  global order_info


  # Use a SOQL statement to query all orders
  #query = f"SELECT Account.Name,Account.PersonEmail,Account.BillingAddress, Account.Billing_First_Name__c, Account.Billing_Last_Name__c, Account.Billing_State__c, Account.Phone,ShippingAddress, Shipping_State__c, Shipping_First_Name__c, Shipping_Last_Name__c, Shipping_Phone__c, Transaction_Id_c, Payment_Status_c, Paymeny_Method_c, Payment_Type_c, Amount_c  FROM Order where Global_Order_Number__c = '{customer_order_number}'"
  transaction_query= "(SELECT Order_Id__c, Status__c, Payment_Id__c, Created_Date_F__c, Transaction_Type__c, Credit_Card_Number__c, Amount__c, Gateway__c FROM Transactions__r)"
  shipping_billing_query= "Account.Name,Account.PersonEmail,Account.BillingAddress, Account.Billing_First_Name__c, Account.Billing_Last_Name__c, Account.Billing_State__c, Account.Phone,ShippingAddress, Shipping_State__c, Shipping_First_Name__c, Shipping_Last_Name__c, Shipping_Phone__c"
  order_price_query= "TotalAmount, Shipping__c, Discount_Amount__c, SubTotal__c, Discount_Coupon_Code__c, Shopify_Order_Tags__c"

  query = f"SELECT {shipping_billing_query}, {order_price_query}, {transaction_query} FROM Order where Global_Order_Number__c = '{customer_order_number}'"
  

  #print(query)
  # Use the query method to get the record
  result = sf.query(query)
  #print(result)
  # Check if there is a record
  if result["totalSize"] > 0:
    # Get the record as a dictionary
    record = result["records"][0]
    #print(record)
    # Get the billing address
    
    billing_address = record["Account"]["BillingAddress"]
    # Get the shipping address
    shipping_address = record["ShippingAddress"]
    billing_name = record["Account"]["Billing_First_Name__c"]+" "+record["Account"]["Billing_Last_Name__c"]
    if 'Shipping' in order_info_shopify[f'{customer_order_number}']:
    #if (list(order_info_shopify[f'customer_order_number'].keys())) ==([''] or ['']) 
        shipping_name = record["Shipping_First_Name__c"]+" "+record["Shipping_Last_Name__c"] 
    #print(shipping_name)

    billing = {
      "name": billing_name,
      "address1": billing_address["street"],
      "city": billing_address["city"],
      "country": billing_address["country"],
      "zip": billing_address["postalCode"],
      "phone": record["Account"]["Phone"],
      "state": record["Account"]["Billing_State__c"]
      #"province_code": billing_address["state"]
    }
    if 'Shipping' in order_info_shopify[f'{customer_order_number}']:
        shipping = {
          "name": shipping_name,
          "address1": shipping_address["street"],
          "city": shipping_address["city"],
          "country": shipping_address["country"],
          "zip": shipping_address["postalCode"],
          "phone": record["Shipping_Phone__c"],
          "state": record["Shipping_State__c"]
          #"province_code": shipping_address["state"]
        }
    contact= {
        "Customer Name": record["Account"]["Name"],
        "Customer Email": record["Account"]["PersonEmail"]
        }
    # Return the dictionary with the order information
    if 'Shipping' in (order_info_shopify[f'{customer_order_number}']):
        #order_info[str(customer_order_number)] = {"Billing": billing, "Shipping": shipping, "Contact": contact}
        order_info[str(customer_order_number)] = {"Shipping": shipping, "Contact": contact}
    #print(order_info)
    else:
        #order_info[str(customer_order_number)] = {"Billing": billing, "Contact": contact}
        order_info[str(customer_order_number)] = {"Contact": contact}

    #fetching Transaction Reords from Order Query
    tr_record= record["Transactions__r"]

    #Condition for Transaction fields exists for the order
    if tr_record != None:
        #print("this is printing", tr_record["records"])
        for idx,rec_tr in enumerate(tr_record["records"]):
            
            transaction_details= transactions(rec_tr, customer_order_number, idx)

            order_price= order_price_details(record, customer_order_number)

            order_info[str(customer_order_number)].update({f"transaction{idx+1}": transaction_details})
            
            order_info[str(customer_order_number)].update({"Order_Price_details": order_price})


    #for Replacement orders where Transactions are not included
    else:
        order_price= order_price_details(record, customer_order_number)
        order_info[str(customer_order_number)].update({"Order_Price_details": order_price})

    return order_info

    
  else:
    # Return None if there is no record or no order found in Salesforce
    return "Order Not Found...."
    



#Order details functions
def order_price_details(record, customer_order_number):
    #Order Price Data
    subtotal_price= '{:.2f}'.format(float(record["TotalAmount"]))
    shipping_price= '{:.2f}'.format(float(record["Shipping__c"]))
    total_discounts= '{:.2f}'.format(float(record["Discount_Amount__c"]))
    total_price= float('{:.2f}'.format(float(record["SubTotal__c"]))) + float(shipping_price)
    total_price= '{:.2f}'.format(total_price)
    coupon_code = record["Discount_Coupon_Code__c"]
    shopify_order_tags= record['Shopify_Order_Tags__c']

    #converting shipping_price to two decimal digits to make it same as shopify
    #shipping_price= "{:.2f}".format(shipping_price)


    #adding to Dictionary order_price
    order_price={
        "total_line_items_price" : subtotal_price,
        "shipping_price": shipping_price,
        "total_discount": total_discounts,
        "total_price": total_price,
        "coupon_code": str(coupon_code) 
        }

    if (('Shipping' not in order_info_shopify[f'{customer_order_number}']) or
       ('shipping_price' not in order_info_shopify[f'{customer_order_number}']['Order_Price_details'])):
        del order_price['shipping_price']

    if shopify_order_tags =='is_replacement_order':
        #order_price['total_line_items_price']='0.0'
        order_price['coupon_code']='Custom discount'

    if shopify_order_tags == 'donation':
        order_price['total_price']= ('{:.2f}'.format(record["SubTotal__c"]))

    return order_price



#Transaction details function
def transactions(rec_tr, customer_order_number, idx):
    
    #Adding Transaction fields for adding in the output
    order_id= rec_tr["Order_Id__c"]
    payment_id=  rec_tr["Payment_Id__c"]
    gateway=  rec_tr["Gateway__c"]
    status=  rec_tr["Status__c"]
    transaction_type= rec_tr["Transaction_Type__c"]
    amount=  '{:.2f}'.format(rec_tr["Amount__c"])
    
    #Decorated dictionary for showiung in output
    transaction_details = {
          "order_id": order_id,
          "status": str(status),
          "gateway": gateway,
          "type": transaction_type,
          "amount": str(amount),
          "payment_id": payment_id
          }

    #For 'Shop Pay installments order because their payment_id was not in Shopify JSON it will store the payment id in seperate txt file
    if 'payment_id' not in (order_info_shopify[f'{customer_order_number}'][f'transaction{idx+1}']):  

         #Saving the order number, payment id of non exists payment id in shopify JSON---
         with open("C:/Users/Abbas Khan/source/repos/shopify_proj/ShopifyCases/payment_ids_list.txt", 'a') as f:
                 f.write('{}, payment_id= {}\n'.format(customer_order_number, transaction_details["payment_id"]))
            
         del transaction_details["payment_id"]
    
    return transaction_details



def sforce_hgfi_response(sforce, hgfi_auth, hgfi_store_id, customer_order_number):

    
    # for Salesforce
    
    query_1= f"SELECT Product2.Name, Product2.StockKeepingUnit , Product_bundling_Source__c from OrderItem where Order.Global_order_number__c = '{customer_order_number}' and Product_bundling_Source__c ='HGFI'"
    result= sforce.query(query_1)

    #for result in result:
    result= result['records']

    result_sf_name=[result['Product2']['Name'] for result in result]
    result_sf_name=set(result_sf_name)
    
    result_sf_SKU=[result['Product2']['StockKeepingUnit'] for result in result]
    result_sf_SKU=set(result_sf_SKU)

    
    #for HGFI
    
    session= requests.get(f'https://hgfn-prod-webapi.azurewebsites.net/api/Order/{hgfi_store_id}/{customer_order_number}', auth=hgfi_auth)
    session= session.json()

    if 'orderItems' in session:
        orderItems= session['orderItems']
        #print("\n")
        
        result_hgfi_name=[orderItem['name'] for orderItem in orderItems]
        result_hgfi_SKU=[orderItem['skuNumber'] for orderItem in orderItems]
        result_hgfi_name=set(result_hgfi_name)
        result_hgfi_SKU=set(result_hgfi_SKU)

        
        #comparing for Sf and GFI order items both
        #check for the names
        if result_sf_name != result_hgfi_name:
            print(f"Order: {customer_order_number} product names not matched...")
        #check for the SKU
        if result_sf_SKU != result_hgfi_SKU:
            print(f"Order: {customer_order_number} product SKU not matched...")
    #else:
        #print(f"{customer_order_number} has no orderItems object in HGFI")