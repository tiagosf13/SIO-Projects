const productContainer = document.querySelector('.product-list');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortOrderSelect = document.getElementById('sortOrder');
const stockSelect = document.getElementById('stockSelect');

const priceSlider = document.getElementById('priceSlider');
const minMaxPriceLabel = document.getElementById('minMaxPriceLabel');

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

// Function to update price labels based on the slider values
function updatePriceLabels() {
    const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
    minMaxPriceLabel.textContent = `Price Range: $${minPrice} - $${maxPrice}`;
}

function displayProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    

    // Fetch products from Flask route
    fetch('/products')
        .then(response => response.json())
        .then(data => {
            // Get the selected sort order
            const sortOrder = sortOrderSelect.value;
            const numberStock = stockSelect.value;
            
            // Filter and sort products based on user input
            const filteredProducts = data.filter(product => {
                const matchesSearch = product.name.toLowerCase().includes(searchTerm) || product.id.toString().toLowerCase().includes(searchTerm);
                
                const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
                const price = parseFloat(product.price);

                // Check if the product price is within the selected range
                const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
                const isWithinPriceRange = price >= parseFloat(minPrice) && price <= parseFloat(maxPrice);

                // Check if the product is in stock
                if (numberStock === 'inStock') {
                    stockStatus = product.stock > 0;
                }
                else{
                    stockStatus = product.stock <= 0;
                }

                return matchesSearch && matchesCategory && isWithinPriceRange&& stockStatus;
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
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');
                const imgElement = document.createElement('img');
                imgElement.src = `/get_image/catalog/${product.id}.png`;
                imgElement.alt = product.name;
                productCard.appendChild(imgElement);
                // Add a click event listener to the product card
                productCard.addEventListener('click', () => redirectToProductPage(product.id));
                if (product.stock <= 0  || product.stock == null) {
                    productCard.innerHTML += `
                    <h3>${product.name}</h3>
                    <p>${product.description}</p>
                    <p style="color: red">ID: ${product.id}</p>
                    <p>Stock: 0</p>
                    <p class="price" style="color: green">$${product.price}</p>
                `;
                } else{
                    productCard.innerHTML += `
                    <h3>${product.name}</h3>
                    <p class="product-details">${product.description}</p>
                    <p style="color: red">ID: ${product.id}</p>
                    <p>Stock: ${product.stock}</p>
                    <p class="price" style="color: green">${product.price} €</p>
                `;
                }
                
                productContainer.appendChild(productCard);
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

    // Initial update of price label
    updatePriceLabels();
}


// Call displayProducts once when the page loads
fetch('/products')
    .then(response => response.json())
    .then(data => {
        const maxProductPrice = Math.max(...data.map(product => parseFloat(product.price)));
        initPriceSlider(maxProductPrice); // Initialize the slider with maxProductPrice
        displayProducts(); // Fetch and display products immediately
    })
    .catch(error => {
        console.error('Error fetching products:', error);
    });



// Event listeners for filtering, searching, and sorting
searchInput.addEventListener('input', displayProducts);
categoryFilter.addEventListener('change', displayProducts);
sortOrderSelect.addEventListener('change', displayProducts);
categoryFilter.addEventListener('change', displayProducts);
stockSelect.addEventListener('change', displayProducts);


function goToLogin() {

    // Redirect to the profile page
    window.location.href = "/login";
}

function goToSignUp() {

    // Redirect to the profile page
    window.location.href = "/signup";
}

function goToCatalogIndex() {
    
        // Redirect to the profile page
        window.location.href = "/";
}



// Function to show the popup
function showPopup(name) {
    const popup = document.getElementById(name);
    popup.style.display = "block";
}

// Function to close the popup
function closePopup(name) {
    const popup = document.getElementById(name);
    popup.style.display = "none";
}

// Event listener to show the Add Product popup when "Add Product" is clicked
const addProductLink = document.getElementById("add_product");
addProductLink.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default behavior of the anchor link
    showPopup("addProductPopup");
});

// Event listener to show the Remove Product popup when "Remove Product" is clicked
const removeProductLink = document.getElementById("remove_product");
removeProductLink.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default behavior of the anchor link
    showPopup("removeProductPopup");
});


// Event listener to show the Remove Product popup when "Remove Product" is clicked
const editProductLink = document.getElementById("edit_product");
editProductLink.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default behavior of the anchor link
    showPopup("editProductPopup");
});


// Event listener to close the Add Product popup when the close button is clicked
const closeButtonAdd = document.querySelector(".popup#addProductPopup .close");
closeButtonAdd.addEventListener("click", function() {
    closePopup("addProductPopup");
});

// Event listener to close the Remove Product popup when the close button is clicked
const closeButtonRemove = document.querySelector(".popup#removeProductPopup .close");
closeButtonRemove.addEventListener("click", function() {
    closePopup("removeProductPopup");
});

// Event listener to close the Remove Product popup when the close button is clicked
const editButtonRemove = document.querySelector(".popup#editProductPopup .close");
closeButtonRemove.addEventListener("click", function() {
    closePopup("editProductPopup");
});


function redirectToProductPage(productId) {
    // Redirect to the product page with the product ID
    window.location.href = `/product/${productId}`;
}