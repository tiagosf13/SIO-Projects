from flask import Flask
from views import views
from handlers.DataBaseCoordinator import check_database_table_exists
import os


# Declare the app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.config['SECRET_KEY'] = 'LECI'

app_root = '/home/tiago/Services/SIO-Project'
os.chdir(app_root)



if __name__ == '__main__':
    os.chdir(app_root)  # Set the working directory again in case it changed
    check_database_table_exists("users")
    check_database_table_exists("products")
    check_database_table_exists("reviews")
    CORS(app)
    app.run(debug=True, host='0.0.0.0', port='80')

"""
    1. User Management: 
        • User registration and login ========================================> DONE
        • User profiles               ========================================> DONE
        • Password management (reset, change) ================================> DONE
        • User roles and permissions (admin, customer) =======================> DONE
    2. Product Catalog:
        • Product listings with details (name, description, price, images) ===> DONE
        • Product categories and filters =====================================> DONE
        • Product search functionality =======================================> DONE
    3. Shopping Cart:
        • Cart management (add, remove, update items)
        • Cart total calculation
        • Save cart for later or wish list
    4. Checkout Process:
        • Shipping and billing information collection
        • Payment processing (credit card, PayPal, etc.)
        • Order confirmation and receipt generation
    5. Inventory Management:
        • Tracking product availability (in-stock, out-of-stock) =============> DONE
        • Managing product quantities ========================================> DONE
    6. Order History:
        • View and track past orders
        • Reorder from order history
    7. Reviews and Ratings:
        • Allow customers to rate and review products ========================> DONE
        • Display average ratings and reviews ================================> DONE
"""
