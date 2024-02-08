import ast
import re
from shopify_functions import order_info_shopify


def sort_and_strip(name,key,obj):
   
    if isinstance(obj, str):
        
        obj = obj.replace('"', "'")
        obj=obj.rstrip("'")
        obj= obj.replace("''","'")
        obj= obj.replace("+'","")
        
        try:
            new_obj= ast.literal_eval(obj)
 
            new_obj=set(new_obj)
            return new_obj

        except (ValueError, SyntaxError):
            print("The value of the field contains invalid syntax either (,{,\) ", obj)
        


def list_to_set(obj):
    
    if isinstance(obj, str):
        new_set_obj = set(obj[1:-1].split(",")) # remove the brackets and split by comma
        return new_set_obj

    else:
        return obj


def updating_the_metafield_values(shopify_products, sf_products):
    
    for name, value in shopify_products.items():
        for key, value in shopify_products[name]['metafields'].items():
          
            updated_field_1= sort_and_strip(name,key,value) #remove spaces and commas
            
            shopify_products[name]['metafields'].update({key: updated_field_1})
    
    for name, value in sf_products.items():
        for key, value in sf_products[name]['metafields'].items():
            
            updated_field_2= sort_and_strip(name, key, value)
   
            sf_products[name]['metafields'].update({key: updated_field_2})

    
        
    
#Checking Products Response of Shopify and Salesforce
def verifying_both_env_response_product(shopify_products, sf_products):


    print("\n")
    print("==================================")
    print("\n")
    print("The Below Products are the passed products =========== >")    
    print("\n")
    #executing function for removing and creating the  sets
    updating_the_metafield_values(shopify_products, sf_products)


    for name,data in shopify_products.items():
        
        print(name)
        if name in sf_products:

            
            sf_data = sf_products[name]



            #Comparing both SKU and ID values
            if data['SKU']!= sf_data["SKU"] or data["product_id"]!=sf_data["product_id"] or data["metafields"]!=sf_data["metafields"]:
            #printing message for mismatch
                
                """
                #check which value is missing or different
                if data["SKU"] != sf_data["SKU"]:
                    print(f"Product SKU Changed observed in {name}")
                    print(f" Shopify SKU = {data['SKU']} , Salesforce SKU = {sf_data['SKU']}")
                """
            
                if data["product_id"] != sf_data["product_id"]:
                    print(f"Product ID Change observed in {name}")
                    print(f"Product ID shopify = {data['product_id']}. Product ID Salesforce = {sf_data['product_id']}")


                if data["metafields"] != sf_data["metafields"]:
                    print("\n")
                    print(f"{name} Metafield change")
                    print("\n")
                    #print("Shopify...")
                    #print(data["metafields"])
                    #print("\n\n\n")
                    #print("Salesforce...")
                    #print(sf_data["metafields"])
                   
            
                    

        else:
            #the product is not exists in shopify or salesforce just print that product name msg
            print(f"the Product {name} is not exists in any Environment Shopify/Salesforce verify it....")


#----------------------------------------------------------------------------------
#Checking Order Respoinses of Shopify and Salesforce



def verifying_both_env_response_order(shopify_search_order, sf_search_order):

 
    for name, data in shopify_search_order.items():
        #check that if the product exists in the salesforce products
        print("Checking for the Order: ",name)
        if name in sf_search_order:
            #get the respone data value {billing, shipping, contact) from the salesforce for that order response
            sf_data = sf_search_order[name]

            #Comparing both billing, shipping and contact values
            #if (data['Billing']!= sf_data["Billing"] or 
            
            if (('Shipping' in data and data["Shipping"])!=('Shipping' in sf_data and sf_data["Shipping"]) or 
            ('Shipping' in data and data["Shipping"])!=('Shipping' in sf_data and sf_data["Shipping"]) or 
            data["Contact"] != sf_data["Contact"]) or ('transaction1' in data and 'transaction1' in sf_data and data['transaction1']!=sf_data['transaction1']) or ('transaction2' in data and 'transaction2' in sf_data and data['transaction2']!=sf_data['transaction2'] or
            data["Order_Price_details"] != sf_data["Order_Price_details"]):
            #printing message for mismatch
                print(f"the values of {name} are not same in both environment Sopify/Salesforce")
            
                #check which value is missing or different
                #if data["Billing"] != sf_data["Billing"]:
                #    print(f" Shopify Billing Details are not same with Salesforce Billing Detailss")
            
            
                if (('Shipping' in order_info_shopify[f'{name}'])and data["Shipping"]) != (('Shipping' in order_info_shopify[f'{name}'])and sf_data["Shipping"]):
                    print(f" Shopify Shipping Details are not same with Salesforce Shipping Details")

                if data["Contact"] != sf_data["Contact"]:
                    print(f" Shopify Contact Details are not same with Salesforce Contact Details")

                if (("transaction1" in data) and data["transaction1"]) != (("transaction1" in sf_data) and sf_data["transaction1"]):
                    print(f"Shopify Transaction details of gateway {data['transaction1']['gateway']} order {name} are not same with Salesforce..")

                if (("transaction2" in data) and data["transaction2"]) != (("transaction2" in sf_data) and sf_data["transaction2"]):
                    print(f"Shopify Transaction details of gateway {data['transaction2']['gateway']} order {name} are not same with Salesforce..")

                if data["Order_Price_details"]!= sf_data["Order_Price_details"]:
                    print("Shopify Order Price details is not same with Salesforce Order Price details")

        else:
            #the product is not exists in shopify or salesforce just print that product name msg
            print(f"the Order {name} is not exists in any Environment Shopify/Salesforce verify it....")

