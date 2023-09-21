import os
import json
import psycopg2


def read_json(filename):


    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

    full_file_path = current_directory + filename

    with open(full_file_path, "r", encoding="utf8") as file:
        data = json.load(file)
    return data


def db_query(query, params=None):

    # Get the credentials for accessing the database
    credentials = read_json("/credentials/DataBaseCredentials.json")

    # Connect to the database
    conn = psycopg2.connect(
        host=credentials["host"],
        dbname=credentials["dbname"],
        user=credentials["user"],
        password=credentials["password"],
        port=credentials["port"]
    )

    # Initiate the cursor
    cur = conn.cursor()

    # Check if there is any parameters
    if params:

        # Execute query with parameters
        cur.execute(query, params)

    else:

        # Execute query without parameters
        cur.execute(query)

    # Define select_in_query as False by default
    select_in_query = False

    # Check if the query has SELECT
    if "SELECT" in query:

        # Fetch all the data
        data = cur.fetchall()
        select_in_query = True

    # Commit the connection
    conn.commit()

    # Close the cursor
    cur.close()

    # Close the connection
    conn.close()

    # Check if the query has SELECT
    if select_in_query:

        # Return the requested data
        return data
    

def check_database_table_exists(table_name):
        # Construct the SQL query

        # Secure Query
        # query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"
        # result = db_query(query, (table_name,))

        # Unsecure Query
        query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=" + table_name + ")"
        result = db_query(query)
        
        if not result[0][0]:
            if table_name == "users":
                # Construct the SQL query
                query = "CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), email VARCHAR(255), admin BOOLEAN)"
            elif table_name == "products":
                query = "CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), price VARCHAR(255), category VARCHAR(255), stock INTEGER)"
            elif table_name == "reviews":
                query = "CREATE TABLE reviews (id SERIAL PRIMARY KEY, product_id INTEGER, user_id INTEGER, rating INTEGER, review VARCHAR(255))"
            elif "_cart" in table_name:
                # Secure Query
                #params = table_name
                #query = "CREATE TABLE %s (product_id SERIAL PRIMARY KEY, quantity INTEGER)"

                query = "CREATE TABLE " + table_name + " (product_id SERIAL PRIMARY KEY, quantity INTEGER)"

            elif "all_orders" in table_name:
                query = "CREATE TABLE all_orders (id SERIAL PRIMARY KEY, user_id INTEGER, order_date VARCHAR(255))"
            else:
                # Secure Query
                # params = table_name
                #query = "CREATE TABLE %s (id SERIAL PRIMARY KEY, products JSON, total_price VARCHAR(255), shipping_address VARCHAR(255), order_date VARCHAR(255))"
                query = "CREATE TABLE " + table_name + " (id SERIAL PRIMARY KEY, products JSON, total_price VARCHAR(255), shipping_address VARCHAR(255), order_date VARCHAR(255))"
            
            # Secure Query
            #if params:
            #    db_query(query, params)
            #else:
            #    db_query(query)
            db_query(query)