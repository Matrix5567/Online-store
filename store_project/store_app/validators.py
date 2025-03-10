import re
import imghdr

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
    else:
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-,]+$",email):
            return "Invalid Email"
        else:
            return None

def phone_validator(phone):
    if not phone:
        return "Phone number cannot be empty"
    else:
        if not re.match(r"^\d{10,12}$",phone):
            return "Phone number must contain digits and 10-12 characters long"
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