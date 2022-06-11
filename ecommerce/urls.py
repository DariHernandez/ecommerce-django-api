from store.admin import admin_site
from django.urls import path, include

urlpatterns = [
    path('api/', include('store.urls')),
    path('', admin_site.urls),
]
