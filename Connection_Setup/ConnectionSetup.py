
#-----------------Creating Seperate class for activating the session for Shopify here

import shopify
from simple_salesforce import Salesforce as sf
import os
from dotenv import load_dotenv
import requests
import warnings
from requests.auth import HTTPBasicAuth 

#....loading the dot env for importing the API keys and token from ENV
load_dotenv()

SHOPIFY_SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_PASSWORD = os.getenv('SHOPIFY_API_PASSWORD')

#Saleforce importing credentials
SALESFORCE_USERNAME= os.getenv('SALESFORCE_USERNAME')
SALESFORCE_PASSWORD= os.getenv('SALESFORCE_PASSWORD')
SALESFORCE_TOKEN= os.getenv('SALESFORCE_TOKEN')
def activating_connection():

    # Authenticate the session
    shopify.ShopifyResource.set_site(f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_PASSWORD}@{SHOPIFY_SHOP_NAME}/admin")
   
    #activating SALESFORCE seesion
    
    
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
    #salesforce = sf(username= SALESFORCE_USERNAME, password= SALESFORCE_PASSWORD, security_token= SALESFORCE_TOKEN, domain= 'test')
    salesforce = sf(username= SALESFORCE_USERNAME, password= SALESFORCE_PASSWORD, security_token= SALESFORCE_TOKEN, domain= 'login')
    #print("Salesforce Connection_Established....", salesforce)

    
    #HGFI Credentials
    HGFI_USERNAME= os.getenv('HGFI_USERNAME')
    HGFI_API_PASSWORD= os.getenv('HGFI_API_PASSWORD')
    HGFI_STORE_ID= os.getenv('HGFI_STORE_ID')


    auth=(HGFI_USERNAME,HGFI_API_PASSWORD)
    order_number='23915'
    store_id=HGFI_STORE_ID
    
       
    sf_hgfn={"salesforce":salesforce,"hgfi_auth":auth,"hgfi_store_id":store_id}

    return sf_hgfn


def clear_connection():
    #clearing the session
    shopify.ShopifyResource.clear_session()
    requests.Session().close()
    #print("Connection_Clear...")
    