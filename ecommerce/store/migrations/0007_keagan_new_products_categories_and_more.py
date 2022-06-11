# Generated by Django 4.0.4 on 2022-05-29 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_keagan_best_options_alter_keagan_brand_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='keagan_new_products_categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('details', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'new products category',
                'verbose_name_plural': 'new products categories',
            },
        ),
        migrations.AlterModelOptions(
            name='keagan_best',
            options={'verbose_name': 'best product', 'verbose_name_plural': 'best products'},
        ),
        migrations.AlterModelOptions(
            name='keagan_brand',
            options={'verbose_name': 'brand', 'verbose_name_plural': 'brands'},
        ),
        migrations.AlterModelOptions(
            name='keagan_product',
            options={'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.CreateModel(
            name='keagan_new_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('price', models.FloatField()),
                ('image', models.ImageField(blank=True, default=None, upload_to='imgs/products/full-size')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.keagan_new_products_categories')),
            ],
            options={
                'verbose_name': 'new product',
                'verbose_name_plural': 'new products',
            },
        ),
    ]
