from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('login/', views.login_view, name='login'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
     path('editar/<str:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<str:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]
