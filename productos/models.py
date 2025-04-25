from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    codigo_balanza = models.CharField(max_length=50)
    codigo_sap = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"
    
    