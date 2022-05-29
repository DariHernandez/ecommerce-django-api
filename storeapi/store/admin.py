from django.contrib import admin, auth
from .models import keagan_brand, keagan_product

class MyAdminSite(admin.AdminSite):
    site_header = 'Dari Dev Store Dashboard'
    site_title = 'Store Dashboard'
    

admin_site = MyAdminSite()

# regular import database table
# admin.site.register(keagan_brand)

# Import with extra actions
@admin.register(keagan_brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    ordering = ['name']

@admin.register(keagan_product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'brand', 'name', 'price')
    list_filter = ('brand',)
    radio_fields = {"brand": admin.VERTICAL}
    ordering = ['code']
    search_fields = ['name']
    search_help_text = "Serach keagan_product by name"

admin_site.register(keagan_brand, BrandAdmin)
admin_site.register(keagan_product, ProductAdmin)
admin_site.register(auth.models.User)
admin_site.register(auth.models.Group)
