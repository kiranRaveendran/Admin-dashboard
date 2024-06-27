document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var usernameInput = document.getElementById('username');
        var passwordInput = document.getElementById('password');
        var errorMessage = document.getElementById('error-message');
        var username = usernameInput.value.trim();
        
        var password = passwordInput.value.trim();
        
        var usernamePattern = /^[a-zA-Z0-9_]{3,16}$/; 
        var passwordPattern = /^(?=.*\d)(?=.*[a-zA-Z]).{8,}$/; 

        if (!usernamePattern.test(username)) {
            errorMessage.textContent = 'Invalid username.';
            return;
        }
        if (!passwordPattern.test(password)) {
            errorMessage.textContent = 'Invalid password.';
            return;
        
        }
        errorMessage.textContent = '';

        var formData = new FormData(loginForm);
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


        // Send Ajax request using jQuery
        $.ajax({
            type: 'POST',
            url: '',  // URL to submit the form data to
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    // Redirect to a success page or perform further actions
                    window.location.href = '/dashboard/';
                } else {
                    // Display error message(s) returned by the server
                    if (response.errors) {
                        $('#error-message').text(response.errors);  // Display the first error
                    } else {
                        $('#error-message').text('Invalid username or password.');
                    }
                }
            },
            error: function(xhr, status, error) {  // Log any errors to the console
                errorMessage.textContent = 'Error occurred .Please try again.';
            }
        });
    });
});


   function togglePasswordVisibility(fieldId) {
        const field = document.getElementById(fieldId);
        if (field.type === "password") {
            field.type = "text";
        } else {
            field.type = "password";
        }
    }
