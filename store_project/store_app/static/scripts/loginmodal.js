document.addEventListener('DOMContentLoaded', function() {
    fetch('/onload/')  // Call the backend API
        .then(response => response.json())
        .then(data => {
            if (data.success && data.user.image) {
                document.getElementById('std_profile_pic').src=data.user.image;    // onload function for user details
                document.getElementById("logout").style.display = "block";
            }
        })
        .catch(error => console.error('not logged in',error));
});



function openModal() {
        document.getElementById("loginModal").style.display = "flex";
    }

function closeModal() {
        document.getElementById("loginModal").style.display = "none";
    }


function openSignupModal() {
        document.getElementById("signupModal").style.display = "flex";
    }

    function closeSignupModal() {
        document.getElementById("signupModal").style.display = "none";
    }

//  document.getElementById("signup-image").addEventListener("change", function(event) {
//        const file = event.target.files[0];
//        if (file) {
//            const reader = new FileReader();
//            reader.onload = function(e) {
//                const preview = document.getElementById("image-preview");
//                preview.src = e.target.result;
//                preview.style.display = "block";
//            };
//            reader.readAsDataURL(file);  // image upload preview
//        }
//    });


$(document).ready(function(){
    $("#signupForm").submit(function(e){
        e.preventDefault(); // Prevent default form submission

        var formData = new FormData(this); // Get form data, including files

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/signup/', // Django signup URL
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    alert("Sign-up successful!");
                    document.getElementById("signupModal").style.display = "none"; // Hide modal after successful sign-up
                } else {
                    let errors = response.errors;
                    if (errors.email) {
                    $("#emailError").html(errors.email);
                    }
                    if(errors.name){
                    $("#nameError").html(errors.name);
                    }
                    if(errors.phone){
                    $("#phoneError").html(errors.phone);
                    }
                    if(errors.image){
                    $("#imageError").html(errors.image);
                    }
                     if(errors.password){
                    $("#passwordError").html(errors.password);
                    }
                }
            },
            error: function() {
                $("#signupError").html("Something went wrong. Please try again.");
            }
        });
    });
});







$(document).ready(function(){
    $("#loginForm").submit(function(e){
        e.preventDefault(); // Prevent default form submission

        var formData = new FormData(this); // Get form data, including files

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/login/', // Django signup URL
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success && response.user.image) {
                    document.getElementById("logout").style.display = "block";
                    document.getElementById("loginModal").style.display = "none"; // Hide modal after successful login
                    document.getElementById("std_profile_pic").src= response.user.image;



                } else {
                    let errors = response.errors;
                    if (errors.email) {
                    $("#loginemailError").html(errors.email);
                    }
                    if(errors.password){
                    $("#passwordemailError").html(errors.password);
                    }
                }
            },
            error: function() {
                $("#loginemailError").html("Something went wrong. Please try again.");
            }
        });
    });
});