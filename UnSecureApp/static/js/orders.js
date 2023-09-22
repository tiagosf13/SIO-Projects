const reorderButtons = document.querySelectorAll('.reorderButton');
reorderButtons.forEach(button => {
    button.addEventListener('click', function () {
        const productDetails = this.getAttribute('data-product');
        console.log('Product Details:', productDetails);
        try {
            const parsedProductDetails = JSON.parse(productDetails);
            reorder_item(parsedProductDetails);
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    });
});

async function reorder_item(product) {
    try {
        const response = await fetch(`/add_item_cart/${product.product_id}`, {
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
            // get the error message from the response,
            const errorMessage = await response.json();
            // then display it on the page
            alert('Failed to add product to the cart. ' + errorMessage.error);
            // Handle errors or server responses here
            console.error('Failed to add product to the cart.');
        }
    } catch (error) {
        console.error('Error adding product to the cart:', error);
    }
}