#import sys

from addding_all_cases_for_behave import *
from behave import given, when , then, fixture, use_fixture



#Test_Case__1
@given('Verifying that the test print shopify Store ID and Store name')
def step_setup_connection(context):
    Check_Connection_established()



#Test_Case__2
@when('the products searched in Shopify')
def step_searched_product_in_Shopify(context):
    Searched_Product_in_Shopify()


#Test_Case__3
@when('the same product searched in Salesforce')
def step_searched_product_in_salesforce(context):
    Searched_Product_in_Salesforce()



#Test_Case__4
@then('Check the Product SKU and Product ID are same for the searched product in both environments')
def step_verifying_product_values_Shopify_salesforce(context):
    Check_Product_Values_in_Shopify_Salesforce()


#------------------------------------------------------------------------------------------------------------------------------

#Test_Case__5
@given('New Order Created in Shopify')
def step_create_order_Shopify(context):
    Create_Order_in_Shopify()


#Test_Case__6
@when('the created Order searched in shopify')
def step_searched_order_Shopify(context):
    Searched_Order_in_Shopify()



#Test_Case__7
@when('the same Order searched in Salesforce')
def step_searched_order_salesforce(context):
    Searched_Order_in_Salesforce()



#Test_Case__8
@then('check the Billing, shipping and contact details are same for the searched order in both environments')
def step_verifying_order_values_Shopify_salesforce(context):
    Check_Order_Values_in_Shopify_Salesforce()


#-----------------------------------------------------------------------------------------------------------------------------

#Test_Case_9
@given('fetch the order number of last week orders of Shopify')
def step_fetch_last_week_order_numbers(context):
    fetch_last_week_orders_numbers()



#Test_Case_10
@when('all last week Orders searched in shopify')
def step_search_last_week_orders_shopify(context):
    search_last_week_orders_shopify()



#Test_Case_11
@when('the same all last week Orders searched in Salesforce')
def step_search_last_week_orders_sforce(context):
    search_last_week_orders_sforce()


#Test_CAse_12
@then('check the Billing, shipping and contact details of all last week searched order in both environments')
def step_check_last_week_orders_response_both_env(context):
    check_last_week_orders_response_both_env()
