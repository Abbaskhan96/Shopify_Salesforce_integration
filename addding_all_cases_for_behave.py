import sys
sys.path += ['./Connection_Setup/','./ShopifyCases/','./SalesForceCases']

from testConnection import *
from shopify_functions import *
from SF_functions import *
from testCases import *

def Check_Connection_established():
    Test1= test_01_connection_established()



def sSearched_Product_in_Shopify():
    Test2= Test_Cases()
    Test2.test_02_search_product_shopify()



def Searched_Product_in_Salesforce():
    Test3= Test_Cases()
    Test3.setUp()
    Test3.test_03_search_product_salesforce()



def Check_Product_Values_in_Shopify_Salesforce():
    Test4= Test_Cases()
    Test4.setUp()
    Test4.test_04_checking_both_env_responses_product()


#------------------------------------------------------------------{Last=Week}---O-R-D-E-R-S----------------------

def fetch_last_week_orders_numbers():
    Test5= Test_Cases()
    Test5.setUp()
    Test5.test_05_save_last_week_orders_number()


def search_last_week_orders_shopify():
    Test6= Test_Cases()
    Test6.setUp()
    Test6.test_06_search_last_week_orders_shopify()

def search_last_week_orders_sforce():
    Test7= Test_Cases()
    Test7.setUp()
    Test7.test_07_search_last_week_orders_sforce()



def check_last_week_orders_response_both_env():
    Test8 = Test_Cases()
    Test8.setUp()
    Test8.test_08_check_last_week_orders_response_both_env()

#----------------------------------------------------------------{New-Created-Orders}-----------------------------
def Create_Order_in_Shopify():
    Test9= Test_Cases()
    Test9.setUp()
    Test9.test_09_creating_searching_order_shopify()



def Searched_Order_in_Shopify():
    Test10= Test_Cases()
    Test10.setUp()
    Test10.test_10_search_new_order_in_shopify()



def Searched_Order_in_Salesforce():
    Test11= Test_Cases()
    Test11.setUp()
    Test11.test_11_search_new_order_in_sforce()



def Check_Order_Values_in_Shopify_Salesforce():
    Test12= Test_Cases()
    Test12.setUp()
    Test12.test_12_checking_both_env_responses_order()
