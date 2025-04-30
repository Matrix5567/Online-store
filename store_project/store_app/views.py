from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from . common import fetch_product_subimage, fetch_single_product, categories, register, json_serializable\
    , get_cart, increment_decrement, cart_count, delete_product, user_total, pagenation, show_filter
from . validators import name_validator, email_validator, phone_validator, image_validator, password_validator\
,category_url_validator, fetch_single_product_validator,fetch_product_subimage_validator
import stripe
from .models import Cart, Products , Categories
from django.conf import settings


# Create your views here.

def check_is_logged_in(request):
    return JsonResponse({'success': True, 'is_logged_in': request.user.is_authenticated})


def onload(request):
    if request.user.is_authenticated:
        user_data = json_serializable(request.user, request=request)
        return JsonResponse({'success': True, 'user': user_data,'count':cart_count(request)})
    else:
        return JsonResponse({'success': False,'count':cart_count(request)})


def signup(request):
    if request.method == 'POST':
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
    else:
        return JsonResponse({'success': False})



def user_login(request):
    if request.method == 'POST':
        login_email = request.POST.get('email')
        login_password = request.POST.get('password')
        user = authenticate(request, email=login_email, password=login_password)
        if user is not None:
            login(request,user)
            user_data = json_serializable(user,request=request)
            return JsonResponse ({'success':True,'user':user_data,'count':cart_count(request),
                              'cart_items':get_cart(submitt=False,user=request.user.is_authenticated,request=request),
                              'total':user_total(request.session.get('cart', {}),request)})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid login credentials'})
    else:
        return JsonResponse({'success': False, 'errors': 'Error'})


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
        if category_url_validator(key):
            products = categories(URL=key)
            for product in products:
                if fetch_single_product_validator(id=False,product_type=product):
                    all_products.extend(fetch_single_product(product_type=product, id=False))
                    return render(request, 'shop.html', {'page_obj':pagenation(request,all_products),
                                                         'section_name':key,'categories':show_filter()['categories']
                                                         ,'brands':show_filter()['brands']})
                else:
                    return HttpResponse('Unauthorized')
        else:
            return HttpResponse('Unauthorized')
    else:
        all_products = fetch_single_product(product_type=False, id=False)
        return render(request, 'shop.html',{'page_obj':pagenation(request,all_products),'section_name':key,
                                            'categories': show_filter()['categories'],'brands': show_filter()['brands']})

def single(request,id):
    if fetch_single_product_validator(id=id,product_type=False) and fetch_product_subimage_validator(id):
        return render(request,'shop-single.html',{'sub_images':fetch_product_subimage(id),
                                              'product':fetch_single_product(id=id,product_type=False)})
    else:
        return HttpResponse('Unauthorized')


def cartpage(request):
    if request.method == 'POST':
        if get_cart(submitt=request.POST,user=request.user.is_authenticated,request=request):
            return JsonResponse({'success':True,'count':cart_count(request)})
        else:
            return JsonResponse({'success': False, 'message':'Item already present in cart'})
    else:
        return render(request,'cart.html',{'cart_items':get_cart(submitt=False,user=request.user.is_authenticated,request=request),
                                           'total':user_total(request.session.get('cart', {}),request)})

def quantity(request,action,id):
    if fetch_single_product_validator(id=id, product_type=False):
        return increment_decrement(action=action,id=id,request=request)
    else:
        return HttpResponse('Unauthorized')

def delete(request,id):
    if fetch_single_product_validator(id=id, product_type=False):
        return delete_product(request,id)
    else:
        return HttpResponse('Unauthorized')


def total_quantity(request):
    total_qty = 0
    if request.user.is_authenticated:
        qty=Cart.objects.filter(user=request.user)
        for quantity in qty:
            total_qty+=int(quantity.quantity)
    return total_qty



@login_required()
def checkout(request):
    if request.user.is_authenticated and int(user_total(cart=False,request=request))*100>0 :
        line_items=[]

        items=Cart.objects.filter(user=request.user)
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'unit_amount':item.product.unit_product_price*100,
                    'product_data': {
                        'name': item.product.product_name,
                        'images': [request.build_absolute_uri(item.product.product_image.url)] if item.product.product_image else [],
                    },
                },
                'quantity': item.quantity,
            })

        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            metadata={"product_id":request.user},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
            customer_email=request.user,
            billing_address_collection='required',
            customer_creation='always',
        )
        items.delete()
        return redirect(checkout_session.url)
    else:
        return redirect('home')

@login_required()
def success(request):
    return render(request,'success.html')

def custom_404(request,exception):
    return render(request,'404.html',status=404)


def search(request):
    if request.method == 'POST':
        search_word = request.POST.get('search')
        # section = request.POST.get('section')
        product_list = []
        results = Products.objects.filter(Q(product_name__icontains=search_word) | Q(product_description__icontains=search_word) |
                                  Q(product_brand_name__icontains=search_word))
        for product in pagenation(request, results).object_list:
                product_list.append({
                'id': product.id,
                'product_name': product.product_name,
                'product_brand_name': product.product_brand_name,
                'product_image': product.product_image.url,
                'unit_product_price': product.unit_product_price,
                })
        return JsonResponse({'success':True,'page_obj':product_list,'section_name':'Search Results'})
    else:
        return JsonResponse({'success':False,'results':'unauthorized'})

def filter(request):
    categories = Categories.objects.values_list('product_Type_name', flat=True).distinct()
    brands = Products.objects.values_list('product_brand_name', flat=True).distinct()
    return render(request, 'shop.html', {
            'categories': categories,
            'brands': brands,
        })