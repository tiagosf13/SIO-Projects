from handlers.DataBaseCoordinator import db_query
import re


def check_username_exists(username):

    # Execute the query to check if the username exists in the user's table
    # Secure Query
    query = "SELECT exists(select 1 from users where username=%s);"
    result = db_query(query, (username,))

    # Return the boolean
    return result[0][0]

def is_valid_table_name(table_name):
    # Define a regular expression pattern to match valid table names
    valid_table_name_pattern = re.compile(r'^[a-zA-Z0-9_]+$')

    # Maximum table name length (adjust as needed)
    max_table_name_length = 50

    # Check if the table name matches the valid pattern and is not too long
    if len(table_name) <= max_table_name_length and valid_table_name_pattern.match(table_name):
        return True
    else:
        return False


def is_valid_review(review_text):
    # Define a regular expression pattern to match valid review characters
    valid_characters_pattern = re.compile(r'^[a-zA-Z0-9,.!?()\'" ]+$')

    # Check if the review contains only valid characters
    if not valid_characters_pattern.match(review_text):
        return False

    # You can add additional checks for specific patterns or keywords to prevent XSS
    # For example, you can look for "<script>", "onload=", etc., and return False if found.

    # If none of the checks above triggered a return False, the review is valid
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
