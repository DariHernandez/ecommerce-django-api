# Generated by Django 4.0.4 on 2022-06-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_keaganbrand_image_alter_keagannewproduct_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keaganbrand',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
