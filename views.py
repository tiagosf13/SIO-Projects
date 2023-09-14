from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_from_directory, send_file
from handlers.UserManagement import search_user_by_email, validate_login, get_id_by_username
from handlers.UserManagement import search_user_by_username, send_recovery_password, create_user
from handlers.UserManagement import update_username, search_user_by_id, update_email, update_password
from handlers.UserManagement import get_username_by_id
from handlers.Verifiers import check_username_exists, check_email_exists
from handlers.Retrievers import get_all_products
from handlers.DataBaseCoordinator import db_query
import os



# Starting Blueprint
views = Blueprint('views', __name__)


# Routes

# This route is used to show the home page
@views.route('/', methods=['GET'])
def index():
    return render_template('catalog_index.html')


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

            # Return the 2FA login page
            return redirect(url_for("views.catalog", id=session["id"]))


    else:
        return render_template("login.html")


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

            # Set the 2FA signup code, username, email and password to the signup session
            session["username_signup"] = username
            session["email_signup"] = email
            session["password_signup"] = password

            # Create the dictionary with the data to send in the email
            content = {"username": username, "email": email}

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
    file_path = os.getcwd()+f"/database/accounts/{id}/{id}.png"

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
        username = session["username"]
    
        # Return the catalog page
        return render_template("catalog.html", username=username, id=id)


@views.route('/products')
def products():

    products = get_all_products()
    return jsonify(products)
