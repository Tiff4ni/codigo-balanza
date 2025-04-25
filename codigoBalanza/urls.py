from django.shortcuts import redirect
from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', lambda request: redirect('/productos/buscar/')),  
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
]
