const productContainer = document.querySelector('.product-list');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortOrderSelect = document.getElementById('sortOrder');

const priceSlider = document.getElementById('priceSlider');
const minMaxPriceLabel = document.getElementById('minMaxPriceLabel');

// Function to update price labels based on the slider values
function updatePriceLabels() {
    const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
    minMaxPriceLabel.textContent = `Price Range: $${minPrice} - $${maxPrice}`;
}



// Function to display products
function displayProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    // Get the product list container
    const productList = document.querySelector('.product-list');
    

    // Fetch products from Flask route
    fetch('/products')
        .then(response => response.json())
        .then(data => {
            // Get the selected sort order
            const sortOrder = sortOrderSelect.value;
            
            // Filter and sort products based on user input
            const filteredProducts = data.filter(product => {
                const matchesSearch = product.name.toLowerCase().includes(searchTerm) || product.id.toString().toLowerCase().includes(searchTerm);
                const inStock = product.stock > 0;
                const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
                const price = parseFloat(product.price);

                // Check if the product price is within the selected range
                const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
                const isWithinPriceRange = price >= parseFloat(minPrice) && price <= parseFloat(maxPrice);


                return matchesSearch && matchesCategory && isWithinPriceRange && inStock;
            });

            // Sort the products based on the selected order
            filteredProducts.sort((a, b) => {
                if (sortOrder === 'asc') {
                    return a.price - b.price;
                } else if (sortOrder === 'desc') {
                    return b.price - a.price;
                }
            });

            // Clear existing products
            productContainer.innerHTML = '';

            filteredProducts.forEach(product => {
                const productContainer = document.createElement('div');
                productContainer.classList.add('product-container');
            
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');
            
                // Add a click event listener to the product card
                productCard.addEventListener('click', () => redirectToProductPage(product.id));
            
                const imgElement = document.createElement('img');
                imgElement.src = `/get_image/catalog/${product.id}.png`;
                imgElement.alt = product.name;
                productCard.appendChild(imgElement);
            
                productCard.innerHTML += `
                    <div class="product-content">
                        <h3>${product.name}</h3>
                        <p class="product-description">${product.description}</p>
                        <p style="color: red">ID: ${product.id}</p>
                        <p class="price" style="color: green">${product.price} €</p>
                    </div>
                `;
            
                const productButtonsContainer = document.createElement('div'); // Container for cart buttons
                productButtonsContainer.classList.add('product-buttons-container');

                // add a quantity input
                const quantityInput = document.createElement('input');
                quantityInput.type = 'number';
                quantityInput.min = 1;
                quantityInput.max = product.stock;
                quantityInput.value = 1;
                quantityInput.classList.add('quantity-input');
            
                const addToCartButton = document.createElement('button');
                addToCartButton.innerHTML = '<i class="fas fa-cart-plus"></i>'; // Font Awesome icon for "Add to Cart"
                addToCartButton.classList.add('cart-button');
                addToCartButton.addEventListener('click', (event) => {
                    event.stopPropagation();
                    product.quantity = 0;
                    product.quantity = parseInt(quantityInput.value);
                    shoppingCart.addProduct(product);
                });
            
                const removeItemButton = document.createElement('button');
                removeItemButton.innerHTML = '<i class="fas fa-trash"></i>'; // Font Awesome icon for "Remove from Cart"
                removeItemButton.classList.add('cart-button');
                removeItemButton.addEventListener('click', (event) => {
                    event.stopPropagation();
                    product.quantity = 0;
                    product.quantity = parseInt(quantityInput.value);
                    shoppingCart.removeProduct(product);
                });
            
                // Append the cart buttons to the container
                productButtonsContainer.appendChild(quantityInput);
                productButtonsContainer.appendChild(addToCartButton);
                productButtonsContainer.appendChild(removeItemButton);
            
                // Append the product card and cart buttons container to the product container
                productContainer.appendChild(productCard);
                productContainer.appendChild(productButtonsContainer);
            
                // Append the product container to the product list
                productList.appendChild(productContainer);
            });                                  
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
}


// Function to initialize the dual-handle slider
function initPriceSlider(maxProductPrice) {
    noUiSlider.create(priceSlider, {
        start: [0, maxProductPrice], // Set the initial range based on maxProductPrice
        connect: true,
        range: {
            'min': 0,
            'max': maxProductPrice
        }
    });

    // Event listener for the slider
    priceSlider.noUiSlider.on('update', () => {
        updatePriceLabels();
        displayProducts(); // Update products when the price range changes
    });
}

function redirectToProductPage(productId) {
    // Redirect to the product page with the product ID
    window.location.href = `/product/${productId}`;
}

// Call displayProducts once when the page loads
fetch('/products')
    .then(response => response.json())
    .then(data => {
        const maxProductPrice = Math.max(...data.map(product => parseFloat(product.price)));
        console.log(maxProductPrice);
        initPriceSlider(maxProductPrice); // Initialize the slider with maxProductPrice
    })
    .catch(error => {
        console.error('Error fetching products:', error);
    });


// Event listeners for filtering, searching, and sorting
searchInput.addEventListener('input', displayProducts);
categoryFilter.addEventListener('change', displayProducts);
sortOrderSelect.addEventListener('change', displayProducts);
categoryFilter.addEventListener('change', displayProducts);

function goToLogin() {

    // Redirect to the profile page
    window.location.href = "/login";
}

function goToSignUp() {

    // Redirect to the profile page
    window.location.href = "/signup";
}


// JavaScript to handle the logout button click
document.getElementById('logoutButton').addEventListener('click', function() {
    // Send a request to the logout route
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin',  // Include cookies in the request
    })
    .then(response => {
        if (response.ok) {
            // Redirect to the login or home page after successful logout
            window.location.href = '/';  // Replace with your actual login or home page URL
        }
    })
    .catch(error => {
        console.error('Error logging out:', error);
    });
});





