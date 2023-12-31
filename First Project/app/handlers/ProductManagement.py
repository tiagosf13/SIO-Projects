import random, os, json
from datetime import datetime
from handlers.Retrievers import get_product_by_id
from handlers.DataBaseCoordinator import db_query


def verify_id_exists(id, table):
    # Secure Query
    #query = "SELECT * FROM %s WHERE id= %s"
    #results = db_query(query, (table, id,))

    query = "SELECT * FROM " + table + " WHERE id=" + str(id)
    results = db_query(query)

    if len(results) == 0:
        return False
    else:
        return True

def generate_random_product_id(table):
    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while verify_id_exists(random_id, table):
        random_id = random.randint(100000, 999999)

    return random_id


def create_product_image(id, product_photo):
    # Get the current working directory
    directory = os.getcwd()

    # Define the path for the user's directory
    user_directory = os.path.join(directory, "catalog")

    # Create the user's directory and any missing parent directories
    os.makedirs(user_directory, exist_ok=True)

    if os.path.exists(os.path.join(user_directory, f"{id}.png")):
        os.remove(os.path.join(user_directory, f"{id}.png"))
    # Save the product photo
    product_photo.save(os.path.join(user_directory, f"{id}.png"))


def create_product(product_name, product_description, product_price, product_category, product_quantity, product_photo):
    # Generate a unique user id
    id = str(generate_random_product_id("products"))
    
    # Add the user to the USER table
    # Secure Query
    # db_query("INSERT INTO products (id, name, description, price, category, stock) VALUES (%s, %s, %s, %s, %s, %s);",
    #         (id, product_name, product_description, product_price, product_category, product_quantity)
    # )

    query = "INSERT INTO products (id, name, description, price, category, stock) VALUES ("+str(id)+",'"+str(product_name)+"','"+str(product_description)+"',"+str(product_price)+",'"+str(product_category)+"',"+str(product_quantity)+")"
    db_query(query)
    # Create a folder for the user
    create_product_image(id, product_photo)

    # Return the created user
    return id


def remove_product(id):
    # Secure Query
    # query = "DELETE FROM products WHERE id = %s"
    # db_query(query, (id,))

    query = "DELETE FROM products WHERE id="+str(id)
    db_query(query)

    # Get the current working directory
    directory = os.getcwd()

    # Define the path for the user's directory
    user_directory = os.path.join(directory, "catalog")

    # Create the user's directory and any missing parent directories
    if os.path.exists(os.path.join(user_directory, f"{id}.png")):
        os.remove(os.path.join(user_directory, f"{id}.png"))

    return True


def update_product_name(id, name):
    # Secure Query
    # query = "UPDATE products SET name = %s WHERE id = %s"
    # db_query(query, (name, id))

    query = "UPDATE products SET name='"+name+"' WHERE id="+str(id)
    db_query(query)
    return True


def update_product_description(id, description):
    # Secure Query
    # query = "UPDATE products SET description = %s WHERE id = %s"
    # db_query(query, (description, id))

    query = "UPDATE products SET description='"+description+"' WHERE id="+str(id)
    db_query(query)
    return True


def update_product_price(id, price):
    # Secure Query
    # query = "UPDATE products SET price = %s WHERE id = %s"
    # db_query(query, (price, id))

    query = "UPDATE products SET price="+price+" WHERE id="+str(id)
    db_query(query)
    return True


def update_product_category(id, category):
    
    # Secure Query
    # query = "UPDATE products SET category = %s WHERE id = %s"
    # db_query(query, (category, id))

    query = "UPDATE products SET category='"+category+"' WHERE id="+str(id)
    db_query(query)
    return True


def update_product_quantity(id, quantity):
    # Secure Query
    # query = "UPDATE products SET stock = %s WHERE id = %s"
    # db_query(query, (quantity, id))

    query = "UPDATE products SET stock="+str(quantity)+" WHERE id="+str(id)
    db_query(query)
    return True


def create_review(id, user_id, review, rating):
    review_id = str(generate_random_product_id("reviews"))

    # Secure Query
    # query = "INSERT INTO reviews (id, product_id, user_id, rating, review) VALUES (%s, %s, %s, %s, %s);"
    # db_query(query, (review_id, id, user_id, rating, review))

    query = "INSERT INTO reviews (id, product_id, user_id, rating, review) VALUES ("+review_id+","+str(id)+","+str(user_id)+","+str(rating)+",'"+str(review)+"');"
    db_query(query)
    return True


def set_cart_item(table_name, product_id, quantity, operation):

    #check if the product is already in the cart
    # Secure Query
    # query = "SELECT * FROM %s WHERE product_id = %s"
    # results = db_query(query,(table_name, product_id,))
    
    query = "SELECT * FROM "+table_name+" WHERE product_id = "+str(product_id)
    results = db_query(query)
    if operation == "remove" and len(results) == 0:
        return False

    if len(results) != 0:
        #update the quantity
        if operation == "add":
            # Secure Query
            # query = "UPDATE %s SET quantity = quantity + %s WHERE product_id = %s"
            query = "UPDATE "+table_name+" SET quantity = quantity + "+str(quantity)+" WHERE product_id = "+str(product_id)
        else:
            # Secure Query
            # query = "UPDATE %s SET quantity = quantity - %s WHERE product_id = %s"
            query = "UPDATE "+table_name+" SET quantity = quantity - "+str(quantity)+" WHERE product_id = "+str(product_id)
        # Secure Query
        #db_query(query, (table_name, quantity, product_id))
        db_query(query)
        return True
    else:
        #add the product to the cart
        # Secure Query
        # query = "INSERT INTO %s (product_id,quantity) VALUES (%s,%s);"
        # db_query(query, (table_name, product_id, quantity))
        query = "INSERT INTO "+table_name+" (product_id, quantity) VALUES ("+str(product_id)+","+str(quantity)+");"
        db_query(query)
        return True


def register_order(username, user_id, order_details, products):

    products_to_register = {}
    total_price = 0
    for product in products:
        total_price += float(product["price"]) * product["quantity"]
        products_to_register[product["product_id"]] = product["quantity"]

    order_id = str(generate_random_product_id("all_orders"))
    time = datetime.now().strftime("%d-%m-%Y %H:%M")
    # register in all orders
    # Secure Query
    # query = "INSERT INTO all_orders (id, user_id, order_date) VALUES (%s, %s, %s);"
    #db_query(query, (order_id, user_id, time))
    query = "INSERT INTO all_orders (id, user_id, order_date) VALUES ("+order_id+","+user_id+",'"+str(time)+"');"
    db_query(query)

    # Secure Query
    # query = "INSERT INTO %s_orders (id, products, total_price, shipping_address, order_date) VALUES (%s, %s, %s, %s, %s);"
    # db_query(query, (username, order_id, json.dumps(products_to_register), total_price, order_details["shipping_address"], time))
    
    query = "INSERT INTO "+username+"_orders (id, products, total_price, shipping_address, order_date) VALUES ("+order_id+",'"+str(json.dumps(products_to_register))+"',"+str(total_price)+",'"+order_details["shipping_address"]+"','"+str(time)+"');"
    db_query(query)
    return True, order_id

def update_product_after_order(products):

    for product in products:
        product_stock = get_product_by_id(product["product_id"])["stock"]
        quantity = product["quantity"]
        if product_stock < quantity:
            return False
        # update the product quantity
        update_product_quantity(product["product_id"], product_stock - quantity)
    return True