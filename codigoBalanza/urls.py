from django.shortcuts import redirect
from django.urls import include
from django.contrib import admin
from django.urls import path

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('menu')  # Redirige al menú si está autenticado
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('', root_redirect, name='root_redirect'),
]
