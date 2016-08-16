from django.contrib import admin
from api.models import *
from django.contrib.auth.models import User

# Register your models here

admin.site.register(Persona)
admin.site.register(Item)
admin.site.register(Movimiento)
admin.site.register(Prestamo)
admin.site.register(Item_Relationship)
