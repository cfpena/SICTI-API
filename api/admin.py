from django.contrib import admin
from api.models import *
from django.contrib.auth.models import User

# Register your models here

admin.site.register(Proveedor)
admin.site.register(Dispositivo)
admin.site.register(Elemento)
admin.site.register(Kit)
admin.site.register(KitContieneElemento)
admin.site.register(Prestador)
admin.site.register(Prestamo)
admin.site.register(IngresoEgresoElemento)
admin.site.register(IngresoEgresoDispositivo)
