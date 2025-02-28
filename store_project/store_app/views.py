from django.http import HttpResponse , JsonResponse
from django.shortcuts import render
from . models import Products, ProductsSubimage, ProductTypes

# Create your views here.


def home(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def shop(request,key):
    if key == 'all':
        all_products = Products.objects.all()
        return render(request,'shop.html',{'product':all_products})
    elif key == 'electronics':
        products = ProductTypes.objects.filter(product_Type_name='Electronics')
        all_products = []
        for product in products:
            get_products = Products.objects.filter(product_type=product)
            all_products.extend(get_products)
        return render(request, 'shop.html', {'product': all_products})
    elif key == 'accessories':
        products = ProductTypes.objects.filter(product_Type_name='Accessories')
        all_products = []
        for product in products:
            get_products = Products.objects.filter(product_type=product)
            all_products.extend(get_products)
        return render(request, 'shop.html', {'product': all_products})
    elif key == 'clothing':
        products = ProductTypes.objects.filter(product_Type_name='Clothing')
        all_products=[]
        for product in products:
            get_products = Products.objects.filter(product_type=product)
            all_products.extend(get_products)
        return render(request, 'shop.html', {'product': all_products})

def single(request,id):
    product_single = ProductsSubimage.objects.filter(product=id)
    products = Products.objects.get(id=id)
    return render(request,'shop-single.html',{'sub_images':product_single,'product':products})