

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

