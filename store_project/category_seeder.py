import os
import django

os.environ['DJANGO_SETTINGS_MODULE']='store_project.settings'
django.setup()
from store_app.models import Categories


category = Categories(product_Type_name='Toys',product_Sub_type_name='Toys',is_featured_product=False)
category.save()