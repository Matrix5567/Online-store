$(document).ready(function () {
    $('#searchForm').submit(function (e) {
        e.preventDefault(); // Prevent normal form submission

        var formData = new FormData(this); // Gather form data including CSRF token

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/search/",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    const container = $(".row").eq(2); // Target the row containing products
                    container.empty(); // Clear existing products

                    response.page_obj.forEach(product => {
                        const productHTML = `
                        <div class="col-md-4">
                            <div class="card mb-4 product-wap rounded-0">
                                <div class="card rounded-0">
                                    <img class="card-img rounded-0 img-fluid" style="width:100%;height:250px;object-fit:cover;" src="${product.product_image}">
                                    <div class="card-img-overlay rounded-0 product-overlay d-flex align-items-center justify-content-center">
                                        <ul class="list-unstyled">
                                            <li><a class="btn btn-success text-white mt-2" href="/single/${product.id}/"><i class="far fa-eye"></i></a></li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="card-body" style="min-height:129px;">
                                    <a href="/single/${product.id}/" class="h3 text-decoration-none">${product.product_name}</a>
                                    <h6 class="h3 text-decoration-none">${product.product_brand_name}</h6>
                                    <ul class="w-100 list-unstyled d-flex justify-content-between mb-0">
                                        <li class="pt-2">
                                            <span class="product-color-dot color-dot-red float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-blue float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-black float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-light float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-green float-left rounded-circle ml-1"></span>
                                        </li>
                                    </ul>
                                    <p class="text-center mb-0">₹${product.unit_product_price}</p>
                                </div>
                            </div>
                        </div>`;
                        container.append(productHTML);
                    });
                } else {
                    console.log("No products found or unauthorized.");
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX error:", error);
            }
        });
    });
});