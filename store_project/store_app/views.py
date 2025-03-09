from django.shortcuts import render
from . common import  fetch_product_subimage, fetch_single_product, categories
# Create your views here.


def home(request):
    return render(request,'index.html',{'product':categories(URL=False)})


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def shop(request,key=None):
    all_products = []
    if key:
        products = categories(URL=key)
        for product in products:
            all_products.extend(fetch_single_product(product_type=product, id=False))
        return render(request, 'shop.html', {'product': all_products})
    else:
        return render(request, 'shop.html', {'product': fetch_single_product(product_type=False, id=False)})

def single(request,id):
    return render(request,'shop-single.html',{'sub_images':fetch_product_subimage(id),
                                              'product':fetch_single_product(id=id,product_type=False)})

def cartpage(request):
    return render(request,'cart.html')