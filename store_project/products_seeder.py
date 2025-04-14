import json
import os
import django

os.environ['DJANGO_SETTINGS_MODULE']='store_project.settings'
django.setup()
from store_app.models import Products, ProductsSubimage, Categories

with open('products.json') as f:
    data = json.load(f)
for datas in data:
    products = Products(product_type=Categories.objects.get(product_Type_name='Electronics'),product_color=datas['product_color'], product_name=datas['product_name'],product_description=datas['product_description'],
                        product_brand_name=datas['product_brand_name'],unit_product_price=datas['unit_product_price'],
                        product_image=datas['product_image'],is_featured_product=datas['is_featured_product'])
    products.save()
    for sub in datas['subimage']:
        product_sub_image = ProductsSubimage(product=products,product_subimage=sub['product_subimage'])
        product_sub_image.save()
print("data seeded successfully")
