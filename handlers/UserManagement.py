from handlers.DataBaseCoordinator import db_query
import random
from string import ascii_uppercase
from handlers.EmailHandler import send_email
import os
import shutil



def search_user_by_username(username):
    # Construct the SQL query
    query = "SELECT * FROM users WHERE username = %s"
    
    # Execute the query and get the result
    result = db_query(query, (username,))

    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]


def search_user_by_email(email):

    # Construct the SQL query
    query = "SELECT * FROM users WHERE email = %s"
    
    # Execute the query and get the result
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
    query = "SELECT id FROM users WHERE username = %s"

    # Execute the query and get the result
    result = db_query(query, (username,))

    # Check if 
    if result:
        return str(result[0][0])
    else:
        return None
    

def generate_password(length):

    while True:
        code = ""
        # Generate a code with the specified length
        for _ in range(length):
            code += random.choice(ascii_uppercase)
    
    # Return the unique code
    return code
    

def send_recovery_password(email):

    # Search for the user with the given email
    user = search_user_by_email(email)

    # If user is None, return False (user not found)
    if user is None:

        return False
    else:

        # Extract the username and password from the user
        name = user
        password = generate_password(15)
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
                <p>Your password is: <strong>{password}</strong></p>
            </body>
            </html>
        """

        # Send the recovery email to the user
        send_email(email, "Recover your password", HTMLBody)

        # Return True to indicate the email was sent successfully
        return True
    

def check_id_existence(id):
    result = db_query("SELECT EXISTS(SELECT 1 FROM users WHERE id = %s);", (id,))
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
    user_directory = os.path.join(directory, "database", "accounts", str(id))

    # Create the user's directory and any missing parent directories
    os.makedirs(user_directory, exist_ok=True)

    # Set the paths for the source and destination files
    src_path = os.path.join(directory, "static", "images", "default.png")
    dst_path = os.path.join(user_directory, f"{id}.png")

    # Copy the source file to the destination file
    shutil.copy(src_path, dst_path)



def create_user(username, password, email):
    # Generate a unique user id
    id = str(generate_random_id())
    
    # Add the user to the USER table
    db_query("INSERT INTO users (id, username, password, email) VALUES (%s, %s, %s, %s);",
            (id, username, password, email)
    )

    # Create a folder for the user
    create_user_folder(id)

    # Return the created user
    return id


def change_password(id, password):

    # Build the query to update the password in the user's table
    update_query = 'UPDATE users SET password = %s WHERE id = %s'

    # Set the parameters for the query
    update_params = (password, id)

    # Execute the query
    db_query(update_query, update_params)


def update_username(id, new_username):

    # Get the old username based on the ID
    old_username = search_user_by_id(id)[1]
    
    # Construct the SQL query
    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"

    # Execute the query and get the result
    result = db_query(query, (old_username,))
    if result[0][0]:

        # Build the query to alterate the statement username's table
        alter_query = f'ALTER TABLE "{old_username}" RENAME TO "{new_username}";'

        # Execute the query
        db_query(alter_query)

    # Build the query to update the username in the user's table
    update_query = 'UPDATE users SET username = %s WHERE id = %s'

    # Set the parameters for the query
    update_params = (new_username, id)

    # Execute the query
    db_query(update_query, update_params)


def search_user_by_id(id):

    # Construct the SQL query
    query = "SELECT * FROM users WHERE id = %s"

    # Execute the query and get the result
    result = db_query(query, (id,))

    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]


def update_email(id, email):

    # Build the query to update the email in the user's table
    update_query = 'UPDATE users SET email = %s WHERE id = %s'

    # Set the parameters for the query
    update_params = (email, id)

    # Execute the query
    db_query(update_query, update_params)


def update_password(id, password):

    # Build the query to update the password in the user's table
    update_query = 'UPDATE users SET password = %s WHERE id = %s'

    # Set the parameters for the query
    update_params = (password, id)

    # Execute the query
    db_query(update_query, update_params)


def get_username_by_id(id):
    # Construct the SQL query to retrieve the username
    query = "SELECT username FROM users WHERE id = %s"
    
    # Execute the query and get the result
    result = db_query(query, (id,))

    # Check if the username was found
    if result:

        # If it was, return the username
        return result[0][0]

    else:

        # If it wasn't return None
        return None