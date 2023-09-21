let currentWidget = 1;
const widgets = document.querySelectorAll('.checkout-widget');
const widgetButtons = document.querySelectorAll('.widget-button');

document.getElementById('submitButton').addEventListener('click', submitOrder);

// JavaScript to handle widget navigation
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the widget state when the page loads
    for (let i = 0; i < widgets.length; i++) {
        if (i === currentWidget - 1) {
            widgets[i].classList.add('active-widget');
        } else {
            widgets[i].classList.add('prev-widget');
        }
    }

    // Initialize the widget buttons opacity
    updateWidgetButtonOpacity();
});

function showWidget(widgetNumber) {
    if (widgetNumber >= 1 && widgetNumber <= widgets.length) {
        widgets[currentWidget - 1].classList.remove('active-widget');
        widgets[currentWidget - 1].classList.add('prev-widget');
        widgets[widgetNumber - 1].classList.remove('prev-widget');
        widgets[widgetNumber - 1].classList.add('active-widget', 'next-widget');
        currentWidget = widgetNumber;

        // Update widget buttons opacity
        updateWidgetButtonOpacity();
    }
}

function nextWidget() {
    if (currentWidget < widgets.length) {
        widgets[currentWidget - 1].classList.remove('active-widget');
        widgets[currentWidget - 1].classList.add('prev-widget');
        widgets[currentWidget].classList.remove('prev-widget');
        widgets[currentWidget].classList.add('active-widget', 'next-widget');
        currentWidget++;

        // Update widget buttons opacity
        updateWidgetButtonOpacity();
    }
}

function submitOrder(event) {
    event.preventDefault();

    // Get form data
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const address = document.getElementById('address').value;
    const creditCard = document.getElementById('creditCard').value;
    const expirationDate = document.getElementById('expirationDate').value;
    const cvv = document.getElementById('cvv').value;

    // Create an object to hold the form data
    const formData = {
        'firstName': firstName,
        'lastName': lastName,
        'address': address,
        'creditCard': creditCard,
        'expirationDate': expirationDate,
        'cvv': cvv
    };

    // Send the form data to the server using an AJAX POST request
    fetch('/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse the response body as JSON
        } else {
            throw new Error('Order failed to submit.'); // Throw an error if the response is not ok
        }
    })
    .then(data => {
        // Handle the response data
        alert('Order submitted successfully!');
        window.location.href = `/thanks`;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Order failed to submit.');
    });
}


function updateWidgetButtonOpacity() {
    for (let i = 0; i < widgetButtons.length; i++) {
        if (i === currentWidget - 1) {
            widgetButtons[i].classList.add('active-button');
        } else {
            widgetButtons[i].classList.remove('active-button');
        }
    }
}
