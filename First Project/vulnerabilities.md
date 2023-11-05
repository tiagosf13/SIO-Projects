# V1 [[CWE-89](https://cwe.mitre.org/data/definitions/89.html)] - Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

> **The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component.**

---

##### Login (V1.1)

> In the Login, if the username is ' the web app will malfunction (SQL Injection)

In the Login View, the function `validate_login(username, password)` in the *UserManagement.py* file was used to validate the Login.

Definition of the function:

```python
def validate_login(username, password):

    # If username is None, return False (user not found)
    if username is None:
        return False
    else:
  
        # Fetch the user's password
        # Secure Query
        # query = "SELECT password FROM users WHERE username = %s"
        # result = db_query(query, (username,))

        query = "SELECT password FROM users WHERE username = '"+username + "';"
        result = db_query(query)

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
```

As we can see, this function creates a SQL query by concatenating a username variable into the string. This makes the SQL query susceptible to SQL injection.

Examples of SQL Injection:

```sql
    SELECT password FROM users WHERE username = 'malicious' OR '1'='1';
```

```sql
    SELECT password FROM users WHERE username = ' ' ';
```

This would break the Web App. Demonstration:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/aa7a1116-08f8-49b8-9826-1ddb810a3854

To fix this vulnerabiltiy, we used a parameterized query in the function `search_user_by_username(username)`, and modified the our custom `db_query` to work with parameters.

Definition of the two functions:

```python
def search_user_by_username(username):

    # Secure Query
    query = "SELECT * FROM users WHERE username = %s"
    result = db_query(query, (username,))


    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]
```

```python
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
```

In this way, and by using a cursor to execute the queries, we eliminate the SQL Injection vulnerability.

---

# V2 [[CWE-79](https://cwe.mitre.org/data/definitions/79.html)] - Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

> **The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component.**

---

##### Add a Product Review (V2.1)

> While adding a product review, the text area input is vulnerable to XSS

In the Add Review View, when adding a product review, the input ,  it was possible to obtain profile images of other users using:

```html
    <img src="/get_image/database/accounts/926927.png">
```

This was possible because when adding a review, the input on the textbox wasn't being checked for XSS (it wasn't sanitized before adding the review):

```python
def add_review(product_id):

    # Get the user's id and username from the session
    user_id = session.get("id")
    username = session.get("username")

    # Get the review and rating from the request
    review = request.form.get("userReview")
    rating = request.form.get("rating")
  

    # Create the review
    create_review(product_id, user_id, review, rating)

    # Return a JSON response with the correct content type
    response_data = {'message': 'Review added successfully', "username": username}
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}
```

Demonstration:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/d7539639-2ba3-4cf9-8251-f0d57a8c984b

In order to fix this, we implemented the function `is_valid_input(review)` to verify if it didn't have any patterns, expressions or characters that are linked to XSS:

```python
    def add_review(product_id):

    # Get the user's id and username from the session
    user_id = session.get("id")
    username = session.get("username")

    if user_id == None:
        return redirect(url_for("views.login"))

    # Get the review and rating from the request
    review = request.form.get("userReview")
    rating = request.form.get("rating")

    if not is_valid_input(review) or verify_id_exists(product_id, "products") == False or rating == None:
        return jsonify({'error': 'Invalid review.'}), 500
  

    # Create the review
    create_review(product_id, user_id, review, rating)

    # Return a JSON response with the correct content type
    response_data = {'message': 'Review added successfully', "username": username}
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}
```

```python
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
```

With the use of this function, any XSS input on the textbox won't be added to the reviews

---

# V3 [[CWE-285](https://cwe.mitre.org/data/definitions/285.html)] - Improper Authorization

> **The product does not perform or incorrectly performs an authorization check when an actor attempts to access a resource or perform an action.**

---

##### Acessing Pages Without Auth (V3.1)

> The authentication can be skipped by putting the right URL, so any page can be easily accessed, including the user's profile page and all the account.

Any client could access other user's profile, cart, orders, etc. This was a critical vulnerability because any client could alter with the user's account information (ex. Changing Password).

```python
    @views.route("/profile/<username>")
    def profile(username):
      
        # Get ID based on the username
        id = get_id_by_username(username)
  
        # Return the account settings page
        return render_template("profile.html", username=username, id=id)
```

```python
    @views.route('/login', methods=['GET','POST'])
    def login():
      
        if request.method == "POST":
            # Get the password and username and email that were set in the signup session
            username = request.form.get("username")
            password = request.form.get("password")
  
            # Check if the username has a space
            if " " in username and len(username.split(" ")) == 2:
  
                # Merge the string into one username
                username = username.replace(" ", "")
  
            # Check if the username inserted is a email
            if "@" in username:
  
                # Search the username based on the email
                username = search_user_by_email(username)
  
            # Check if the login credentials are valid
            if validate_login(username, password) == True:
                # Set the session variables
                session["username"] = username
                session["id"] = get_id_by_username(username)
                session["admin"] = get_user_role(session["id"])
                check_database_table_exists(username.lower() + "_cart")
                check_database_table_exists(f"{username.lower()}_orders")
  
                return redirect(url_for("views.catalog", id=session["id"]))
  
        return render_template("login.html")
```

This was possible because on every View, we didn't check for the user's ID, which is granted on Login.

Demonstration:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/12a3ed63-446e-4e84-a364-646dc45d55b0

To fix this, we checked if the user ID was present when we looked at the view. If it wasn't, we returned the Login View.

```python
    # This view returns the account settings page
    @views.route("/profile/<username>")
    def profile(username):
      
        if is_valid_input(username) == False:
            return render_template("index.html", message="Invalid username.")
  
        # Get ID based on the username
        id = session.get("id")
  
        if id == None:
            return redirect(url_for("views.login"))
  
        # Return the account settings page
        return render_template("profile.html", username=username, id=id)
```

Demonstration after the fix:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/6962b34a-3972-4b37-9792-691684718d57

---

# V4 [[CWE-256](https://cwe.mitre.org/data/definitions/256.html)] - Plaintext Storage of a Password

> **Storing a password in plaintext may result in a system compromise.**

---

##### Password not Encrypted (V4.1)

> The password is being stored in plaintext

If there were to be a data breach from the database, the attacker could visualize all the passwords because they weren't encrypted.

This was possible because when storing the user's password after Signing Up or changing the password, it wasn't being encrypted:

```python
    # This view is used to enroll new users into the platform
    @views.route("/signup", methods=["GET", "POST"])
    def signup():
  
        if request.method == "POST":
            # Get the username, password and email from the request
            username = request.form.get("username")
            password = request.form.get("password")
            email = request.form.get("email")
  
            # Check if there is no user in the database using the same email or the same username
            if search_user_by_email(email) != None or search_user_by_username(username) != None:
  
                # Return signup page if there is
                return render_template("signup.html", message="User already exists.")
  
            else:
  
                # Create the user in the database
                create_user(username, password, email)
  
                # Return the 2FA signup page, in order to validate the email
                return redirect(url_for("views.login"))
        else:
            return render_template("signup.html")
```

```python
    # This view is used to check if te email exits
    @views.route('/update_account/<id>', methods=['POST'])
    def update_account(id):
  
        # Set the user's account image file path
        file_path = os.getcwd()+f"/database/accounts/{id}.png"
  
        # Get the new uploaded user's account image
        profile_photo = request.files.get("profile_photo")
  
        # If there is a image
        if profile_photo:
  
            # Save the image to the user's account
            profile_photo.save(file_path)
  
        # Get the username, email and password, from the user's session
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("psw")
  
        # Check if the username field wasn't empty and occupied by another user
        if username != "" and not check_username_exists(username):
  
            # Update the username
            update_username(id, username)
  
            # Set the sessions username
            session["username"] = username
  
        else:
  
            # If there is a problem with the username, get the username based on the ID
            username = search_user_by_id(id)[1]
  
        # Check if the email field wasn't empty and occupied by another user
        if email != "" and not check_email_exists(email):
  
            # Update the email
            update_email(id, email)
  
        else:
  
            # If there is a problem with the username, get the username based on the ID
            email = search_user_by_id(id)[3]
  
        # Check if the password wasn't empty
        if password != "":
  
            # Update the password
            update_password(id, password)
      
        # Return the profile page
        return redirect(url_for("views.catalog", id=id))
```

To fix this, we used `bcrypt` to generate a password hash and then store it. When we needed the password (ex. Login), we check if the two password hashes match.

```python
    @views.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username").lower()
            password = request.form.get("password")
            email = request.form.get("email")
  
            if is_valid_input(username) == False or is_valid_input(email) == False:
                return render_template("signup.html", message="Invalid username.")
  
  
            # Check if there is no user in the database using the same email or the same username
            if search_user_by_email(email) != None or search_user_by_username(username) != None:
                return render_template("signup.html", message="User already exists.")
            else:
                # Hash the password before storing it in the database
                hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
  
                # Create the user in the database with the hashed password
                create_user(username, hashed_password, email)
  
                return redirect(url_for("views.login"))
        else:
            return render_template("signup.html")
```

```python
    @views.route('/login', methods=['GET','POST'])
    def login():
        if request.method == "POST":
            username = request.form.get("username").lower()
            password = request.form.get("password")
  
            if is_valid_input(username) == False:
                return render_template("login.html", message="Invalid username.")
  
            user = search_user_by_username(username)
  
            if user and bcrypt.check_password_hash(user[2], password):
                # Password is correct
                session["username"] = username
                session["id"] = get_id_by_username(username)
                session["admin"] = get_user_role(session["id"])
                check_database_table_exists(username.lower() + "_cart")
                check_database_table_exists(f"{username.lower()}_orders")
                return redirect(url_for("views.catalog", id=session["id"]))
  
            # Password is incorrect
            return render_template("login.html", message="Invalid login credentials.")
  
        return render_template("login.html")
```

Demonstration:

`Before`

![Before](https://github.com/detiuaveiro/1st-project-group_10/blob/main/image/vulnerabilities/1697807825519.png)

`After`

![After](https://github.com/detiuaveiro/1st-project-group_10/blob/main/image/vulnerabilities/1697807881092.png)


---

# V5 [[CWE-756](https://cwe.mitre.org/data/definitions/756.html)] - Missing Custom Error Page

> **The product does not return custom error pages to the user, possibly exposing sensitive information.**

---

##### Missing Error Page (V5.1)

> The product does not return custom error pages to the user, possibly exposing sensitive information.

When the web application encountered an error, it would display the error message along with lines of code, and occasionally, it would expose privileged information.

This has the potential to inflict greater harm upon the web application and its users, as the exposure of sensitive information could lead to the discovery of vulnerabilities or the compromise of user data.

Demonstration:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/aa7a1116-08f8-49b8-9826-1ddb810a3854

To address this issue, custom error pages were implemented. In the event of an error in the web application or a missing page, these custom pages would be displayed.

This routes are present in the `app.py` file.

```python
    # Define a custom error handler for 403 (Not Found) errors
    @app.errorhandler(403)
    def page_not_found(error):
        return render_template('403.html'), 403
    
    
    # Define a custom error handler for 404 (Not Found) errors
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    
    # Define a custom error handler for 500 (Not Found) errors
    @app.errorhandler(500)
    def page_not_found(error):
        return render_template('500.html'), 500
```

Demonstration After Fix:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/55968e48-4ae9-46cc-b778-ce89d7a6bdd9

---

# V6 [[CWE-798](https://cwe.mitre.org/data/definitions/798.html)] - Use of Hard-coded Credentials

> The product contains hard-coded credentials, such as a password or cryptographic key, which it uses for its own inbound authentication, outbound communication to external components, or encryption of internal data.

---

##### Credentials in the Code (V6.1)

> The email and database credentials are hard-coded into the code files.

To access APIs and the database, the backend required authentication credentials. During the development of the web application, hard-coded credentials were utilized.

This poses a significant security risk because, in the event of a source code breach (e.g., through an error page), the credentials could be exposed.

```python
    def db_query(query, params=None):

    credentials = {
                    "host": "Your_Machine_IP_Address",
                    "dbname": "Your_Database_Name",
                    "user": "Your_Database_Username",
                    "password" : "Your_Database_Password",
                    "port" : "Your_Database_Port (Standard PostgreSQL Port - 5432)"
                }

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
```

```python
    def send_email_with_attachment(to, subject, body, attachment_path):
    # Read Email credentials file
    credentials = {
                    "email": "Your_Gmail_Address",
                    "password": "Your_Gmail_API_Key"
                }

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Attach the PDF file as an attachment
    with open(attachment_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")

    pdf_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    msg.attach(pdf_attachment)

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(credentials["email"], credentials["password"])

        # Send the email with attachment
        server.sendmail(credentials["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True




    def send_email(to, subject, body):
    
        # Read Email credentials file
        credentials = {
                        "email": "Your_Gmail_Address",
                        "password": "Your_Gmail_API_Key"
                    }
    
        # Create a MIMEText object to represent the email body
        msg = MIMEMultipart()
        msg['From'] = credentials["email"]
        msg['To'] = to
        msg['Subject'] = subject
    
        # Attach the body of the email
        msg.attach(MIMEText(body, 'html'))
    
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server
    
        try:
            # Login to your email account
            server.login(credentials["email"], credentials["password"])
    
            # Send the email
            server.sendmail(credentials["email"], to, msg.as_string())
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
        finally:
            # Close the connection to the SMTP server
            server.quit()
    
        # Return True to indicate the email was sent successfully
        return True
```

To address this issue, we introduced the read_json(filename) function to store credentials in a JSON file. When necessary, we read the file to obtain the credentials, ensuring they are not hard-coded in the source code.

```python
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
```

```python
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
```

```python
    def send_email_with_attachment(to, subject, body, attachment_path):
    # Read Email credentials file
    credentials = read_json("/credentials/EmailCredentials.json")

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Attach the PDF file as an attachment
    with open(attachment_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")

    pdf_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    msg.attach(pdf_attachment)

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(credentials["email"], credentials["password"])

        # Send the email with attachment
        server.sendmail(credentials["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True




    def send_email(to, subject, body):
    
        # Read Email credentials file
        credentials = read_json("/credentials/EmailCredentials.json")
    
        # Create a MIMEText object to represent the email body
        msg = MIMEMultipart()
        msg['From'] = credentials["email"]
        msg['To'] = to
        msg['Subject'] = subject
    
        # Attach the body of the email
        msg.attach(MIMEText(body, 'html'))
    
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server
    
        try:
            # Login to your email account
            server.login(credentials["email"], credentials["password"])
    
            # Send the email
            server.sendmail(credentials["email"], to, msg.as_string())
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
        finally:
            # Close the connection to the SMTP server
            server.quit()
    
        # Return True to indicate the email was sent successfully
        return True
```

`DataBaseCredentials.json`

```json
    {
        "host": "Your_Machine_IP_Address",
        "dbname": "Your_Database_Name",
        "user": "Your_Database_Username",
        "password" : "Your_Database_Password",
        "port" : "Your_Database_Port (Standard PostgreSQL Port - 5432)"
    }
```

`EmailCredentials.json`

```json
    {
        "email": "Your_Gmail_Address",
        "password": "Your_Gmail_API_Key"
    }
```

---

# V7 [[CWE-620](https://cwe.mitre.org/data/definitions/620.html)] - Unverified Password Change

> When setting a new password for a user, the product does not require knowledge of the original password, or using another form of authentication.

##### Previous Password Not Required (V7.1)

> In the account settings page, when changing the password, the original password isn't required

In the Profile View, users could change their password without the requirement of providing the old one.

This allowed anyone with access to a user's Profile View to potentially compromise accounts by changing the password.

```python
    # This view is used to check if te email exits
    @views.route('/update_account/<id>', methods=['POST'])
    def update_account(id):
    
        # Set the user's account image file path
        file_path = os.getcwd()+f"/database/accounts/{id}.png"
    
        # Get the new uploaded user's account image
        profile_photo = request.files.get("profile_photo")
    
        # If there is a image
        if profile_photo:
    
            # Save the image to the user's account
            profile_photo.save(file_path)
    
        # Get the username, email and password, from the user's session
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("psw")
    
        # Check if the username field wasn't empty and occupied by another user
        if username != "" and not check_username_exists(username):
    
            # Update the username
            update_username(id, username)
    
            # Set the sessions username
            session["username"] = username
    
        else:
    
            # If there is a problem with the username, get the username based on the ID
            username = search_user_by_id(id)[1]
    
        # Check if the email field wasn't empty and occupied by another user
        if email != "" and not check_email_exists(email):
    
            # Update the email
            update_email(id, email)
    
        else:
    
            # If there is a problem with the username, get the username based on the ID
            email = search_user_by_id(id)[3]
    
        # Check if the password wasn't empty
        if password != "":
    
            # Update the password
            update_password(id, password)
        
        # Return the profile page
        return redirect(url_for("views.catalog", id=id))
```

Demonstration:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/5f867165-416f-47f2-b044-0e67d620744b

To fix this issue, we updated the HTML page and the Update Account View to include the old password

```python
    @views.route('/update_account/<id>', methods=['POST'])
    def update_account(id):
    
        if id == None or session.get("id") == None:
            return redirect(url_for("views.login"))
        
        try:
    
            if os.name == "nt":
                # Get the current working directory
                current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
            else:
                # Get the current working directory
                current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]
                
            accounts_directory = os.path.join(current_directory, "database", "accounts")
            os.makedirs(accounts_directory, exist_ok=True)  # Ensure the directory exists
    
            file_path = os.path.join(accounts_directory, f"{id}.png").replace("\\", "/")
    
            # Get the new uploaded user's account image
            profile_photo = request.files.get("profile_photo")
    
            # If there is an image
            if profile_photo:
                # Save the image to the user's account
                profile_photo.save(file_path)
    
            # Get the username, email, and password from the user's session
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("psw")
            old_password = request.form.get("psw-old")
    
            # Check if the username field wasn't empty and occupied by another user
            if username != "" and not check_username_exists(username) and is_valid_input(username):
    
                # Update the username
                update_username(id, username)
    
                # Set the session's username
                session["username"] = username
    
            else:
                # If there is a problem with the username, get the username based on the ID
                username = search_user_by_id(id)[1]
    
            # Check if the email field wasn't empty and occupied by another user
            if email != "" and not check_email_exists(email) and is_valid_input(email):
    
                # Update the email
                update_email(id, email)
    
            else:
                # If there is a problem with the email, get the email based on the ID
                email = search_user_by_id(id)[3]
    
            # Check if the password wasn't empty
            if password != "":
                # Update the password
                # Hash the password before storing it in the database
    
                if bcrypt.check_password_hash(search_user_by_id(id)[2], old_password):
                    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
                    username = search_user_by_id(id)[1]
                    update_password(username, hashed_password)
                else:
                    return render_template("profile.html", message="Invalid password.", username=username, id=id)
    
            # Return the profile page
            return redirect(url_for("views.catalog", id=id))
```
---

# V8 [[CWE-640](https://cwe.mitre.org/data/definitions/640.html)] - Weak Password Recovery Mechanism for Forgotten Password

> When setting a new password for a user, the product does not require knowledge of the original password, or using another form of authentication.

##### Password Sent to Email (V7.1)

> When recovering the password, the system will send the new password to the user's email

The password recovery system was designed to generate a new password, store it in the database and then send it to the user's email.

This causes severe issues, such as lack of authentication, exposure to email interception, password exposure, password rotation, etc.

```python
    # This route is used to let the user reset he's password
@views.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    # Check if the requested method is POST
    if request.method == "POST":

        # Get the user's email from the request
        email = request.form.get("email")

        # Get the username based on the email
        user = search_user_by_email(email)

        # Check if the user exists
        if user is None:

            # If the user doesn't exist, return the signup page
            return redirect(url_for("views.signup"))

        else:
            
            # Send recovery password to the user's email
            send_recovery_password(email)

            # Return the login page
            return redirect(url_for("views.login"))
    else:

        # If it isn't, return the same page
        return render_template("reset-password.html")
```

Demonstration:

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/067e7dd7-5d4c-4d96-ba75-fb4c0c7ea862

![Password-Weak Recover](https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/71f55e97-f480-431d-b684-0600fb430ff6)

To address this concern, we implemented a new password recovery system that relies on tokens with timestamps. In order to accomodate this system, we change the table `user` in the database.

```python
    # This route is used to let the user reset their password
    @views.route("/reset-password", methods=["GET", "POST"])
    def reset_password():
        if request.method == "POST":
            email = request.form.get("email")
            if is_valid_input(email) == False:
                return render_template("reset-password.html", message="Invalid email.")
    
            user = search_user_by_email(email)
            if user is None:
                # If the user doesn't exist, return the signup page
                return redirect(url_for("views.signup"))
            else:
                # Generate a unique reset token
                reset_token = generate_reset_token()
                # Store the reset token in the user's record in the database
                set_reset_token_for_user(user, reset_token)
                # Send a password reset email with the token
                send_password_reset_email(email, reset_token)
                return redirect(url_for("views.login"))
        else:
            return render_template("reset-password.html")
```

```python
    @views.route('/reset_password/<reset_token>', methods=['GET', 'POST'])
    def reset_password_confirm(reset_token):
        # Check if the reset token is valid and not expired
        if is_valid_reset_token(reset_token):
            if request.method == 'POST':
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')
    
                if new_password == confirm_password:
                    # Update the user's password in the database with the new hashed password
                    username = get_user_by_reset_token(reset_token)[1]
    
                    if username:
                        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
                        update_password(username, hashed_password)
    
                        # Clear the reset token for security
                        clear_reset_token(username)
                        return redirect(url_for('views.login'))
            return render_template('reset_password.html', reset_token=reset_token)
        else:
            return redirect(url_for('views.login'))
```

Demonstration

https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/9b9e03dd-05b9-46bb-bcd0-063559530eb6

![Password-Strong Recover Database](https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/dfc4c419-f45a-4580-a6e1-239f4d97c9ee)

![Password-Strong Recover Email](https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/f1bc7b51-65f4-4c45-98b4-b8f421e4807b)

![Password-Strong Recover WebPage](https://github.com/detiuaveiro/1st-project-group_10/assets/102866402/784c73b0-128b-4ab5-b706-baa2776598c3)
