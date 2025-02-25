import json
import os
import django

os.environ['DJANGO_SETTINGS_MODULE']='store_project.settings'
django.setup()
from store_app.models import Products, ProductsSubimage, ProductTypes

with open('products.json') as f:
    data = json.load(f)
for datas in data:
    product_type = ProductTypes(product_Type_name=datas['product_Type_name'],product_Sub_type_name=datas['product_Sub_type_name'],
                                is_featured_product=datas['is_featured_product'])
    product_type.save()
    products = Products(product_type=product_type,product_name=datas['product_name'],product_description=datas['product_description'],
                        product_brand_name=datas['product_brand_name'],product_price=datas['product_price'],
                        product_image=datas['product_image'])
    products.save()
    for sub in datas['subimage']:
        product_sub_image = ProductsSubimage(product=products,product_subimage=sub['product_subimage'])
        product_sub_image.save()
print("data seeded successfully")
