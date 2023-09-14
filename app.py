from flask import Flask
from views import views
from handlers.DataBaseCoordinator import check_database_table_exists


# Declare the app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.config['SECRET_KEY'] = 'LECI'



if __name__ == '__main__':
    check_database_table_exists("users")
    check_database_table_exists("products")
    app.run(debug=True)

"""
#   1. User Management: 
        • User registration and login ========================================> DONE
        • User profiles               ========================================> DONE
        • Password management (reset, change) ================================> DONE
        • User roles and permissions (admin, customer)
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
        • Tracking product availability (in-stock, out-of-stock)
        • Managing product quantities
    6. Order History:
        • View and track past orders
        • Reorder from order history
    7. Reviews and Ratings:
        • Allow customers to rate and review products
        • Display average ratings and reviews 
"""
