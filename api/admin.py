from django.contrib import admin
from api.models import *
from django.contrib.auth.models import User

# Register your models here

admin.site.register(Proveedor)
admin.site.register(Item)
admin.site.register(Kit)
admin.site.register(KitDetalle)
admin.site.register(Prestador)
admin.site.register(Prestamo)
admin.site.register(IngresoEgreso)
