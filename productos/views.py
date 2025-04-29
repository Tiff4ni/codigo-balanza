from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.conf import settings
import firebase_admin # type: ignore
from firebase_admin import db, credentials # type: ignore
from firebase_admin import auth # type: ignore
import os
from .forms import LoginForm
import requests # type: ignore
from django.contrib import messages
from .decoradores import login_requerido
import json

API_KEY = os.environ.get('FIREBASE_API_KEY')

if not firebase_admin._apps:
    firebase_config_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')
    if not firebase_config_json:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY no está configurada en Render!")
    
    firebase_config = json.loads(firebase_config_json)
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://appproductos-9ead1-default-rtdb.firebaseio.com/'
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            API_KEY = os.environ.get('FIREBASE_API_KEY')
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            data = response.json()

            # ——— DEPURACIÓN ———
            print("Firebase login response:", data)

            if 'idToken' in data:
                request.session['user'] = {
                    'email': data['email'],
                    'idToken': data['idToken'],
                    'uid': data['localId']
                }
                return redirect('buscar_producto')
            else:
                err = data.get('error', {}).get('message', 'Credenciales inválidas')
                messages.error(request, f"Error Firebase: {err}")
    else:
        form = LoginForm()

    return render(request, 'productos/login.html', {'form': form})



@login_requerido
def menu_view(request):
    return render(request, 'productos/menu.html')

@login_requerido
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ref = db.reference('Productos')
            nueva_ref = ref.push() 
            data['id'] = nueva_ref.key 
            nueva_ref.set(data) 
            return redirect('agregar_producto')
    else:
        form = ProductoForm()

    return render(request, 'productos/agregar_producto.html', {'form': form})

@login_requerido
def buscar_producto(request):
    query = request.GET.get('query', '').lower()
    resultados = []

    ref = db.reference('Productos')
    productos = ref.get()

    try:
        ref = db.reference('Productos')
        productos = ref.get() or {}
        ...
    except Exception as e:
        print(f"Error buscando productos: {e}")
        productos = {}

    if productos and query.strip():
        palabras_query = query.split()

        for key, data in productos.items():
            nombre = data.get('nombre', '').lower()
            marca = data.get('marca', '').lower()
            texto_completo = f"{nombre} {marca}"

            # Verificamos si todas las palabras del query están en el texto (nombre+marca)
            if all(palabra in texto_completo for palabra in palabras_query):
                data['id'] = key
                resultados.append(data)

    return render(request, 'productos/buscar_producto.html', {
        'resultados': resultados,
        'query': query
    })



@login_requerido
def editar_producto(request, producto_id):
    ref = db.reference(f'Productos/{producto_id}')
    producto = ref.get()

    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect('buscar_producto')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['id'] = producto_id
            ref.set(data)
            return redirect('buscar_producto')
    else:
        form = ProductoForm(initial=producto)

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto_id': producto_id})

@login_requerido
def eliminar_producto(request, producto_id):
    ref = db.reference(f'Productos/{producto_id}')
    producto = ref.get()

    if producto:
        ref.delete()
        messages.success(request, "Producto eliminado correctamente.")
    else:
        messages.error(request, "Producto no encontrado.")

    return redirect('buscar_producto')

def cerrar_sesion(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('login')
