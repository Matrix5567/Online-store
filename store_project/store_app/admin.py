from django.contrib import admin
from .models import CustomUser , Products , ProductsSubimage , Categories, Cart, Payment_History
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Products)
admin.site.register(ProductsSubimage)
admin.site.register(Categories)
admin.site.register(Cart)
admin.site.register(Payment_History)