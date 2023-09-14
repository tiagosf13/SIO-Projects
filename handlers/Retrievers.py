from handlers.DataBaseCoordinator import db_query
from flask import jsonify

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
            # Add other fields as needed
        }
        products.append(product)

    return products
