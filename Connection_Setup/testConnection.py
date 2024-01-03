
import shopify
import unittest
from  ConnectionSetup import * 
from simple_salesforce import Salesforce as sf

#======Conenection Test Class------------------

class ConnectionTest(unittest.TestCase):
    
    def setUp(self):
        #---calling function from setup_session.py to activate the session in setUp fixture
        activating_connection()
       
    def tearDown(self):
         #---calling function from setup_session.py to clear the session in tearDown fixture
        session_clear=clear_connection()
        #checking that our connection is closed or not
        self.assertIsNone(session_clear)

    def test_connection_established(self):
        # Check if the connection is established in the setUp method
        shop=shopify.Shop.current()
        self.assertIsNotNone(shop)
        self.assertIsNotNone(sf)

        """
        #print(f"Shop ID: {shop.id}", f"\t\t\tshop Name: {shop.name}")
        products= shopify.Product.find(title="American Beautyberry Shrub", status="active")
        #print(products)
        for product in products:
            metafield= product.metafields()
            for metafield in metafield:
                print(metafield.key, metafield.value)
        
        """

def setup_connection():

    connection_test = ConnectionTest()
    connection_test.setUp()

def teardown_connection():

    connection_test = ConnectionTest()
    connection_test.tearDown()


def test_01_connection_established():

    connection_test = ConnectionTest()
    connection_test.test_connection_established()


if __name__ == "__main__":
    unittest.main()
