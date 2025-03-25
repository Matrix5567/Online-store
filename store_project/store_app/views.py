from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . common import  fetch_product_subimage, fetch_single_product, categories, register, json_serializable\
    , get_cart
from . validators import name_validator, email_validator, phone_validator, image_validator, password_validator


# Create your views here.




def onload(request):
    if request.user.is_authenticated:
        user_data = json_serializable(request.user, request=request)
        return JsonResponse({'success': True, 'user': user_data})
    else:
        return JsonResponse({'success': False})


def signup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    image = request.FILES.get('image')
    password = request.POST.get('password')
    name_error = name_validator(name)
    email_error = email_validator(email)
    phone_error = phone_validator(phone)
    image_error = image_validator(image)
    password_error = password_validator(password)
    errors = {}
    if name_error:
        errors['name']=name_error
    if email_error:
        errors['email']=email_error
    if phone_error:
        errors['phone'] = phone_error
    if image_error:
        errors['image'] = image_error
    if password_error:
        errors['password'] = password_error
    if errors:
        return JsonResponse({'success':False,"errors":errors})
    register_success = register(name,phone,email,image,password)
    if register_success:
        return JsonResponse({'success':True})


def user_login(request):
    login_email = request.POST.get('email')
    login_password = request.POST.get('password')
    user = authenticate(request, email=login_email, password=login_password)
    if user is not None:
        login(request,user)
        user_data = json_serializable(user,request=request)
        return JsonResponse ({'success':True,'user':user_data})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid login credentials'})

def user_logout(request):
    logout(request)
    return redirect(home)


def home(request):
    return render(request,'index.html',{'product':categories(URL=False),
                                        'featured':fetch_single_product(id=False,product_type=False)})


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
    if request.method == 'POST':
        if request.POST.get('action') == 'inc':
            get_cart(inc=request.POST.get('action'),dec=False,submitt=False)
            return JsonResponse({'success': True})
        elif request.POST.get('action') == 'dec':
            get_cart(inc=False, dec=request.POST.get('action'), submitt=False)
            return JsonResponse({'success': True})
        else:
            get_cart(inc=False, dec=False, submitt=request.POST)
            return JsonResponse({'success':True})
    else:
        return render(request,'cart.html',{'cart_items':get_cart(inc=False,dec=False,submitt=False)})

