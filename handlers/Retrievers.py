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
