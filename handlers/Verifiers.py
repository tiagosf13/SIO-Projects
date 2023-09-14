from handlers.DataBaseCoordinator import db_query


def check_username_exists(username):

    # Execute the query to check if the username exists in the user's table
    result = db_query("SELECT exists(select 1 from users where username=%s)", (username,))

    # Return the boolean
    return result[0][0]


def check_email_exists(email):

    #Execute the query to check if the email exists in the user's table
    result = db_query("SELECT exists(select 1 from users where email=%s)", (email,))

    # Return the boolean
    return result[0][0]