# Generated by Django 4.0.4 on 2022-06-09 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_keagannewproduct_image_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KeaganNewProductsCategories',
            new_name='KeaganNewProductCategory',
        ),
    ]
