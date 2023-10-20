function previewImage() {
    var preview = document.querySelector('.preview-image');
    var file = document.querySelector('input[type=file]').files[0];
    var reader = new FileReader();

    reader.addEventListener("load", function () {
        preview.src = reader.result;
        preview.style.display = 'block'; // display the preview image after loading it
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}

function validateForm() {
    var password = document.getElementById("psw").value;
    var repeatPassword = document.getElementById("psw-repeat").value;
    var oldPassword = document.getElementById("old-psw").value;

    if (password !== "" && repeatPassword !== "" && oldPassword !== "") {
        if (password !== repeatPassword) {
            document.getElementById("error-message-psw").innerHTML = "Passwords don't match";
            return false;
        }
    }

    var username = document.getElementById("username").value;
    var usernameExists = false;  // flag to indicate whether username exists
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if (response.exists) {
                document.getElementById("error-message-username").innerHTML = "Username already exists.";
                usernameExists = true;  // set flag to true
            }
        }
    };
    xhr.open("POST", "/check_username", false);  // make request synchronous
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("username=" + encodeURIComponent(username));

    if (usernameExists) {
        return false;  // don't submit form if username exists
    }
    

    var email = document.getElementById("email").value;
    var emailExists = false;  // flag to indicate whether username exists
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if (response.exists) {
                document.getElementById("error-message-email").innerHTML = "Email already exists.";
                emailExists = true;  // set flag to true
            }
        }
    };
    xhr.open("POST", "/check_email", false);  // make request synchronous
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("email=" + encodeURIComponent(email));

    if (emailExists) {
        return false;  // don't submit form if username exists
    }
    
    return true;  // submit form if username doesn't exist
}


function goToCatalogPage(id) {
    // Redirect to the profile page without the space character
    window.location.href = '/catalog/' + id;
}

