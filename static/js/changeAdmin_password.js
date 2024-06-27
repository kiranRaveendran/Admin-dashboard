

    function showModal() {
        document.getElementById('changePasswordModal').classList.remove('hidden');
         
    }

    function hideModal() {
        document.getElementById('changePasswordModal').classList.add('hidden');
       
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).ready(function() {
        $('#changePasswordForm').on('submit', function(event) {
            event.preventDefault();

            $.ajax({
                type: 'POST',
                url: '/change_password/',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        $('#message-container').html('<div class="alert alert-success text-white bg-green-600">' + response.message + '</div>');
                        $('#changePasswordForm')[0].reset();
                        setTimeout(function() {
                                hideModal()
                                }, 3000); 
                    } else {
                        $('#changePasswordForm').html(response.form_html);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
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


function add_modal(){
            var variable_change =document.getElementById('changePasswordModal')
            variable_change.classList.add('hidden')
        }

function togglePasswordVisibility(fieldId) {
            const field = document.getElementById(fieldId);
            const fieldType = field.getAttribute('type') === 'password' ? 'text' : 'password';
            field.setAttribute('type', fieldType);
        }

document.addEventListener("DOMContentLoaded", function() {
            var alertMessage = document.getElementById("alert-message");
            if (alertMessage) {
                setTimeout(function() {
                    alertMessage.style.display = "none";
                }, 3000); 
            }
        });