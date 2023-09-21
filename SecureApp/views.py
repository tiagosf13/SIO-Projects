from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_from_directory, send_file
from handlers.UserManagement import search_user_by_email, validate_login, get_id_by_username
from handlers.UserManagement import search_user_by_username, send_recovery_password, create_user
from handlers.UserManagement import update_username, search_user_by_id, update_email, update_password
from handlers.UserManagement import get_user_role
from handlers.Verifiers import check_username_exists, check_email_exists, check_product_in_cart
from handlers.Retrievers import get_all_products, get_product_by_id, get_product_reviews, get_cart, verify_product_id_exists
from handlers.ProductManagement import create_product, remove_product, verify_id_exists, update_product_name, create_product_image
from handlers.ProductManagement import update_product_description, update_product_price, update_product_category, update_product_quantity
from handlers.ProductManagement import create_review, set_cart_item
from handlers.DataBaseCoordinator import check_database_table_exists, db_query
import os
import pandas as pd



# Starting Blueprint
views = Blueprint('views', __name__)


# Routes


@views.route('/static/<path:filename>')
def serve_static(filename):
    return views.send_static_file(filename)


# This route is used to show the home page
@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# This route is used to perform the login
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

            return redirect(url_for("views.catalog", id=session["id"]))

    return render_template("login.html")

@views.route('/logout')
def logout():

    # Clear the session variables
    session.clear()

    # Return the login page
    return redirect(url_for("views.login"))


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
    

# This view returns the account settings page
@views.route("/profile/<username>")
def profile(username):
    
    # Get ID based on the username
    id = get_id_by_username(username)

    # Return the account settings page
    return render_template("profile.html", username=username, id=id)


# This view is used to check if te username exits
@views.route('/check_username', methods=['POST'])
def check_username():

    # Get the username from the request
    username = request.form.get('username')

    # Check if the username exists
    exists = check_username_exists(username)

    # Build response dictionary with the boolean
    response = {'exists': exists}

    # Return the response as a JSON object
    return jsonify(response)


# This view is used to check if te email exits
@views.route('/check_email', methods=['POST'])
def check_email():

    # Get the email from the request
    email = request.form.get('email')

    # Check if the username exists
    exists = check_email_exists(email)

    # Build response dictionary with the boolean
    response = {'exists': exists}

    # Return the response as a JSON object
    return jsonify(response)

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


# This view is used to get a image
@views.route('/get_image/<path:filename>')
def get_image(filename):

    # Send the image
    path = "/".join(filename.split("/")[:-1])
    filename = filename.split("/")[-1]
    return send_from_directory(path, filename)


@views.route('/catalog/<id>')
def catalog(id):
    
        # Get the username and id from the session
        name = session.get("username")
        admin = session.get("admin")

        if admin:
            return render_template("catalog_admin.html", username=name, id=id, admin=admin)
        else:
            # Return the catalog page
            return render_template("catalog.html", username=name, id=id, admin=admin)


@views.route('/products')
def products():

    products = get_all_products()

    return jsonify(products)


@views.route('/add_product/<id>', methods=['POST'])
def add_product(id):

    product_name = request.form.get("productName")
    product_description = request.form.get("productDescription")
    product_price = request.form.get("productPrice")
    product_category = request.form.get("productCategory")
    product_quantity = request.form.get("productUnits")
    product_photo = request.files.get("productImage")

    product_id = create_product(product_name, product_description, product_price, product_category, product_quantity, product_photo)


    return redirect(url_for("views.catalog", id=session["id"]))


@views.route('/remove_product/<id>', methods=['POST'])
def remove_product_by_id(id):
    # Updated route name and parameter name to avoid conflicts
    product_id = request.form.get("productId")

    # Assuming 'remove_product' is a function you've defined elsewhere, you can use it here
    product = remove_product(product_id)

    return redirect(url_for("views.catalog", id=session["id"]))


@views.route('/edit_product/<id>', methods=['POST'])
def edit_product_by_id(id):

    product_id = request.form.get("productId")
    product_name = request.form.get("productName")
    product_description = request.form.get("productDescription")
    product_price = request.form.get("productPrice")
    product_category = request.form.get("productCategory")
    product_quantity = request.form.get("productUnits")
    product_photo = request.files.get("productImage")

    if verify_id_exists(product_id, "products"):
        if product_name != "":
            update_product_name(product_id, product_name)
        if product_description != "":
            update_product_description(product_id, product_description)
        if product_price != "":
            update_product_price(product_id, product_price)
        if product_category != "":
            update_product_category(product_id, product_category)
        if product_quantity != "":
            update_product_quantity(product_id, product_quantity)
        if product_photo:
            create_product_image(product_id, product_photo)


    return redirect(url_for("views.catalog", id=session["id"]))


@views.route('/product-quantities/<id>', methods=['POST', 'GET'])
def product_quantities(id):

    products = get_all_products()

    return render_template('product_quantities.html', products=products)


@views.route('/product/<int:product_id>')
def product_page(product_id):
    # Fetch the product details based on the product_id
    # You can retrieve the product information from your data source

    product = get_product_by_id(product_id)

    id = session.get("id")

    if id == None:
        # Pass the product details to the template
        return render_template('product_anonymous.html', productId=product_id, productPrice=product["price"], productName=product["name"], productDescription = product["description"])
    else:
        # Pass the product details to the template
        return render_template('product.html', productId=product_id, productPrice=product["price"], productName=product["name"], productDescription = product["description"])


@views.route('/get_reviews/<int:product_id>/')
def get_reviews(product_id):

    reviews = get_product_reviews(product_id)
    for element in reviews:
        element["username"] = search_user_by_id(element["user_id"])[1]

    return jsonify(reviews)


@views.route('/add_review/<product_id>', methods=['POST'])
def add_review(product_id):

    # Get the user's id and username from the session
    user_id = session.get("id")

    # Get the review and rating from the request
    review = request.form.get("userReview")
    rating = request.form.get("rating")
    

    # Create the review
    create_review(product_id, user_id, review, rating)

    # Return a JSON response with the correct content type
    response_data = {'message': 'Review added successfully'}
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}


@views.route('/add_item_cart/<int:product_id>', methods=['POST'])
def add_item_to_cart(product_id):
    username = session.get("username").lower()
    check_database_table_exists(username + "_cart")
    try:
        data = request.get_json()
        quantity = data.get('quantity')

        if quantity <= 0:
            return jsonify({'error': 'Invalid quantity.'}), 500

        user_cart = get_cart(username + "_cart")

        for product in user_cart:
            if product["product_id"] == product_id:
                product_stock = get_product_by_id(product_id)["stock"]
                print("product_quantity: " + str(product["quantity"]))
                print("quantity: " + str(quantity))
                print("product_stock: " + str(product_stock))
                if product["quantity"] + quantity > product_stock:
                    return jsonify({'error': 'Not enough stock.'}), 500
                else:
                    # You can add code here to update the user's cart in the database
                    set_cart_item(username + "_cart", product_id, quantity, "add")
                    return jsonify({'message': 'Product added to the cart.'}), 200
                
        product_stock = get_product_by_id(product_id)["stock"]
        if quantity > product_stock or quantity < 0:
            return jsonify({'error': 'Not enough stock.'}), 500
        else:
            # You can add code here to update the user's cart in the database
            set_cart_item(username + "_cart", product_id, quantity, "add")
            return jsonify({'message': 'Product added to the cart.'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    


@views.route('/remove_item_cart/<int:product_id>', methods=['POST'])
def remove_item_from_cart(product_id):
    username = session.get("username").lower()

    try:
        data = request.get_json()
        quantity = data.get('quantity')

        if check_product_in_cart(username + "_cart", product_id) == False or quantity <= 0:
            return jsonify({'error': 'Product not in cart.'}), 500
        else:
            user_cart = get_cart(username + "_cart")

            for product in user_cart:
                if product["quantity"] == 0:
                    print("delete")
                    # Remove the product from the cart
                    query = "DELETE FROM " + username + "_cart WHERE product_id = %s"
                    db_query(query, (product["product_id"],))
                elif product["product_id"] == product_id:
                    product_stock = get_product_by_id(product_id)["stock"]
                    print("product_quantity: " + str(product["quantity"]))
                    print("quantity: " + str(quantity))
                    print("product_stock: " + str(product_stock))
                    if product["quantity"] - quantity < 0:
                        return jsonify({'error': 'Not enough stock.'}), 500
                    else:
                        # You can add code here to update the user's cart in the database
                        set_cart_item(username + "_cart", product_id, quantity, "remove")
                        return jsonify({'message': 'Product added to the cart.'}), 200

            return jsonify({'message': 'Product added to the cart.'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500



@views.route('/get_cart_items/', methods=['GET'])
def get_cart_items():
    username = session.get("username").lower()
    check_database_table_exists(username + "_cart")
    user_cart = get_cart(session.get("username").lower() + "_cart")

    for product in user_cart:
        if not verify_product_id_exists(product["product_id"]) or product["quantity"] == 0 or product["quantity"] > get_product_by_id(product["product_id"])["stock"]:
            # Remove the product from the cart
            query = "DELETE FROM " + username + "_cart WHERE product_id = %s"
            db_query(query, (product["product_id"],))
            #remove from user cart
            user_cart.remove(product)

    return jsonify(user_cart)


@views.route('/remove_all_items_cart', methods=['POST'])
def remove_all_items_cart():
    username = session.get("username").lower()

    # Remove all the products from the cart
    query = "DELETE FROM " + username.lower() + "_cart"
    db_query(query)

    return jsonify({'message': 'Cart cleared.'}), 200