# Generated by Django 4.2.19 on 2025-02-28 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0007_products_product_color'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductTypes',
            new_name='Categories',
        ),
    ]
