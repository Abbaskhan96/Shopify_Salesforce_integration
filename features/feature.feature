Feature: Verifying the Fields Data Values of the added Products and orders should be same in Shopify and Salesforce
  
  Scenario: Check that the connection of Shopify and salesforce established successfully or not
    Given Verifying that the test print shopify Store ID and Store name



  Scenario: Verifying that same response fetched for all products from Shopify/Salesforce
    When the products searched in Shopify
    And the same product searched in Salesforce
    Then Check the Product SKU and Product ID are same for the searched product in both environments
  

   
  Scenario: Verify the newly Created Order response in Shopify and Salesforce
    Given New Order Created in Shopify
    When the created Order searched in shopify
    And the same Order searched in Salesforce
    Then check the Billing, shipping and contact details are same for the searched order in both environments



  Scenario: Verifying the last week Order response in Shopify and Salesforce
    Given fetch the order number of last week orders of Shopify
    When all last week Orders searched in shopify
    And the same all last week Orders searched in Salesforce
    Then check the Billing, shipping and contact details of all last week searched order in both environments




 