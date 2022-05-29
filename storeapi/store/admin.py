from django.contrib import admin, auth
from . import models

class MyAdminSite(admin.AdminSite):
    site_header = 'Dari Dev Store Dashboard'
    site_title = 'Store Dashboard'
    

admin_site = MyAdminSite()

# regular import database table
# admin.site.register(keagan_brand)

# Import with extra actions
@admin.register(models.keagan_brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    ordering = ['name']

@admin.register(models.keagan_product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'brand', 'name', 'price')
    list_filter = ('brand',)
    # radio_fields = {"brand": admin.VERTICAL}
    ordering = ['code']
    search_fields = ['name']
    search_help_text = "Serach product by name"

@admin.register (models.keagan_best)
class BestAdmin (admin.ModelAdmin):
    product = ['code']

@admin.register(models.keagan_new_products_categories)
class NewCategoryProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    ordering = ['name']

@admin.register(models.keagan_new_product)
class NewProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price')
    list_filter = ('category',)
    # radio_fields = {"category": admin.VERTICAL}
    ordering = ['id']
    search_fields = ['name']
    search_help_text = "Serach new product by name"


admin_site.register(auth.models.User)
admin_site.register(auth.models.Group)
admin_site.register(models.keagan_brand, BrandAdmin)
admin_site.register(models.keagan_product, ProductAdmin)
admin_site.register(models.keagan_best, BestAdmin)
admin_site.register(models.keagan_new_products_categories, NewCategoryProductAdmin)
admin_site.register(models.keagan_new_product, NewProductAdmin)