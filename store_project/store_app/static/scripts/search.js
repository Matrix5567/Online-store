
$(document).ready(function() {
    $('#searchForm').submit(function(e) {
        e.preventDefault(); // Prevent form from submitting normally

        var formData = new FormData(this); // Gather form data including CSRF token

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/search/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Response from backend:", response);
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", error);
            }
        });
    });
});