import os, random, shutil
from flask import render_template_string
from string import ascii_uppercase, ascii_lowercase
from handlers.EmailHandler import send_email
from handlers.DataBaseCoordinator import db_query
from handlers.ProductManagement import get_product_by_id
from handlers.Verifiers import is_valid_table_name, is_valid_input



def search_user_by_username(username):

    # Secure Query
    query = "SELECT * FROM users WHERE username = %s"
    result = db_query(query, (username,))


    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]


def search_user_by_email(email):

    # Secure Query
    query = "SELECT * FROM users WHERE email = %s"
    result = db_query(query, (email,))


    # If no user is found, return None
    if not result:

        return None

    # Return the user data
    return result[0][1]


def validate_login(username, password):

    # If username is None, return False (user not found)
    if username is None:
        return False
    else:
        
        # Fetch the user's password
        # Secure Query
        query = "SELECT password FROM users WHERE username = %s"
        result = db_query(query, (username,))


        # Check if there is a password
        if not result:
            return None
        
        # Check if the provided password matches the user's password
        if result[0][0] == password:

            # Return True to indicate the login has been validated
            return True

        else:
            # Return False to indicate the login credentials aren't valid
            return False
        

def get_id_by_username(username):
    # Construct the SQL query
    # Secure Query
    query = "SELECT id FROM users WHERE username = %s"
    result = db_query(query, (username,))


    # Check if 
    if result:
        return str(result[0][0])
    else:
        return None
    

def generate_password(length):

    code = ''

    # Generate a random password
    for i in range(length):
        code += random.choice(ascii_uppercase + ascii_lowercase + '0123456789')

    return code

def send_recovery_password(email):


    # Search for the user with the given email
    user = search_user_by_email(email)
    id = get_id_by_username(user)

    # If user is None, return False (user not found)
    if user is None:

        return False
    else:

        # Extract the username and password from the user
        name = user
        password = generate_password(15)
        change_password(id, password)

        # Build the HTML body
        HTMLBody = f"""
            <html>
            <head>
                <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    color: #333;
                }}
                h1 {{
                    color: #007bff;
                }}
                p {{
                    margin-bottom: 10px;
                }}
                </style>
            </head>
            <body>
                <h1>Recover Password</h1>
                <p>Hello, {name}</p>
                <p>Your new password is: <strong>{password}</strong></p>
            </body>
            </html>
        """

        # Send the recovery email to the user
        send_email(email, "Recover your password", HTMLBody)

        # Return True to indicate the email was sent successfully
        return True
    

def check_id_existence(id):
    # Secure Query
    query = "SELECT EXISTS(SELECT 1 FROM users WHERE id = %s);"
    result = db_query(query, (id,))


    return result[0][0]


def check_order_id_existence(id):
    # Secure Query
    query = "SELECT EXISTS(SELECT 1 FROM all_orders WHERE id = %s);"
    result = db_query(query, (id,))

    return result[0][0]


def generate_random_id():
    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while check_id_existence(random_id):
        random_id = random.randint(100000, 999999)

    return random_id


def create_user_folder(id):
    # Get the current working directory
    directory = os.getcwd()

    # Define the path for the user's directory
    user_directory = os.path.join(directory, "database", "accounts")

    # Set the paths for the source and destination files
    src_path = os.path.join(directory, "static", "images", "default.png")
    dst_path = os.path.join(user_directory, f"{id}.png")

    # Copy the source file to the destination file
    shutil.copy(src_path, dst_path)



def create_user(username, password, email):
    # Generate a unique user id
    id = str(generate_random_id())
    
    # Add the user to the USER table
    # Secure Query
    query = "INSERT INTO users (id, username, password, email, admin) VALUES (%s, %s, %s, %s, %s);"
    db_query(query, (id, username, password, email, False))


    # Create a folder for the user
    create_user_folder(id)

    # Return the created user
    return id


def change_password(id, password):

    # Build the query to update the password in the user's table
    # Secure Query
    query = 'UPDATE users SET password = %s WHERE id = %s'
    db_query(query, (password, id))


def update_username(id, new_username):

    # Get the old username based on the ID
    old_username = search_user_by_id(id)[1]
    
    # Construct the SQL query
    # Secure Query
    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s);"
    result = db_query(query, (old_username+"_cart",))


    if result[0][0]:

        # Build the query to alterate the statement username's table
        # Secure Query
        query = "ALTER TABLE %s RENAME TO %s;"
        db_query(query, (old_username.lower()+"_cart", new_username.lower()+"_cart"))


    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s);"
    result = db_query(query, (old_username+"_orders",))
    
    if result[0][0]:

        # Build the query to alterate the statement username's table
        # Secure Query
        query = "ALTER TABLE %s RENAME TO %s;"
        db_query(query, (old_username.lower()+"_orders", new_username.lower()+"_orders"))


    # Build the query to update the username in the user's table
    # Secure Query
    query = "UPDATE users SET username = %s WHERE id = %s"
    db_query(query, (new_username, id))


def search_user_by_id(id):

    # Construct the SQL query
    # Secure Query
    query = "SELECT * FROM users WHERE id = %s"
    result = db_query(query, (id,))


    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]


def update_email(id, email):

    # Verify if the email is valid
    if not is_valid_input(email):
        return False

    # Build the query to update the email in the user's table
    # Secure Query
    query = "UPDATE users SET email = %s WHERE id = %s"
    db_query(query, (email, id))


def update_password(id, password):

    # Build the query to update the password in the user's table
    # Secure Query
    query = "UPDATE users SET password = %s WHERE id = %s"
    db_query(query, (password, id))


def get_username_by_id(id):
    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT username FROM users WHERE id = %s"
    result = db_query(query, (id,))

    # Check if the username was found
    if result:

        # If it was, return the username
        return result[0][0]

    else:

        # If it wasn't return None
        return None
    

def get_user_role(id):

    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT admin FROM users WHERE id = %s"
    result = db_query(query, (id,))

    # Check if the username was found
    if result:

        # If it was, return the username
        return result[0][0]

    else:

        # If it wasn't return None
        return None


def compose_email_body(products, order_id):
    # Read the HTML and CSS files
    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

    with open(current_directory + '/templates/email_order.html', 'r', encoding='utf8') as html_file:
        email_template = html_file.read()

    with open(current_directory + '/static/css/email_order.css', 'r', encoding='utf8') as css_file:
        css_styles = css_file.read()

    # Create a context dictionary with the products and total_price
    context = {
        'products': products,
        'total_price': calculate_total_price(products),  # Calculate the total price here]
        'order_id': order_id
    }

    # Render the email template with the context
    body = render_template_string(email_template, **context)
    body = body.replace('{{ css_styles }}', css_styles)

    return body

def calculate_total_price(products):
    total_price = 0
    for product in products:
        total_price += int(product['quantity']) * float(product['price'])
    return total_price


def get_orders_by_user_id(id):

    username = get_username_by_id(id).lower()

    # Check if table exists
    # Secure Query
    table_name = username + "_orders"
    if not is_valid_table_name(table_name):
        return None

    query = "SELECT * FROM {};".format(table_name)
    results = db_query(query)

    # Check if the user has any orders
    if not results:
        return None

    products = []
    for row in results:
        order_id = row[0]
        order_address = row[2]
        order_Date = row[4]
        for element in row[1]:
            product__ = get_product_by_id(element)
            if product__ is not None:

                product = {
                    "order_id" : order_id,
                    "product_id": element,
                    "quantity": row[1][element],
                    "name": product__["name"],
                    "price": product__["price"],
                    "address": order_address,
                    "date": order_Date
                }
                products.append(product)

    return products