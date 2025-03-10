# Generated by Django 4.2.19 on 2025-03-09 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0013_remove_customuser_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='is_featured_product',
        ),
        migrations.AddField(
            model_name='products',
            name='is_featured_product',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
