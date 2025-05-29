from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from . common import fetch_product_subimage, fetch_single_product, categories, register, json_serializable\
    , get_cart, increment_decrement, cart_count, delete_product, user_total, pagenation, show_filter\
    , history_save
from . validators import name_validator, email_validator, phone_validator, image_validator, password_validator\
,category_url_validator, fetch_single_product_validator,fetch_product_subimage_validator
import stripe
from .models import Cart, Products, Categories, ProductsSubimage, Payment_History, OrderItem
from django.conf import settings
from .decorator import role_required
from .tasks import send_emails_to_users
from .insights import get_top_products
from sklearn.linear_model import LinearRegression
import pandas as pd
from datetime import timedelta

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
            if user.is_admin:
                login(request, user)
                user_data = json_serializable(user, request=request)
                return JsonResponse({'success': True, 'user':user_data })
            else:
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

def about(request):
    return render(request,'about.html')



def shop(request,key=None):
    all_products = []
    if key:
        if category_url_validator(incomming_url=key,product_Type_name=False):
            products = categories(URL=key)
            for product in products:
                all_products.extend(fetch_single_product(product_type=product, id=False))
                return render(request, 'shop.html', {'page_obj':pagenation(request,all_products),
                                                         'section_name':key,'categories':show_filter()['categories']
                                                         ,'brands':show_filter()['brands']})
        else:
            return HttpResponse('Unauthorized')
    else:
        all_products = fetch_single_product(product_type=False, id=False)
        return render(request, 'shop.html',{'page_obj':pagenation(request,all_products),'section_name':key,
                                            'categories': show_filter()['categories'],'brands': show_filter()['brands']})

def single(request,id):
    if fetch_single_product_validator(id=id,product_type=False,brand=False) and fetch_product_subimage_validator(id):
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
    if fetch_single_product_validator(id=id, product_type=False,brand=False):
        return increment_decrement(action=action,id=id,request=request)
    else:
        return HttpResponse('Unauthorized')

def delete(request,id):
    if fetch_single_product_validator(id=id, product_type=False,brand=False):
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

        payment_history=Payment_History.objects.create(user=request.user, amount=sum(li['price_data']['unit_amount']*li['quantity']for li in line_items)//100,
                     currency='inr',status='success',payment_method='card')
        for item in items:
            OrderItem.objects.create(
                payment = payment_history,
                product = item.product,
                quantity = item.quantity,
                price_of_purchase = item.product_total_price        # for ML
            )

        items.delete()
        return redirect(checkout_session.url)
    else:
        return redirect('cancel')

@login_required()
def success(request):
    send_emails_to_users(request.user.email)
    return render(request,'success.html')


@login_required()
def cancel(request):
    return render(request,'cancel.html')

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
    if request.method == 'POST':
        categories = Categories.objects.values_list('product_Type_name', flat=True).distinct()
        brands = Products.objects.values_list('product_brand_name', flat=True).distinct()
        return render(request, 'shop.html', {
            'categories': categories,
            'brands': brands,
            })
    else:
        filter_type = request.GET.get('type')
        filter_value = request.GET.get('value')
        if filter_type == 'category':
            products = Products.objects.filter(product_type__product_Type_name=filter_value)
        elif filter_type == 'brand':
            if fetch_single_product_validator(id=False, product_type=False, brand=filter_value):
                products = Products.objects.filter(product_brand_name=filter_value)
            else:
                return JsonResponse({'success': False, 'results': 'unauthorized'})
        else:
            products = Products.objects.none()

        product_list = [{
            'id': p.id,
            'product_name': p.product_name,
            'product_brand_name': p.product_brand_name,
            'product_image': p.product_image.url,
            'unit_product_price': p.unit_product_price,
        } for p in pagenation(request, products).object_list]

        return JsonResponse({'products': product_list,'section_name':filter_value})


@role_required()
def admin_dash(request):
    top_products_df=get_top_products()
    return render(request,'admin_dash.html',{'total_categories':len(categories(URL=False)),
                                             'total_products':len(fetch_single_product(id=False,product_type=False)),
                                             'total_orders':history_save(user=False,amount=False,currency=False,status=False
                                                                         ,payment_method=False,
                                                                         order_length=True,total_amount=False),
                                             'total_payments':history_save(user=False,amount=False,currency=False,status=False
                                                                         ,payment_method=False,
                                                                         order_length=False,total_amount=True),
                                             'top_products':top_products_df.to_dict('records')})
@role_required()
def addcategory(request):
    if request.method == 'POST':
        category_image = request.FILES.get('category_image')
        product_Type_name = request.POST.get('category_name')
        image_error = image_validator(category_image)
        product_Type_name_error = category_url_validator(incomming_url=product_Type_name,product_Type_name=False)
        errors = {}
        if image_error:
            errors['image'] = image_error
        if product_Type_name_error:
            errors['name']='This category already exists'
        if errors:
            return render(request,'add_category.html',{'errors':errors})
        else:
            category = Categories(product_Type_name=product_Type_name.capitalize(),URL= product_Type_name.lower(),
                                  category_image=category_image)
            category.save()
            return render(request, 'add_category.html', {'success': 'Category successfully added'})
    else:
        return render(request, 'add_category.html')

@role_required()
def addproduct(request,id=None):
    if id:           # for editing products
        if request.method == 'POST':
            if fetch_single_product_validator(id=id, product_type=False, brand=False):
                product = fetch_single_product(id=id, product_type=False)
                product.product_name = request.POST.get('product_name')             # saving edited products
                product.product_color = request.POST.get('product_color')
                product.product_description = request.POST.get('product_description')
                product.product_brand_name = request.POST.get('product_brand_name')
                pro_sub_images = request.FILES.getlist('sub_images')
                product.unit_product_price = request.POST.get('unit_product_price')
                product.is_featured_product = request.POST.get('is_featured')
                product.product_image = request.FILES.get('product_image')
                sub_images=fetch_product_subimage(id)
                sub_images.delete()
                product.save()
                for sub in pro_sub_images:
                    product_sub_image = ProductsSubimage(product=product, product_subimage=sub)
                    product_sub_image.save()
                return render(request, 'add_product.html', {'success': 'Product successfully edited'})
            else:
                return HttpResponse('unauthorized')
        else:
            if fetch_single_product_validator(id=id,product_type=False,brand=False):
                category = categories(URL=False)                                          # rendering edit product
                return render(request,'add_product.html',{'product':fetch_single_product(id=id,product_type=False),
                                                      'categories':category,'sub_images':fetch_product_subimage(id)})
            else:
                return HttpResponse('unauthorized')
    if request.method == 'POST':
        pro_type = request.POST.get('product_type')
        pro_color = request.POST.get('product_color')
        pro_name = request.POST.get('product_name')
        pro_desc = request.POST.get('product_description')        # adding a product
        pro_brand = request.POST.get('product_brand_name')
        pro_unit_price = request.POST.get('unit_product_price')
        pro_main_image = request.FILES.get('product_image')
        pro_is_featured = request.POST.get('is_featured')
        pro_sub_images = request.FILES.getlist('sub_images')
        get_category_name = Categories.objects.get(id=pro_type)
        if category_url_validator(incomming_url=False,product_Type_name=get_category_name):
            products = Products(product_type=get_category_name,
                            product_color=pro_color, product_name=pro_name.capitalize(),
                            product_description=pro_desc,
                            product_brand_name=pro_brand.capitalize(),
                            unit_product_price=pro_unit_price,
                            product_image=pro_main_image, is_featured_product=pro_is_featured)
            products.save()
            for sub in pro_sub_images:
                product_sub_image = ProductsSubimage(product=products, product_subimage=sub)
                product_sub_image.save()
            return render(request, 'add_product.html', {'success': 'Product successfully added'})
        else:
            return render(request, 'add_product.html', {'success': 'Category does not exists'})
    else:
        category=categories(URL=False)
        return render (request,'add_product.html',{'categories':category})   # rendering add product page


@role_required()
def admin_payment_view(request):
    hist = Payment_History.objects.all()
    return render(request,'admin_payment_view.html',{'payments':hist})


@role_required()
def admin_products_view(request):
    return render(request,'admin_products_view.html',{'products':fetch_single_product(product_type=False, id=False)})


@role_required()
def demand_prediction_view(request):
    # Load data from the OrderItem model
    qs = OrderItem.objects.all().values('product__id', 'product__product_name', 'date_of_order', 'quantity')
    df = pd.DataFrame(qs)

    if df.empty:
        print("no data entered")
        return render(request, 'demand_prediction.html',
                      {'predictions': {}, 'error': 'No data available for prediction.'})

    df['date_of_order'] = pd.to_datetime(df['date_of_order'])
    df_grouped = df.groupby(['product__id', 'product__product_name', 'date_of_order'])['quantity'].sum().reset_index()

    predictions = {}

    for (product_id, product_name), group in df_grouped.groupby(['product__id', 'product__product_name']):
        group = group.sort_values('date_of_order')
        group['days_since'] = (group['date_of_order'] - group['date_of_order'].min()).dt.days

        X = group[['days_since']]
        y = group['quantity']

        if len(X) < 2:
            continue  # Skip if not enough data for regression

        model = LinearRegression()
        model.fit(X, y)

        # Predict for next 7 days
        last_day = group['days_since'].max()
        future_days = [last_day + i for i in range(1, 8)]
        future_dates = [group['date_of_order'].max() + timedelta(days=i) for i in range(1, 8)]
        predicted_quantities = model.predict([[day] for day in future_days])
        print("predicted quantities",predicted_quantities)
        predictions[product_name] = list(zip(future_dates, predicted_quantities.round(2)))
    print("data entered",predictions)
    return render(request, 'demand_prediction.html', {'predictions': predictions})