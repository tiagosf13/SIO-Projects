from handlers.DataBaseCoordinator import db_query
from handlers.Verifiers import is_valid_table_name

def get_orders(username_orders):

    # Secure Query
    query = "SELECT * FROM %s"
    result = db_query(query, (username_orders,))


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
    # Secure Query - Select specific columns
    query = "SELECT id, name, description, price, category, stock FROM products"
    results = db_query(query)
    
    # Fetch all rows in one go and convert to a list of dictionaries
    products = [{
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "category": row[4],
        "stock": row[5]
    } for row in results]
    
    return products

def verify_product_id_exists(id):
    # Secure Query
    query = "SELECT * FROM products WHERE id = %s"
    results = db_query(query, (id,))

    if len(results) == 0:
        return False
    else:
        return True
    

def get_product_by_id(id):
    # Secure Query
    query = "SELECT * FROM products WHERE id = %s"
    results = db_query(query, (id,))


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
    query = "SELECT * FROM reviews WHERE product_id = %s"
    results = db_query(query, (product_id,))

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
    if not is_valid_table_name(username_cart):
        return []

    query = "SELECT * FROM {};".format(username_cart)
    result = db_query(query)

    cart = []

    for element in result:
        if not ((verify_product_id_exists(element[0]) and element[1] > 0 and element[1] <= get_product_by_id(element[0])["stock"])):
            # Secure Query
            if is_valid_table_name(username_cart):
                delete_query = "DELETE FROM {} WHERE product_id = %s;".format(username_cart)
                db_query(delete_query, (element[0],))

        else:
            cart.append({
                "product_id": element[0],
                "quantity": element[1],
                "name": get_product_by_id(element[0])["name"],
                "price": get_product_by_id(element[0])["price"]
            })
    return cart


def get_user_email(id):
    # Secure Query
    query = "SELECT email FROM users WHERE id = %s"
    results = db_query(query, (id,))

    
    if len(results) == 0:
        return None
    else:
        return results[0][0]