
from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    marca = forms.CharField(max_length=100, required=False, label='Marca')
    cod_ean = forms.IntegerField(label='Código EAN')
    cod_sap = forms.IntegerField(label='Código SAP')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')