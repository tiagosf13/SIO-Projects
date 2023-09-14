from flask import Flask
from views import views
from handlers.DataBaseCoordinator import check_database_table_exists


# Declare the app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.config['SECRET_KEY'] = 'LECI'



if __name__ == '__main__':
    check_database_table_exists("users")
    app.run(debug=True)