from handlers.DataBaseCoordinator import db_query


def check_username_exists(username):

    # Execute the query to check if the username exists in the user's table
    # Secure Query
    query = "SELECT exists(select 1 from users where username=%s);"
    result = db_query(query, (username,))

    # Return the boolean
    return result[0][0]


def check_email_exists(email):

    #Execute the query to check if the email exists in the user's table
    # Secure Query
    query = "SELECT exists(select 1 from users where email=%s);"
    result = db_query(query, (email,))

    # Return the boolean
    return result[0][0]


def check_product_in_cart(tablename, product_id):
    
    # Execute the query to check if the product exists in the cart
    # Secure Query
    query = "SELECT exists(select 1 from %s where product_id=%s);"
    result = db_query(query, (tablename, product_id,))

    # Return the boolean
    return result[0][0]