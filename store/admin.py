from django.contrib import admin, auth
from . import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class MyAdminSite(admin.AdminSite):
    site_header = 'Dari Dev Store Dashboard'
    site_title = 'Store Dashboard'
    

admin_site = MyAdminSite()

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

@admin.register(models.KeaganNewProductCategory)
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

# Unregister defauls admin and groups
admin.site.unregister(User)
admin.site.unregister(Group)

# Setup agian admin and groups using django class
@admin.register(User)
class NewUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(Group)
class NewGroupAdmin(GroupAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


admin_site.register(User, NewUserAdmin)
admin_site.register(Group, NewGroupAdmin)
admin_site.register(models.KeaganBrand, BrandAdmin)
admin_site.register(models.KeaganProduct, ProductAdmin)
admin_site.register(models.KeaganBest, BestAdmin)
admin_site.register(models.KeaganNewProductCategory, NewCategoryProductAdmin)
admin_site.register(models.KeaganNewProduct, NewProductAdmin)