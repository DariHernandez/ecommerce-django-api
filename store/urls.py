from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path ('', views.index, name="index"),
    path ('keagan/', views.keagan_home, name="keagan_home"),
    path ('keagan/category-products/<int:brand_name>/', views.keagan_category_products, name="keagan_category_products"),
    path ('keagan/product/<int:product_id>/', views.keagan_product, name="keagan_product"),
    path ('keagan/product-new/<int:product_id>/', views.keagan_product_new, name="keagan_product_new")
]