$(document).ready(function(){
    $("#cartsubmission").submit(function(e){
        e.preventDefault(); // Prevent default form submission

        var formData = new FormData(this); // Get form data, including files

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/cart/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    alert("item added to cart")
                    document.getElementById("count_banner").innerHTML = response.count;
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                $("#signupError").html("Something went wrong. Please try again.");
            }
        });
    });
});


function quantity(action,id){
    $.get("/quantity/"+action+"/"+id+"/", function(data, status)
   {
   if (data.success){
   document.getElementById("var-value-"+id).innerHTML = data.quantity;
   document.getElementById("sub-value-"+id).innerHTML = data.sub_total;
   document.getElementById("total").innerHTML = data.total;
   document.getElementById("count_banner").innerHTML = data.count;
   } else {
    console.log("unknown error occured")
   }
   });
   }


function delete_product(id){
    $.get("/delete/"+id+"/", function(data, status)
   {
   if (data.success){
   const row = document.getElementById("row-"+data.id);
   if (row) {
   row.remove()
   document.getElementById("total").innerHTML = data.total;
   document.getElementById("count_banner").innerHTML = data.count;
   }
   } else {
    console.log("unknown error occured")
   }
   });
   }
async function checklogin_status() {
    try {
        const response = await $.get('/logged-in-check');
        if (response.success) {
            return response.is_logged_in;
        } else {
            console.log("unknown error occurred");
            return false;
        }
    } catch (error) {
        console.error("Request failed:", error);
        return false;
    }
}

document.getElementById('checkout-button').addEventListener('click', async function () {
    const isLoggedIn = await checklogin_status();

    if (isLoggedIn) {
        if (navigator.onLine) {
            window.location.href = '/create-checkout-session/';
        } else {
            alert('No internet connection. Please check your connection and try again.');
        }
    } else {
        document.getElementById("loginModal").style.display = "flex";
    }
});

