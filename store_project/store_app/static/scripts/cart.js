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
                   console.log("error from backend")
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


document.addEventListner("DOMContentLoaded", function() {
const checkoutbutton = document.getElementById("checkout-button");
const offlinealert = document.getElementById("offline-alert");
checkoutbutton.addEventListner("click",function(event)
{
if (!navigator.onLine){
event.preventDefault();
offlinealert.classList.remove("d-none");
else {
offlinealert.classList.add("d-none");
}
});
});
