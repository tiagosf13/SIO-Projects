from handlers.DataBaseCoordinator import db_query

def get_orders(username_orders):

    # Secure Query
    #query = "SELECT * FROM %s"
    #result = db_query(query, (username_orders,))

    query = "SELECT * FROM " + username_orders
    result = db_query(query)

    orders = {}

    for element in result:
        current_order_id = element[2]

        if current_order_id not in orders:
            orders[current_order_id] = []
        else:
            orders[current_order_id].append({
                "product_id": element[0],
                "quantity": element[1],
                "name" : get_product_by_id(element[0])["name"],
                "price" : get_product_by_id(element[0])["price"]
            })
    return orders


def get_all_products():

    # Secure Query
    query = "SELECT * FROM products"
    results = db_query(query)

    products = []
    for row in results:
        product = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "category": row[4],
            "stock": row[5]
        }
        products.append(product)

    return products

def verify_product_id_exists(id):
    # Secure Query
    #query = "SELECT * FROM products WHERE id = %s"
    #results = db_query(query, (id,))

    query = "SELECT * FROM products WHERE id = "+str(id)
    results = db_query(query)

    if len(results) == 0:
        return False
    else:
        return True
    

def get_product_by_id(id):
    # Secure Query
    #query = "SELECT * FROM products WHERE id = %s"
    #results = db_query(query, (id,))

    query = "SELECT * FROM products WHERE id = "+str(id)
    results = db_query(query)

    if len(results) == 0:
        return None
    else:
        row = results[0]
        product = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "category": row[4],
            "stock": row[5]
        }
        return product
    

def get_product_reviews(product_id):

    # check if the product exists
    if not verify_product_id_exists(product_id):
        return None

    # Secure Query
    #query = "SELECT * FROM reviews WHERE product_id = %s"
    #results = db_query(query, (product_id,))

    query = "SELECT * FROM reviews WHERE product_id = "+str(product_id)

    results = db_query(query)
    reviews = []
    for row in results:
        review = {
            "review_id": row[0],
            "product_id": row[1],
            "user_id": row[2],
            "rating": row[3],
            "review": row[4]
        }
        reviews.append(review)

    return reviews


def get_cart(username_cart):
    # Secure Query
    # query = "SELECT * FROM %s"
    # result = db_query(query, (username_cart,))

    query = "SELECT * FROM " + username_cart
    result = db_query(query)

    cart = []

    for element in result:
        if not verify_product_id_exists(element[0]):

            # Secure Query
            # query = "DELETE FROM %s WHERE product_id = %s"
            # db_query(query, (username_cart, element[0]))

            query = "DELETE FROM " + username_cart + " WHERE product_id = " + element[0]
            db_query(query)
        else:
            cart.append({
                "product_id": element[0],
                "quantity": element[1],
                "name" : get_product_by_id(element[0])["name"],
                "price" : get_product_by_id(element[0])["price"]
            })
    return cart


def get_user_email(id):
    # Secure Query
    # query = "SELECT email FROM users WHERE id = %s"
    #results = db_query(query, (id,))

    query = "SELECT email FROM users WHERE id = "+str(id)
    results = db_query(query)
    
    if len(results) == 0:
        return None
    else:
        return results[0][0]