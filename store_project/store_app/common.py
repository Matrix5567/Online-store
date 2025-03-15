from django.forms.models import model_to_dict
from datetime import datetime
from . models import Products, ProductsSubimage, Categories, CustomUser




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