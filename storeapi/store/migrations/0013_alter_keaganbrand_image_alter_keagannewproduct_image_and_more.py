# Generated by Django 4.0.4 on 2022-06-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_rename_keagan_best_keaganbest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keaganbrand',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='D:\\Sync\\Dari Developer\\backend\\ecommerce\\storeapi\\store\\static\\store\\imgs_keagan/brands'),
        ),
        migrations.AlterField(
            model_name='keagannewproduct',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='D:\\Sync\\Dari Developer\\backend\\ecommerce\\storeapi\\store\\static\\store\\imgs_keagan/products/full-size'),
        ),
        migrations.AlterField(
            model_name='keaganproduct',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='D:\\Sync\\Dari Developer\\backend\\ecommerce\\storeapi\\store\\static\\store\\imgs_keagan/products/full-size'),
        ),
    ]
