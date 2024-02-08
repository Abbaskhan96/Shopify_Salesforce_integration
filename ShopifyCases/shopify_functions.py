import shopify
from datetime import datetime, timedelta
#from testCases import *
 
multi_variants_SKU={}
variants_more_than_1=[]

#Compressing the product names to list..

def product_adding_to_list():
    
    with open("C:/Users/Abbas Khan/source/repos/shopify_proj/ShopifyCases/product_names.txt", "r") as f:
        lines = [product_names.strip() for product_names in f.readlines()]
    return lines


#Compressing the order numbers to list

def order_adding_to_list():
    
    with open("C:/Users/Muhammad Abbas Khan/source/repos/shopify_proj/ShopifyCases/customer_order_numbers.txt", "r") as f:
        lines = [order_num.strip() for order_num in f.readlines()]
    return lines


#Searching Products in Shopify..,.

def search_products():
    product_names = product_adding_to_list()

    #titles = [for name in product_names]
    product_dict = {}
    field={}

    for title in product_names:
       # print("title", title)
        products = shopify.Product.find(title=title, status='active')
        for product in products:
            
            if len(product.variants)>1:
                global variants_more_than_1, multi_variants_SKU
                #variants_more_than_1=[]
                

                variants_more_than_1.append(product.title)
                sku_names=[var.sku for var in product.variants]
                multi_variants_SKU.update({product.title:sku_names})
                    #multi_variants_SKU.append(var.sku)
            
            for variant in product.variants:
                sku = variant.sku
                product_id= str(product.id)
                product_dict[product.title] = {"SKU": sku, "product_id": product_id}
                #print(product_dict)
            metafields= product.metafields()
            for metafield in metafields:
                if metafield.key in ["light_conditions","soil_moisture","plant_type","flower_colour","soil_type","animal_resistant",
                                     "bloom_type","wildlife_benefits","plant_height","plants_in_this_collection"]:

                    if (product.title in field):
                        if metafield.key == "plants_in_this_collection":
                            updated_value=metafield.value
                            # Remove square brackets and split by comma
                            metaobject_ids = updated_value.strip("[]").split(",")
                            
                            # Extract numeric IDs
                            numeric_ids = [(metaobject_id.strip("\"").split("/")[-1]) for metaobject_id in metaobject_ids]
                            
                            #changing the values
                            metafield.value=str([numeric_id for numeric_id in numeric_ids])
                        field[product.title][metafield.key]=metafield.value

                    else:
                        field[product.title]={metafield.key:metafield.value}


                    #print(field)
                    product_dict[product.title].update({"metafields": field[product.title]})
                    #print(product_dict)
                    #print("\n\n")

            empty_keys_to_delete=[]
            #print("test test test...")
            #all_check_empty=[x for x in product_dict[product.title]['metafields'].values()]
            #if all(not sublist for sublist in all_check_empty):
            #    print("All elements are empty lists")
            #    return product_dict
            #else:
           # print(product_dict)
           # print("\n")
            for key, value in product_dict[product.title]["metafields"].items():
                if value=='[]':
                    empty_keys_to_delete.append(key)
            for i in empty_keys_to_delete: 
                del product_dict[product.title]["metafields"][i]

            print(product.title)
                    
    return product_dict


#Check that the product exists or not 

def product_order_exist_result(returned_products_dict, provided_products_list):
    returned_products_list= [name for name in returned_products_dict]
        #print(dict_list)

    for names in provided_products_list:
        if names not in returned_products_list:
            print(f"{names} does not exists ")
            return names



def multi_variant_products():
    pass

#==============================================| O R D E R S |=============================================================================|||


# Keeping mind that for every existing customer order the Billing First Name, Last Name is selected as Shipping First Name Last name in Salesforce
# Sandbox
# & in shopify when new customer created with unique email his customer first name, last name will be duplicate from Billing First Name, Last Name
# However when the same customer create another order his customer first name, last name will be selected aw provided in JSON data payload



#Data for creating order 

data = {
  "email": "abbas.khan@codup.co",
  "line_items": [
    {
      "variant_id": 44250104234216,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "first_name": "Abbas",
    "last_name": "khan",
    "address1": "123 Main Street",
    "city": "City-PA",
    "province": "PA",
    "country": "US",
    "zip": "15001",
    "phone": "555-555-5555"
  },
  # Add the customer first name and last name separately from the billing address
  "customer_first_name": "Abbas",
  "customer_last_name": "Khan"
}



order_list=[]     
order_info_shopify={}
payment_non_exists_id={}

#Define a function to create order than search the same order number with search_order_shopify
def create_order(data):
  
  # Create a dictionary to store the billing and shipping information
  order_info = {}

  #---- Create the order for different Billing and shipping details

  order = shopify.Order()
  # Set the order attributes from the data
  order.email = data["email"]
  order.line_items = data["line_items"]
  
  order.billing_address = data["shipping_address"]
  
  order.shipping_address = data["shipping_address"]
  # Create a new customer object
  customer = shopify.Customer()
  # Set the customer attributes from the data
  customer.first_name = data["customer_first_name"]
  customer.last_name = data["customer_last_name"]
  customer.email = data["email"]
  # Save the customer to Shopify
  customer.save()
  # Assign the customer to the order
  order.customer = customer
  # Save the order to Shopify
  order.save()
  #print(order_response)
  #return the order list
  return order.order_number


# Define a function to search an order in Shopify by order number and fetch the billing and shipping details
def search_order_shopify(order_number):
  global order_info_shopify, payment_non_exists_id
  #creating dictionary to store respomse
  
  order = shopify.Order.find(name= order_number)
  #print(order)
  # Check if the order exists
  if order:
    
    for order in order:
        
        # Get the billing address
        billing_address = order.billing_address
        # Get the shipping address
        o= order.to_dict()
        #print(o["shipping_address"])
       # print(order.shipping_address)
        if not 'Rise.ai' in order.tags:
            shipping_address = order.shipping_address

        customer_first_name= order.customer.first_name
        customer_last_name= order.customer.last_name
        #print("Customer Name: ", customer_first_name+ " "+customer_last_name)
        customer_email= order.customer.email
        # Add the billing and shipping information to the dictionary
        billing = {
          "name": billing_address.name,
          "address1": billing_address.address1,
          "city": billing_address.city,
          "country": billing_address.country,
          "zip": billing_address.zip,
          "phone": billing_address.phone,
          "state": billing_address.province
        }
        if not "Rise.ai" in order.tags:
            shipping = {
              "name": shipping_address.name,
              "address1": shipping_address.address1,
              "city": shipping_address.city,
              "country": shipping_address.country,
              "zip": shipping_address.zip,
              "phone": shipping_address.phone,
              "state": shipping_address.province
            }
        contact={
            "Customer Name":customer_first_name+" "+customer_last_name,
            "Customer Email": customer_email
            }
        #adding values in dictionary with the order_number keyword
        if not 'Rise.ai' in order.tags:
            #order_info_shopify[str(order.order_number)]= {"Billing": billing, "Shipping": shipping, "Contact": contact}
            order_info_shopify[str(order.order_number)]= {"Shipping": shipping, "Contact": contact}
        else:
            #order_info_shopify[str(order.order_number)]= {"Billing": billing, "Contact": contact}
            order_info_shopify[str(order.order_number)]= {"Contact": contact}
        #print(order_info_shopify,"\n\n")

        transaction= order.transactions()
        
        if len(transaction)!=0:
            for idx,transaction in enumerate(transaction):
                
                try:
                    credit_card_company= order.payment_details.to_dict()
                    #print(credit_card_company)
               
                    if 'metadata' in transaction.receipt.to_dict(): 
                        # for Visa/Mastercard payments
                        receipt= transaction.receipt.to_dict()
                       # print(transaction.to_dict())
                        payment_id= receipt["metadata"]["order_id"]
                        #payment_id= (receipt["metadata"]["order_id"] if 'metadata' in receipt else print("a"))
                        #print("the payment ID is:----", payment_id)
                    
                        transaction_order_price_details= transaction_fields(transaction, order)
                        transaction_order_price_details["payment_id"]= str(payment_id)
                        order_price= order_price_details(transaction, order)

                        #print(transaction)
                        order_info_shopify[str(order.order_number)].update(
                            {f"transaction{idx+1}": transaction_order_price_details})

                        order_info_shopify[str(order.order_number)].update(
                            {"Order_Price_details": order_price})

                    #if transaction.gateway == 'paypal' or ('paypal' in order.payment_gateway_names):
               
                    elif (('paypal' in order.payment_gateway_names)
                       or ('Visa' in credit_card_company["credit_card_company"])
                       or ('Mastercard' in credit_card_company["credit_card_company"])
                       or ('American Express' in credit_card_company["credit_card_company"])):
                        # for Paypal payments
                        checkout_id= str(order.checkout_id)

                        #print("Payment id is: ","c"+checkout_id+"."+f"{idx+1}")
                        payment_id= ("c"+checkout_id+"."+f"{idx+1}" if idx != 0 else "c"+checkout_id+"."+f"{idx+1}")
                        
                        transaction_order_price_details= transaction_fields(transaction, order)
                        transaction_order_price_details["payment_id"]= str(payment_id)
    
                        order_price = order_price_details(transaction, order)


                        #print(transaction)
                        order_info_shopify[str(order.order_number)].update(
                        {f"transaction{idx+1}": transaction_order_price_details})

                        order_info_shopify[str(order.order_number)].update(
                        {"Order_Price_details": order_price})

                    
                    else:
                        
                        transaction_order_price_details= transaction_fields(transaction, order)
                        order_price= order_price_details(transaction, order)

                        #print(transaction)
                        order_info_shopify[str(order.order_number)].update(
                            {f"transaction{idx+1}": transaction_order_price_details})

                        order_info_shopify[str(order.order_number)].update(
                            {"Order_Price_details": order_price})



                except:
                     transaction_order_price_details= transaction_fields(transaction, order)
                     order_price= order_price_details(transaction, order)   
                     
                     if 'metadata' in transaction.receipt.to_dict():
                        receipt= transaction.receipt.to_dict()
                        payment_id= receipt["metadata"]["order_id"]
                        #payment_id= (receipt["metadata"]["order_id"] if 'metadata' in receipt else print("a"))
                        #print("the payment ID is:----", payment_id)
                    
                        transaction_order_price_details= transaction_fields(transaction, order)
                        transaction_order_price_details["payment_id"]= str(payment_id)
                        order_price= order_price_details(transaction, order)


                     elif 'paypal' in order.payment_gateway_names:
                        checkout_id= str(order.checkout_id)

                        #print("Payment id is: ","c"+checkout_id+"."+f"{idx+1}")
                        payment_id= ("c"+checkout_id+"."+f"{idx+1}" if idx != 0 else "c"+checkout_id+"."+f"{idx+1}")
                        #print(payment_id)
                        
                        transaction_order_price_details= transaction_fields(transaction, order)
                        transaction_order_price_details["payment_id"]= str(payment_id)
                        order_price= order_price_details(transaction, order)

                        #print(transaction)
                        order_info_shopify[str(order.order_number)].update(
                            {f"transaction{idx+1}": transaction_order_price_details})

                        order_info_shopify[str(order.order_number)].update(
                            {"Order_Price_details": order_price})


                     else:  
                        transaction_order_price_details= transaction_fields(transaction, order)
                        order_price= order_price_details(transaction, order)
                     
                     #print(transaction)
                     order_info_shopify[str(order.order_number)].update(
                     {f"transaction{idx+1}": transaction_order_price_details})

                     order_info_shopify[str(order.order_number)].update(
                     {"Order_Price_details": order_price})

        else:
            order_price= order_price_details(transaction, order)
            order_info_shopify[str(order.order_number)].update(
            {f'Order_Price_details': order_price})


    
    payment_non_exists_id= order_info_shopify
    #print(payment_non_exists_id)
    #print(payment_non_exists_id['22916']["transaction2"]["payment_id"])

    return order_info_shopify
  else:
    # Return None if the order does not exist
    return "Order Not Found..."



def order_price_details(transaction, order):
    #Fetching the order_price_details----
    subtotal_price= order.total_line_items_price
    #if (('Rise.ai' not in order.tags) or ('is_replacement_order' not in order.tags)):
    if len(order.shipping_lines)!=0:
        shipping_price= order.shipping_lines[0].price

    total_discounts= order.total_discounts
    total_price= order.total_price

    if not len(order.discount_codes) == 0:
        discount= order.discount_codes[0].to_dict()
        #print(discount)
        coupon_code= (discount["code"] if 'code' in discount else "None")

    else:
        coupon_code= "None"

    #if ('Rise.ai' or 'is_replacement_order') not in order.tags:
    if len(order.shipping_lines)!=0:
        order_price={
            "total_line_items_price": subtotal_price,
            "shipping_price": shipping_price,
            "total_discount": total_discounts,
            "total_price": total_price,
            "coupon_code": coupon_code
            }
    else:
        order_price={
            "total_line_items_price": subtotal_price,
            "total_discount": total_discounts,
            "total_price": total_price,
            "coupon_code": coupon_code
            }

    if 'donation' in order.tags:
        order_price['total_price']="0.00"

    return order_price
    


def transaction_fields(transaction, order):
    order_id= transaction.order_id
    gateway= transaction.gateway
    status= transaction.status
    type= transaction.kind
    amount= transaction.amount
    created_date= transaction.created_at
 
   

    transaction_details={"order_id": str(order_id),
                        "gateway": gateway,
                        "type": type,
                        "amount": amount,
                        "status": status}

    return transaction_details
    

#Fetching the Last week order numbers and writing them on last_week_orders.txt file
def last_week_orders():
    #calculate the start and end date of the last week
    global order_info_shopify
    end_date= datetime.now()
    start_date= end_date - timedelta(weeks=1)

    #format the dates as strings
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S%z')
    #print(end_date_str, start_date_str)

    last_week_orders= shopify.Order.find(created_at_min= start_date_str, created_at_max= end_date_str)
    #print(last_week_orders)

    
    #saving the order numbers in txt file
    with open("C:/Users/Abbas Khan/source/repos/shopify_proj/ShopifyCases/last_week_orders.txt", 'w') as f:
        for order in last_week_orders:
            f.write(f'{order.order_number}\n')
    

    with open("C:/Users/Abbas Khan/source/repos/shopify_proj/ShopifyCases/last_week_orders.txt", "r") as f:
        lines = [order_num.strip() for order_num in f.readlines()]

    return lines


def defined_order_for_searching():
    with open("C:/Users/Abbas Khan/source/repos/shopify_proj/ShopifyCases/orders_to_be_searched.txt", "r") as f:
        lines = [order_num.strip() for order_num in f.readlines()]

    return lines



 