from django.contrib import admin, auth
from . import models

class MyAdminSite(admin.AdminSite):
    site_header = 'Dari Dev Store Dashboard'
    site_title = 'Store Dashboard'
    

admin_site = MyAdminSite()

# regular import database table
# admin.site.register(keagan_brand)

# Import with extra actions
@admin.register(models.KeaganBrand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    ordering = ['name']

@admin.register(models.KeaganProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'brand', 'name', 'price')
    list_filter = ('brand',)
    # radio_fields = {"brand": admin.VERTICAL}
    ordering = ['code']
    search_fields = ['name']
    search_help_text = "Serach product by name"

@admin.register (models.KeaganBest)
class BestAdmin (admin.ModelAdmin):
    product = ['code']

@admin.register(models.KeaganNewProductsCategories)
class NewCategoryProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    ordering = ['name']

@admin.register(models.KeaganNewProduct)
class NewProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price')
    list_filter = ('category',)
    # radio_fields = {"category": admin.VERTICAL}
    ordering = ['id']
    search_fields = ['name']
    search_help_text = "Serach new product by name"


admin_site.register(auth.models.User)
admin_site.register(auth.models.Group)
admin_site.register(models.KeaganBrand, BrandAdmin)
admin_site.register(models.KeaganProduct, ProductAdmin)
admin_site.register(models.KeaganBest, BestAdmin)
admin_site.register(models.KeaganNewProductsCategories, NewCategoryProductAdmin)
admin_site.register(models.KeaganNewProduct, NewProductAdmin)