const productContainer = document.querySelector('.product-list');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortOrderSelect = document.getElementById('sortOrder');

const priceSlider = document.getElementById('priceSlider');
const minMaxPriceLabel = document.getElementById('minMaxPriceLabel');

// Initialize the dual-handle slider
noUiSlider.create(priceSlider, {
    start: [0, 1000],
    connect: true,
    range: {
        'min': 0,
        'max': 1000
    }
});

// Function to update price labels based on the slider values
function updatePriceLabels() {
    const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
    minMaxPriceLabel.textContent = `Price Range: $${minPrice} - $${maxPrice}`;
}

// Event listener for the slider
priceSlider.noUiSlider.on('update', () => {
    updatePriceLabels();
    displayProducts(); // Update products when the price range changes
});

// Initial update of price label
updatePriceLabels();

// Function to display products
function displayProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;

    // Fetch products from Flask route
    fetch('/products')
        .then(response => response.json())
        .then(data => {
            // Get the selected sort order
            const sortOrder = sortOrderSelect.value;

            // Filter and sort products based on user input
            const filteredProducts = data.filter(product => {
                const matchesSearch = product.name.toLowerCase().includes(searchTerm);
                const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
                const price = parseFloat(product.price);

                // Check if the product price is within the selected range
                const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
                const isWithinPriceRange = price >= parseFloat(minPrice) && price <= parseFloat(maxPrice);

                return matchesSearch && matchesCategory && isWithinPriceRange;
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
                productCard.innerHTML += `
                    <h3>${product.name}</h3>
                    <p>${product.description}</p>
                    <p class="price">$${product.price}</p>
                `;
                productContainer.appendChild(productCard);
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
}

// Event listeners for filtering, searching, and sorting
searchInput.addEventListener('input', displayProducts);
categoryFilter.addEventListener('change', displayProducts);
sortOrderSelect.addEventListener('change', displayProducts);

// Initial product display
displayProducts();

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


