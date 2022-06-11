from store.admin import admin_site
from django.urls import path, include

urlpatterns = [
    path('storeapi/', include('store.urls')),
    path('contactform/', include('contactforms.urls')),
    path('', admin_site.urls),
]
