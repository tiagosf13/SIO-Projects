from flask import Flask, render_template
from views import views
from handlers.extensions import bcrypt


# Declare the app
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')
app.config['SECRET_KEY'] = 'LECI'
bcrypt.init_app(app)

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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

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
        • Cart management (add, remove, update items) ========================> DONE
        • Cart total calculation =============================================> DONE
        • Save cart for later or wish list ===================================> DONE
    4. Checkout Process:
        • Shipping and billing information collection ========================> DONE
        • Payment processing (credit card, PayPal, etc.) =====================> DONE
        • Order confirmation and receipt generation ==========================> DONE
    5. Inventory Management:
        • Tracking product availability (in-stock, out-of-stock) =============> DONE
        • Managing product quantities ========================================> DONE
    6. Order History:
        • View and track past orders =========================================> DONE
        • Reorder from order history =========================================> DONE
    7. Reviews and Ratings:
        • Allow customers to rate and review products ========================> DONE
        • Display average ratings and reviews ================================> DONE
"""
