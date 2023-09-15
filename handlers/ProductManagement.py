import random, os, shutil
from handlers.DataBaseCoordinator import db_query

def verify_product_id_exists(id):
    query = "SELECT * FROM products WHERE id = %s"
    results = db_query(query, (id,))

    if len(results) == 0:
        return False
    else:
        return True

def generate_random_product_id():
    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while verify_product_id_exists(random_id):
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
    id = str(generate_random_product_id())
    
    # Add the user to the USER table
    db_query("INSERT INTO products (id, name, description, price, category, stock) VALUES (%s, %s, %s, %s, %s, %s);",
            (id, product_name, product_description, product_price, product_category, product_quantity)
    )

    # Create a folder for the user
    create_product_image(id, product_photo)

    # Return the created user
    return id


def remove_product(id):

    query = "DELETE FROM products WHERE id = %s"
    db_query(query, (id,))

    # Get the current working directory
    directory = os.getcwd()

    # Define the path for the user's directory
    user_directory = os.path.join(directory, "catalog")

    # Create the user's directory and any missing parent directories
    os.remove(os.path.join(user_directory, f"{id}.png"))

    return True


def update_product_name(id, name):

    query = "UPDATE products SET name = %s WHERE id = %s"
    db_query(query, (name, id))
    return True


def update_product_description(id, description):

    query = "UPDATE products SET description = %s WHERE id = %s"
    db_query(query, (description, id))
    return True


def update_product_price(id, price):

    query = "UPDATE products SET price = %s WHERE id = %s"
    db_query(query, (price, id))
    return True


def update_product_category(id, category):
    
    query = "UPDATE products SET category = %s WHERE id = %s"
    db_query(query, (category, id))
    return True


def update_product_quantity(id, quantity):

    query = "UPDATE products SET stock = %s WHERE id = %s"
    db_query(query, (quantity, id))
    return True
