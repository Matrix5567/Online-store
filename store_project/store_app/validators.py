import re
import imghdr
from .models import CustomUser, Categories, Products, ProductsSubimage
from django.contrib.auth.hashers import check_password



def name_validator(name):
    if not name:
        return "Name cannot be empty"
    else:
        if len(name)<=2:
            return "Name must be greater than two"
        else:
            return None


def email_validator(email):
    if not email:
        return "Email cannot be emtpty"
    elif CustomUser.objects.filter(email=email).exists():
        return "This email already exists"
    else:
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-,]+$",email):
            return "Invalid Email"
        else:
            return None

def phone_validator(phone):
    if not phone:
        return "Phone number cannot be empty"
    elif CustomUser.objects.filter(phone_number=phone).exists():
        return "Phone number already exists"
    else:
        if not re.match(r"^\d{10,12}$",phone):
            return "Invalid phone number"
        else:
            return None



def image_validator(image):
    if not image:
        return "Image cannot be empty"
    else:
        if image.size > 5 * 1024 * 1024:  # 5MB limit
            return "Image file size must be less than 5MB."

        ext = image.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg']:
            return "Only JPEG images are allowed."

    # Extra check to ensure it's a real JPEG file
        if imghdr.what(image) not in ['jpeg']:
            return "Invalid image format. Only JPEG is allowed."
        return None

def password_validator(password):
    if not password:
        return "Password cannot be empty"
    else:
        if not re.match(r"^(?=.*[!@#$%^&*()_+{}:;\"'<>,.?/~`-]).{5,}$", password):
            return "Password must be atleast 5 long and must have one special characters"
        else:
            return None

def category_url_validator(incomming_url):
    if Categories.objects.filter(URL=incomming_url).exists():
        return True
    else:
        return False

def fetch_single_product_validator(id,product_type):
    if product_type:
        if Products.objects.filter(product_type=product_type).exists():
            return True
        else:
            return False
    else:
        try:
            Products.objects.get(id=id)
            return True
        except Products.DoesNotExist:
            return False


def fetch_product_subimage_validator(id):
    if ProductsSubimage.objects.filter(product=id).exists():
        return True
    else:
        return False


