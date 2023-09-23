import os, json, psycopg2, re


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
    try:

        if not is_valid_table_name(table_name):
            return False
        # Secure Query
        query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"
        result = db_query(query, (table_name,))

        if not result[0][0]:
            if table_name == "users":
                # Construct the SQL query
                query = "CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), email VARCHAR(255), admin BOOLEAN)"
                db_query(query, ())

            elif table_name == "products":
                query = "CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), price VARCHAR(255), category VARCHAR(255), stock INTEGER)"
                db_query(query, ())

            elif table_name == "reviews":
                query = "CREATE TABLE reviews (id SERIAL PRIMARY KEY, product_id INTEGER, user_id INTEGER, rating INTEGER, review VARCHAR(255))"
                db_query(query, ())

            elif "_cart" in table_name:
                # Construct the SQL query
                query = f"CREATE TABLE {table_name} (product_id SERIAL PRIMARY KEY, quantity INTEGER)"
                db_query(query, ())


            elif "all_orders" in table_name:
                query = "CREATE TABLE all_orders (id SERIAL PRIMARY KEY, user_id INTEGER, order_date VARCHAR(255))"
                db_query(query, ())

            else:
                # Construct the SQL query
                query = f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, products JSON, total_price VARCHAR(255), shipping_address VARCHAR(255), order_date VARCHAR(255))"
                db_query(query, ())

    except Exception as e:
        print(e)
