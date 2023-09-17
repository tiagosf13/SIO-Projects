function updateCartDisplay() {
    const cartTotal = document.getElementById('cartTotal');
    const cartList = document.getElementById('cartList');

    // Clear existing cart items
    cartList.innerHTML = '';

    // Fetch the user's cart items from the server
    fetch(`/get_cart_items/`) // Replace 'username' with the actual username
        .then(response => response.json())
        .then(data => {
            let total = 0;
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
    items: [], // Array to store cart items
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

                // Function to add a product to the cart
                // Check if the product is already in the cart and update the quantity
                /* const existingItem = this.items.find((item) => item.product.id === product.id);
                if (existingItem) {
                    console.log(existingItem.quantity);
                    console.log(product.quantity);
                    console.log("aqui")
                    existingItem.quantity += product.quantity;
                } else {
                    // If not in the cart, add it as a new item
                    console.log("aqui2")
                    console.log(product.quantity);
                    this.items.push({ product, quantity: product.quantity });
                } */

                // Handle a successful response from the server
                console.log(`Added product ${product.id} to the cart.`);
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

                // Function to add a product to the cart
                // Check if the product is already in the cart and update the quantity
                /* const existingItem = this.items.find((item) => item.product.id === product.id);
                if (existingItem && existingItem.quantity > 0 && existingItem.quantity > product.quantity) {
                    existingItem.quantity -= product.quantity;
                    console.log(existingItem.quantity);
                } else {
                    this.items = this.items.filter((item) => item.product.id !== product.id); // Remove the item from the cart
                } */

                // Handle a successful response from the server
                console.log(`Removed product ${product.id} from the cart.`);
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
        //remove all products from the cart
        this.items = [];
        // Make an AJAX request to the server to remove the product from the user's cart
        try {
            const response = await fetch(`/remove_all_items_cart`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
            }
            });

            if (response.ok) {
                // Handle a successful response from the server
                console.log(`Removed all products from the cart.`);
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

// Append the buttons and input to the product card
productCard.appendChild(addToCartButton);
productCard.appendChild(removeItemButton);

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

    if (event.target.classList.contains('remove-from-cart-button')) {
        // Get the product information associated with the clicked button
        const productCard = event.target.closest('.product-card');
        const productId = productCard.querySelector('p[style="color: red"]').textContent.split('ID: ')[1];

        // Check if the cart is empty before trying to remove
        if (shoppingCart.items.length > 0) {
            // Remove the product from the cart by passing only the productId
            shoppingCart.removeProduct(productId);
        }
    }
});
