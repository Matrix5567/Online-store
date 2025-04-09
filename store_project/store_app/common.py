from django.forms.models import model_to_dict
from datetime import datetime

from django.http import JsonResponse

from . models import Products, ProductsSubimage, Categories, CustomUser, Cart




def fetch_product_subimage(id):    # fetching subimages of products
    images = ProductsSubimage.objects.filter(product=id)
    return images

def fetch_single_product(id,product_type):
    if product_type:
        products = Products.objects.filter(product_type=product_type)  # fetch by product_type
    elif id:
        products = Products.objects.get(id=id)  # get single product
    else:
        products = Products.objects.all()    # fetching all products
    return products

def categories(URL):
    if URL:
        prod_cat = Categories.objects.filter(URL=URL)
    else:
        prod_cat = Categories.objects.all()
    return prod_cat

def register(name,phone,email,image,password):
    CustomUser.objects.create_user(full_name=name,phone_number=phone,email=email,image=image,
                                   password=password,is_admin=False,username=email)
    return True

def get_user(email):
    return CustomUser.objects.get(email=email)


def json_serializable(user,request):
    user_data = model_to_dict(user, exclude=['password'])
    for field in ['last_login', 'date_joined']:
        if field in user_data and isinstance(user_data[field], datetime):
            user_data[field] = user_data[field].isoformat()
        # Convert ImageField to full URL
        if 'image' in user_data and user.image:
            user_data['image'] = request.build_absolute_uri(user.image.url)
    return user_data

def get_cart(submitt,user,request):
    if submitt:
        if user:
            print("save to database",submitt)
        else:
            cart = request.session.get('cart',{})
            product_id = str(submitt['product_id'])
            cart[product_id] = {
                'prod_total_price': int(submitt['product_total_price']), 'prod_size': submitt['product-size']
                , 'product_quantity':int(submitt['product_quantity']), 'product_name': submitt['product_name'],
                'product_brand_name': submitt['product_brand_name'],
                'product_description': submitt['product_product_description'],
                'product_color': submitt['product_product_color'], 'product_image': submitt['product_image'],
                'product_unit_price': int(submitt['product_unit_price']), 'product_id': submitt['product_id']

            }
            request.session['cart']=cart
            request.session.modified=True
    else:
        if user:
            return Cart.objects.all()
        else:
            cart = request.session.get('cart',{})
            return cart

def cart_count(request):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        return len(cart)
    else:
        print("count from database")


def cart_total_price(cart,request):
    total_price = 0
    for item in cart.values():
        total_price += int(item['prod_total_price'])
    return total_price

def increment_decrement(action,id,request):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        if action == 'inc':
            cart[str(id)]['product_quantity']+=1
            cart[str(id)]['prod_total_price'] = cart[str(id)]['product_quantity'] * cart[str(id)]['product_unit_price']
            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({'success':True,'quantity':  cart[str(id)]['product_quantity'],
                             'sub_total':cart[str(id)]['prod_total_price'],'total':cart_total_price(cart,request),
                                 'count':cart_count(request)})
        elif action == 'dec':
            if cart[str(id)]['product_quantity'] >1:
                cart[str(id)]['product_quantity'] -= 1
                cart[str(id)]['prod_total_price'] = cart[str(id)]['product_quantity'] * cart[str(id)]['product_unit_price']
                request.session['cart'] = cart
                request.session.modified = True
                return JsonResponse({'success':True,'quantity': cart[str(id)]['product_quantity'],
                                 'sub_total':cart[str(id)]['prod_total_price'],'total':cart_total_price(cart,request),
                                     'count':cart_count(request)})
            else:
                return JsonResponse({'success':True,'quantity': cart[str(id)]['product_quantity'],
                                 'sub_total':cart[str(id)]['prod_total_price'],'total':cart_total_price(cart,request),
                                     'count':cart_count(request)})
        else:
            print("unknown error occured at quantity")
    else:
        print("database increment/decrement operations")


def delete_product(request,id):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        if str(id) in cart:
            del cart[str(id)]
            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({'success':True,'id':id,'total':cart_total_price(cart,request),'count':cart_count(request)})
        else:
            return "no id found"
    else:
        print('database delete')