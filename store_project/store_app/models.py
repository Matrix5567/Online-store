from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True,unique=True)
    image = models.ImageField(upload_to='images/',null=True)
    is_admin = models.BooleanField(default=False,null=True)  # role admin = True , normal user =False
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    def __str__(self):
        return self.email

class Categories(models.Model):
    category_image = models.ImageField(upload_to='category_image/',null=True)
    product_Type_name = models.CharField(max_length=255)
    URL = models.CharField(max_length=25,null=True)
    def __str__(self):
        return self.product_Type_name

class Products(models.Model):
    product_type = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='product_types',null=True)
    product_name = models.CharField(max_length=255)
    product_color = models.CharField(max_length=50,null=True)
    product_description = models.CharField(max_length=255)
    product_brand_name = models.CharField(max_length=255,null=True)
    unit_product_price = models.IntegerField(null=True)
    is_featured_product = models.BooleanField(default=False, null=True)
    product_image = models.ImageField(upload_to='product_main_images/')
    product_quantity = models.PositiveIntegerField(null=True,default=1)

    def __str__(self):
        return self.product_name

class ProductsSubimage(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name='subimages')
    product_subimage = models.ImageField(upload_to='product_sub_images/')

class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product')
    quantity = models.PositiveIntegerField(default=1)
    product_total_price = models.IntegerField(null=True)
    cart_total_price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user}"


class Payment_History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    currency = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)

class OrderItem(models.Model):
    payment = models.ForeignKey(Payment_History, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_of_purchase = models.IntegerField(null =True)