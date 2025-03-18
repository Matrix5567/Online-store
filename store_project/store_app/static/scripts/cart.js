function cart() {
        $.ajax({
            url: 'http://127.0.0.1:8000/cart/', // Django signup URL
            success: function(response) {
                if (response.success) {
                   console.log("success fom backend")
                    window.location.href="/cartpage/"
                } else {
                   document.getElementById("loginModal").style.display = "flex";
                }
            },
            error: function() {
                $("#loginemailError").html("Something went wrong. Please try again.");
            }
        });

    }