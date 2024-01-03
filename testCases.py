__unittest = True
import sys
sys.path += ['./Connection_Setup/','./ShopifyCases/','./SalesforceCases','./SS_mixCases']
from ConnectionSetup import *
from shopify_functions import product_adding_to_list, order_adding_to_list, search_products, product_order_exist_result, defined_order_for_searching
from SF_functions import *
from mix_functions import *
import unittest
import shopify
import warnings
from simple_salesforce import Salesforce as sf
import time
import json
from json import dumps
import ast
import re


return_order=None
search_order=None
order_number_updated=None
search_order_sf=None

returned_search_product_dict_sf=None
returned_search_product_dict_shopify=None
provided_products_list=None


self_sf=None
hgfi_auth=None
hgfi_store_id=None

returned_week_order_name= None

shopify_search_week_orders=None
sf_search_week_orders=None


sf_multivariants_SKU={} 

#=====My Required cases clas======================
class Test_Cases(unittest.TestCase):

    def setUp(self):
        global self_sf, hgfi, hgfi_auth, hgfi_store_id
        
        sf_hgfi=activating_connection()
        self_sf= sf_hgfi['salesforce']
        hgfi_auth= sf_hgfi['hgfi_auth']
        hgfi_store_id= sf_hgfi['hgfi_store_id']
        
        #print(hgfi_store_id, hgfi_auth)
        
        

    def tearDown(self):
        clear_connection()


    """
  #-=================Products--Searching--Test--Cases------------------------------------  
      
  #Test Case for Searching the product in Salesforce
    def test_03_search_product_salesforce(self):
       
        print("Case__Salesforce--Searching--Products--Case--is--running")

        warnings.filterwarnings('ignore')
        returned_search_products_dict_sf = search_products_sf(self_sf)
        #print("\n\n")
        #print("salesforce returned,,,")
        #print(returned_search_products_dict_sf)
        
       # print(returned_search_products_dict_sf)
        provided_products_list= product_adding_to_list()
        matching_product=product_order_exist_result(returned_search_products_dict_sf, provided_products_list)
        
        #Asserting that the count of provided product names are same with product responses count
        self.assertEqual(len(provided_products_list),len(returned_search_products_dict_sf), msg = f"{matching_product} Product is missing in Salesforce")
        

    #Test Case for Searching the Product in Shopify
    def test_02_search_product_shopify(self):
        print("Case__Shopify--Searching--Products--Cases--is-running")

        warnings.filterwarnings('ignore')
        
        
        returned_search_products_dict_shopify = search_products()
        #print("shopify returned,,,")
        #print(returned_search_products_dict_shopify)

        from shopify_functions import multi_variants_SKU
        
        global sf_multivariants_SKU
        sf_multivariants_SKU= multi_variants_SKU
        
        provided_products_list= product_adding_to_list()
        matching_product=product_order_exist_result(returned_search_products_dict_shopify, provided_products_list)

        #Asserting that the count of provided product names are same with product responses count
        self.assertEqual(len(provided_products_list),len(returned_search_products_dict_shopify), msg = f"{matching_product} Product is missing in shopify")


    #Test Case that Check that the Attributes Response of Both Shopify and Salesforce is Same
    def test_04_checking_both_env_responses_product(self):
        self.maxDiff = None
        print("Case__Checking for the product attributes in both the environments Shopify/Salesforce")
        
        shopify_products_dict = search_products()
                                                        
       
        sf_products= search_products_sf(self_sf)

        #----Sorting dictionaries fot same key results

        
        
        #Shopify converts
        shopify_products_dict= json.dumps(shopify_products_dict)
        
    
        shopify_products_dict= json.loads(shopify_products_dict)
        
        sf_products= json.dumps(sf_products)
        
        sf_products = sf_products.replace("'", '\\"')
      
        

        sf_products= json.loads(sf_products)
        
        
        verifying_both_env_response_product(shopify_products_dict, sf_products)


        #self.assertEqual(shopify_products_dict, sf_products, msg= "the response data in the environment are not same")
        
    """    
    #-========================Order-Searching-Test-Cases----------------------------------------

    
    #TestCase for matching the ordernumber, items_names of salesforce and hgfi

    def test_sforce_hgfi(self):
        print("Case for matching the order items in salesforce and hgfi")
        list_of_orders= defined_order_for_searching()

        #print(hgfi)
        for i in list_of_orders:
            result= sforce_hgfi_response(self_sf, hgfi_auth, hgfi_store_id, i)

    

    """
    #Test Cases the Check the last week orders details
    def test_05_save_last_week_orders_number(self):
        global returned_week_order_name
        print("Case for fetching the last week order numbers")

        #returned_week_order_name=last_week_orders()
        #returned_week_order_name= defined_order_for_searching()
    
        action= {
        "y": last_week_orders(),
        "n": defined_order_for_searching(),
        "Y": last_week_orders(),
        "N": defined_order_for_searching()
        }
        
        ask= input("Do you want to Match last 7 days orders details..... (y/n)")

        while ask not in list(action.keys()):
            ask= input("You have Entered Wrong Key please Type..... (y/n) or (Y/N)")

        returned_week_order_name = (action["y"] if (ask=='y' or ask=='Y') else action["n"])

    #Test Cases to search the last week order details
    def test_06_search_last_week_orders_shopify(self):
        global shopify_search_week_orders
        order_info_shopify.clear()
        print('Case for Searching the last week Shopify orders')

        orders_str= ['#'+i for i in returned_week_order_name]
        for order in orders_str:
            
            #print("Checking Order: ",order)
            shopify_search_week_orders= search_order_shopify(order)
        
        #print(shopify_search_week_orders)

    def test_07_search_last_week_orders_sforce(self):
        print('Case for Searching the last week order in Salesforce\n\n')
        global sf_search_week_orders
        order_info.clear()
        for i in returned_week_order_name:
            #print(i)
            sf_search_week_orders= search_order_sforce(self_sf, i)
        #print(sf_search_week_orders)
    
    def test_08_check_last_week_orders_response_both_env(self):
        print('Case for matching order details Both Environments....')

        for item1, item2 in zip(shopify_search_week_orders.items(), sf_search_week_orders.items()):
           
            verifying_both_env_response_order(dict([item1]), dict([item2]))
            self.assertEqual(dict([item1]), dict([item2]), msg= "the response data in the environment are not same")
    """
#-----------------------------------------------------------------------------------------------------------------------
    """
    #Test Cases for Creating Order in Shopify
    def test_09_creating_searching_order_shopify(self):
        print("Case__Craeting_Order_in_Shopify")

        global return_order, order_number_updated
        #return_order= create_order(data)
        return_order=23857
        #return_order= 23838
        #return_order= 23831
        #return_order= 23854
        #return_order= 23846
        #return_order= 23836

        order_number_updated= str(return_order)
        order_number_updated="#"+order_number_updated
        #order_number_updated="#23723"
        
        print("Created Order :", order_number_updated)
        #print("checking_order:", order_number_updated)


    #Test Case for Searching Newly Created Order in Shopfify and Fetch the Billing, Shipping and Contact details information
    def test_10_search_new_order_in_shopify(self):
        print("Case__Searching_Order_in_Shopify...")
        
        global order_number_updated, search_order
        
        #print("Wait for {15 sec} for confirming the order....")
        #time.sleep(15)
        search_order= search_order_shopify(order_number_updated)
        print(search_order)


    #Test Case for Searching the Newly Created Order in Salesforce and Fetch the Billing, Shipping and Contact details information
    def test_11_search_new_order_in_sforce(self):
        print("Case__Seaching_Order_in_Salesforce...")
        
        global return_order, search_order, search_order_sf
        
        print("Customer Order No: ",return_order)
        #print("Searching in Salesforce Order Object....Please..Wait..for..1-min..")
        time.sleep(15)

        search_order_sf= search_order_sforce(self_sf,return_order)
        print(search_order_sf)



    
   #Test Case that Check that the Attributes Response of Both Shopify and Salesforce is Same
    def test_12_checking_both_env_responses_order(self):
        print("Case__Checking for the order details in both the environments Shopify/Salesforce")
        
        verifying_both_env_response_order(search_order, search_order_sf)
        self.assertEqual(search_order, search_order_sf, msg= "the response data in the environment are not same")
        print(f'{return_order} is passed........')
    
    """
if __name__ == "__main__":
    unittest.main()