from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True,unique=True)
    image = models.ImageField(upload_to='images/',null=True)
    is_admin = models.BooleanField(default=False,null=True)  # role admin = True , normal user =False
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    def __str__(self):
        return self.email

class ProductTypes(models.Model):
    product_Type_name = models.CharField(max_length=255)
    product_Sub_type_name = models.CharField(max_length=255)
    is_featured_product = models.BooleanField(default=False,null=True)

class Products(models.Model):
    product_type = models.ForeignKey(ProductTypes,on_delete=models.CASCADE,related_name='product_types',null=True)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_brand_name = models.CharField(max_length=255,null=True)
    product_price = models.IntegerField(null=True)
    product_image = models.ImageField(upload_to='product_main_images/')

class ProductsSubimage(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name='subimages')
    product_subimage = models.ImageField(upload_to='product_sub_images/')