from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

app_name = "contactforms"
urlpatterns = [
    path ('', views.index, name="index"),
]