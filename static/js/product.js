// Function to fetch reviews and ratings and populate the review list and average rating
function fetchReviewsAndRating() {
    console.log(productId)

    fetch(`/get_reviews/${productId}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing reviews
            console.log(data);
            const reviewList = document.getElementById('reviewList');
            reviewList.innerHTML = '';


            let averageRatingCount = 0;
            // Display reviews  
            data.forEach(review => {
                console.log(review);
                displayReview(review);
                averageRatingCount += review.rating;
            });

            averageRatingCount = averageRatingCount / data.length;

            // Round to 1 decimal place
            averageRatingCount = Math.round(averageRatingCount * 10) / 10;

            // Display the average rating
            document.getElementById('averageRating').textContent = averageRatingCount + ' ★';
        })
        .catch(error => {
            console.error('Error fetching reviews and ratings:', error);
        });
}

// Call the function after the page has loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchReviewsAndRating();
});




// Add an event listener to the "Back to Catalog" link
document.getElementById('backToCatalog').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default link behavior
    history.go(-1); // Go back to the previous page
});


// Function to add a user review
function addReview(event) {
    event.preventDefault(); // Prevent the default form submission

    // Collect form data
    const userReview = document.getElementById('userReview').value;
    const rating = parseInt(document.getElementById('rating').value);

    if (!userReview || isNaN(rating)) {
        alert('Please provide a review and rating.');
        return;
    }

    const formData = new FormData();
    formData.append('userReview', userReview);
    formData.append('rating', rating);

    // Send a POST request to the server
    fetch(`/add_review/${productId}`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the server responds with data, you can handle it here
        // For example, you can display a success message or update the review list
        console.log('Review added:', data);

        // Clear the review and reset the rating
        document.getElementById('userReview').value = '';
        document.getElementById('rating').value = '1';

        // Display the new review immediately
        displayReview(data);

        // Refresh the average rating
        fetchReviewsAndRating();
    })
    .catch(error => {
        console.error('Error adding review:', error);
    });
}

// Function to display a review in the review list
function displayReview(review) {
    const reviewList = document.getElementById('reviewList');
    const listItem = document.createElement('li');
    listItem.classList.add('review-balloon'); // Add a class for styling

    listItem.innerHTML = `
        <strong>${review.username}</strong> ${review.rating}★<br>
        <p class="review-paragraph">${review.review}</p>
    `;

    // Insert the new review at the beginning of the list
    reviewList.insertBefore(listItem, reviewList.firstChild);
}

// Add an event listener to the form submission
document.getElementById('reviewForm').addEventListener('submit', addReview);