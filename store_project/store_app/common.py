from django.forms.models import model_to_dict
from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from .validators import category_url_validator
from . models import Products, ProductsSubimage, Categories, CustomUser, Cart


def pagenation(request,products):
    page_number = request.GET.get('page')
    paginator = Paginator(products, 6)
    page_obj = paginator.get_page(page_number)
    return page_obj


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
        if category_url_validator(URL):
            prod_cat = Categories.objects.filter(URL=URL)
        else:
            return False
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


def loged_in_cart_save(user,product,quantity,product_total_price,cart_total):
    Cart(user=user, product=product,
         quantity=quantity, product_total_price=product_total_price,
         cart_total_price=cart_total).save()


def check_item_present(request,id):
    if request.user.is_authenticated:
        if Cart.objects.filter(user=request.user,product=id).exists():
            return True
        else:
            return False
    else:
        cart=request.session.get('cart',{})
        if id in cart:
            return True
        else:
            return False

def get_cart(submitt,user,request):
    if submitt:
        if user:
            product = fetch_single_product(id=submitt['product_id'], product_type=False)
            check_item_exists=check_item_present(request,product)
            if check_item_exists:
                return False
            else:
                loged_in_cart_save(request.user,product,submitt['product_quantity'],submitt['product_total_price'],0)
                return True
        else:
            cart = request.session.get('cart',{})
            product_id = str(submitt['product_id'])
            check_item_exists = check_item_present(request=request,id=product_id)
            if check_item_exists:
                return False
            else:
                cart[product_id] = {
                'prod_total_price': int(submitt['product_total_price'])
                , 'product_quantity':int(submitt['product_quantity']), 'product_name': submitt['product_name'],
                'product_brand_name': submitt['product_brand_name'],
                'product_description': submitt['product_product_description'],
                'product_color': submitt['product_product_color'], 'product_image':submitt['product_image'],
                'product_unit_price': int(submitt['product_unit_price']), 'product_id': submitt['product_id']

                }
                request.session['cart']=cart
                request.session.modified=True
                return True
    else:
        if user:
            cart_items = {}
            for items in Cart.objects.filter(user=request.user):
                cart_items[str(items.product.id)] = {
                    'prod_total_price': items.product_total_price
                    ,'product_quantity': items.quantity, 'product_name':items.product.product_name,
                    'product_brand_name': items.product.product_brand_name,
                    'product_description': items.product.product_description,
                    'product_color': items.product.product_color, 'product_image':items.product.product_image.url,
                    'product_unit_price': items.product.unit_product_price , 'product_id':items.product.id

                }

            return cart_items
        else:
            cart = request.session.get('cart',{})
            return cart

def cart_count(request):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        return len(cart)
    else:
        return len(Cart.objects.filter(user=request.user))

def user_total(cart,request):
    total_price = 0
    if request.user.is_authenticated:
        item = Cart.objects.filter(user=request.user)
        for items in item:
            total_price += items.product_total_price
        return total_price
    else:
        if cart:
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
                             'sub_total':cart[str(id)]['prod_total_price'],'total':user_total(cart,request),
                                 'count':cart_count(request)})
        elif action == 'dec':
            if cart[str(id)]['product_quantity'] >1:
                cart[str(id)]['product_quantity'] -= 1
                cart[str(id)]['prod_total_price'] = cart[str(id)]['product_quantity'] * cart[str(id)]['product_unit_price']
                request.session['cart'] = cart
                request.session.modified = True
                return JsonResponse({'success':True,'quantity': cart[str(id)]['product_quantity'],
                                 'sub_total':cart[str(id)]['prod_total_price'],'total':user_total(cart,request),
                                     'count':cart_count(request)})
            else:
                return JsonResponse({'success':True,'quantity': cart[str(id)]['product_quantity'],
                                 'sub_total':cart[str(id)]['prod_total_price'],'total':user_total(cart,request),
                                     'count':cart_count(request)})
        else:
            print("unknown error occured at quantity")
    else:
        item = Cart.objects.get(product=fetch_single_product(id=id, product_type=False), user=request.user)
        if action == 'inc':
            item.quantity+=1
            item.product_total_price = item.product.unit_product_price * item.quantity
            item.save()
            return JsonResponse({'success': True, 'quantity':item.quantity,
                                 'count': cart_count(request),
                                 'sub_total':item.product_total_price,'total':user_total(cart=False,request=request)})
        elif action == 'dec':
            if item.quantity>1:
                item.quantity -= 1
                item.product_total_price = item.product.unit_product_price * item.quantity
                item.save()
                return JsonResponse({'success': True, 'quantity': item.quantity,
                                     'count': cart_count(request),
                                     'sub_total':item.product_total_price,'total':user_total(cart=False,request=request)})

            else :
                return JsonResponse({'success': True, 'quantity': item.quantity,
                                     'count': cart_count(request),
                                     'sub_total': item.product_total_price,'total':user_total(cart=False,request=request)})
        else:
            print("unknown error occured at quantity")


def delete_product(request,id):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        if str(id) in cart:
            del cart[str(id)]
            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({'success':True,'id':id,'total':user_total(cart,request),'count':cart_count(request)})
        else:
            return ({'success': False})
    else:
        item=Cart.objects.get(product=fetch_single_product(id=id,product_type=False),user=request.user)
        if item:
            item.delete()
        else:
            return ({'success': False})
        return JsonResponse(
            {'success': True, 'id': id,'count': cart_count(request),'total':user_total(cart=False,request=request)})
