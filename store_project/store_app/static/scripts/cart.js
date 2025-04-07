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
   document.getElementById("var-value-"+id).innerHTML = data.quantity;
   document.getElementById("sub-value-"+id).innerHTML = data.sub_total;
   document.getElementById("total").innerHTML = data.total;
   });
   }