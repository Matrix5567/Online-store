from django.http import HttpResponse , JsonResponse
from django.shortcuts import render
from . models import Products, ProductsSubimage

# Create your views here.


def home(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def shop(request):
    products = Products.objects.all()
    return render(request,'shop.html',{'product':products})

def single(request,id):
    product_single = ProductsSubimage.objects.filter(product=id)
    return render(request,'shop-single.html')