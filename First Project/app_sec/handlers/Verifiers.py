from handlers.DataBaseCoordinator import db_query, is_valid_table_name
import re


def check_username_exists(username):

    # Execute the query to check if the username exists in the user's table
    # Secure Query
    query = "SELECT exists(select 1 from users where username=%s);"
    result = db_query(query, (username,))

    # Return the boolean
    return result[0][0]


def is_valid_input(review_text):
    # Define a regular expression pattern to match valid characters
    valid_characters_pattern = re.compile(r'^[a-zA-Z0-9,.!?()\'" @]+$')

    # Check if the review contains only characters not in the valid pattern
    if not valid_characters_pattern.match(review_text):
        return False

    if re.search(r"<script>", review_text) or re.search(r"onload=", review_text) or re.search(r"<img", review_text):
        return False

    # Check if the review contains a single quote
    if "'" in review_text:
        return False
    
    # If none of the checks above returned False, the review is valid
    return True


def check_email_exists(email):

    #Execute the query to check if the email exists in the user's table
    # Secure Query
    query = "SELECT exists(select 1 from users where email=%s);"
    result = db_query(query, (email,))

    # Return the boolean
    return result[0][0]


def check_product_in_cart(tablename, product_id):
    
    # Secure Query: Validate the table name
    if not is_valid_table_name(tablename):
        return False

    # Secure Query: Check if the product exists in the cart
    query = f"SELECT exists(SELECT 1 FROM {tablename} WHERE product_id=%s);"
    result = db_query(query, (product_id,))

    # Return the boolean
    return result[0][0]
