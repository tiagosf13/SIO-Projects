document.getElementById('checkoutButton').addEventListener('click', function(event) {

    event.stopPropagation(); // Stop the click event from propagating to the product card
    window.location.href = '/checkout';

});

function updateCartDisplay() {
    const cartTotal = document.getElementById('cartTotal');
    const cartList = document.getElementById('cartList');

    // Clear existing cart items

    // Fetch the user's cart items from the server
    fetch(`/get_cart_items/`) // Replace 'username' with the actual username
        .then(response => response.json())
        .then(data => {
            let total = 0;
            cartList.innerHTML = '';
            // Iterate through the retrieved cart items and add them to the cart list
            data.forEach((cartItem) => {
                
                const cartItemElement = document.createElement('li');
                cartItemElement.classList.add('list-group-item');
                cartItemElement.innerText = `${cartItem.name} x${cartItem.quantity}`;
                cartList.appendChild(cartItemElement);
                total += cartItem.price * cartItem.quantity;
            });
            // Update the total price based on the server response
            cartTotal.innerText = `Total: ${total.toFixed(2)} €`;

        })
        .catch(error => {
            console.error('Error fetching cart items:', error);
        });
}



const shoppingCart = {
    addProduct: async function (product) {
    
        // Make an AJAX request to the server to add the product to the user's cart
        try {
            const response = await fetch(`/add_item_cart/${product.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: product.quantity }), // You can adjust the quantity here
            });
    
            if (response.ok) {
                // Call a function to update the cart display
                updateCartDisplay();

            } else {
                product.quantity = 0;
                // Handle errors or server responses here
                console.error('Failed to add product to the cart.');
            }
        } catch (error) {
            console.error('Error adding product to the cart:', error);
        }
    },
    removeProduct: async function (product) {
    
        // Make an AJAX request to the server to remove the product from the user's cart
        try {
            const response = await fetch(`/remove_item_cart/${product.id}`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
            },
                body: JSON.stringify({ quantity: product.quantity }), // You can adjust the quantity here
            });

            if (response.ok) {

                updateCartDisplay();
            } else {
                product.quantity = 0;
                // Handle errors or server responses here
                console.error('Failed to remove product from the cart.');
            }
        } catch (error) {
            console.error('Error removing product from the cart:', error);
        }
    },
    removeAllProducts: async function () {
        // Make an AJAX request to the server to remove the product from the user's cart
        try {
            const response = await fetch(`/remove_all_items_cart`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
            }
            });

            if (response.ok) {
                //clear the shopping cart
                if (window.location.href.includes("checkout")) {
                    window.location.href = '/catalog';
                }
                updateCartDisplay();
            } else {
                // Handle errors or server responses here
                console.error('Failed to remove all products from the cart.');
            }
        } catch (error) {
            console.error('Error removing all products from the cart:', error);
        }
    }
};


// JavaScript to handle the logout button click
document.getElementById('removeAllItems').addEventListener('click', function(event) {
    event.stopPropagation(); // Stop the click event from propagating to the product card
    shoppingCart.removeAllProducts();
});

// Add a click event listener to the product container
productContainer.addEventListener('click', (event) => {
    // Check if the clicked element is an "Add to Cart" button
    if (event.target.classList.contains('add-to-cart-button')) {
        // Get the product information associated with the clicked button
        const productCard = event.target.closest('.product-card');
        const productName = productCard.querySelector('h3').textContent;
        const productId = productCard.querySelector('p[style="color: red"]').textContent.split('ID: ')[1];
        const productPrice = parseFloat(productCard.querySelector('.price').textContent.split(' €')[0]);

        // Add the product to the cart (you may need to adjust this part based on your cart implementation)
        shoppingCart.addProduct({
            id: productId,
            name: productName,
            price: productPrice,
        });
    }
});