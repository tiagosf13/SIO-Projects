from handlers.DataBaseCoordinator import db_query

def get_all_products():
    query = "SELECT * FROM products"
    results = db_query(query)  # Assuming db_query returns a list of rows

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
    query = "SELECT * FROM products WHERE id = %s"
    results = db_query(query, (id,))

    if len(results) == 0:
        return False
    else:
        return True
    

def get_product_by_id(id):

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
