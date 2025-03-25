//$(document).ready(function () {
//    let quantityElement = $("#var-value"); // Quantity display
//
//    // Function to send AJAX request
//    function updateCart(action = null) {
//        let quantity = parseInt(quantityElement.text());
////        let unitPrice = parseFloat($("#unit-price").val()); // Get unit price
//
//        // Send only current quantity and action; backend will calculate new values
//        let formData = new FormData($("#cartsubmission")[0]);
//        formData.append("quantity", quantity);
//        if (action) formData.append("action", action); // Only add action if inc/dec
//
//        $.ajax({
//            type: "POST",
//            url: "http://127.0.0.1:8000/cart/", // Single URL for all actions
//            data: formData,
//            processData: false,
//            contentType: false,
//            success: function (response) {
//                if (response.success) {
//                       console.log("from backOO>>>>",response)
////                    quantityElement.text(response.new_quantity); // Update quantity from backend
////                    $("#total-price").text(response.new_price); // Update price from backend
//                }
//            },
//            error: function () {
//                  console.log(">>>>>>FFFFFFF",error)
////                alert("Something went wrong>>>>>>>>>>>>>>>>>>>>>>!");
//            }
//        });
//    }
//
//    // Increase and Decrease Quantity
//    $(".btn-success").click(function () {
//        let action = $(this).attr("id") === "btn-plus" ? "inc" : "dec";
//        updateCart(action);
//    });
//
//    // Add to Cart Submission
//    $("#cartsubmission").submit(function (e) {
//        e.preventDefault(); // Prevent default form submission
//        updateCart(); // Call without action for form submission
//    });
//});


$(document).ready(function () {
    let quantityElement = $("#var-value"); // Quantity display

    // Function to send AJAX request
    function updateCart(action = null) {
        let quantity = parseInt(quantityElement.text());
        let formData = new FormData($("#cartsubmission")[0]);
        formData.append("quantity", quantity);
        if (action) formData.append("action", action);

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/cart/",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    console.log("from backOO>>>>", response);
//                    quantityElement.text(response.new_quantity);
//                    $("#total-price").text(response.new_price);
                }
            },
            error: function (xhr, status, error) {
                console.log("Error:", error);
            }
        });
    }

    // Prevent duplicate event bindings
    $("#btn-minus").off("click").on("click", function () {
        let action = null;
        if($(this).attr("id")==="btn-minus"){
            action = 'dec'
        }
     updateCart(action);
    });

        $("#btn-plus").off("click").on("click", function () {
        let action = null;
        if($(this).attr("id")==="btn-plus"){
            action = 'inc'
        }
     updateCart(action);
    });

    // Prevent duplicate form submission
    $("#cartsubmission").off("submit").on("submit", function (e) {
        e.preventDefault();
        updateCart();
    });
});