
document.addEventListener('DOMContentLoaded', function() {
    fetch('/onload/')  // Call the backend API
        .then(response => response.json())
        .then(data => {
            if (data.success && data.user.image) {
                document.getElementById('std_profile_pic').src=data.user.image;    // onload function for user details
                document.getElementById("logout").style.display = "block";
                document.getElementById("count_banner").innerHTML = data.count;
            } else {
            document.getElementById("count_banner").innerHTML = data.count;
            }
        })
        .catch(error => console.error('not logged in',error));
});



async function openModal() {
        const response = await $.get('/logged-in-check');
        if (!response.is_logged_in){
        document.getElementById("loginModal").style.display = "flex";
        }
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
                    document.getElementById("count_banner").innerHTML = response.count;
                    const cartBody = document.getElementById("cart-body");
                    cartBody.innerHTML = "";  // Clear existing content

    const cartItems = response.cart_items;
    for (const productId in cartItems) {
        const item = cartItems[productId];

        const row = `
        <tr id="row-${item.product_id}">
            <td><img src="${item.product_image}" alt="Product" width="70"></td>
            <td>${item.product_name}</td>
            <td>${item.product_unit_price}</td>
            <td>
                <button id="${item.product_id}" onclick="quantity('dec', this.id)" class="btn btn-success btn-sm">-</button>
                <span class="mx-2" id="var-value-${item.product_id}">${item.product_quantity}</span>
                <button id="${item.product_id}" onclick="quantity('inc', this.id)" class="btn btn-success btn-sm">+</button>
            </td>
            <td id="sub-value-${item.product_id}">${item.prod_total_price}</td>
            <td>
                <button id="${item.product_id}" onclick="delete_product(this.id)" class="btn btn-danger btn-sm">X</button>
            </td>
        </tr>`;

        cartBody.innerHTML += row;
    }
        document.getElementById("total").innerHTML = response.total;
         document.getElementById("count_banner").innerHTML = response.count;
                } else {
                    let errors = response.errors;
                    if (errors) {
                    $("#loginemailError").html(errors);
                    }
                }
            },
            error: function() {
                $("#loginemailError").html("Something went wrong. Please try again.");
            }
        });
    });
});