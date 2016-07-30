from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from django.db import models


#validaciones
solo_letras = RegexValidator(r'^[a-zA-Z]*$','Solo letras')
solo_numeros = RegexValidator(r'^\d{1,10}$','Solo numeros')
alfanumericos = RegexValidator(r'^[0-9a-zA-Z]*$','Solo alfanumericos')

# Create your models here.
class Personas(models.Model):
    generoChoices=(
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )
    CI = models.CharField(max_length=10, unique=True, validators=[solo_numeros])
    Nombre = models.CharField(max_length=30, validators=[solo_letras])
    Apellido = models.CharField(max_length=30, validators=[solo_letras])
    Email = models.EmailField(max_length=60, unique=True)
    Telefono = models.CharField(max_length=10,blank=True)
    Genero = models.CharField(
        max_length=2,
        choices= generoChoices ,
        default='M',
    )
    usuario = models.ForeignKey(User,null=True)

class Items(models.Model):
    Codigo = models.CharField(max_length=10,unique=True, validators=[alfanumericos])
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])
    Marca = models.CharField(max_length=20, blank=True, validators=[alfanumericos])
    Modelo = models.CharField(max_length=20, blank=True, validators=[alfanumericos])
    Is_dispositivo = models.BooleanField(default=False)
    Is_kit = models.BooleanField(default=False)
    Stock = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    Images = models.ImageField(upload_to='fotos', blank=True)

class Items_Detalle_Kits(models.Model):
    Cantidad = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    fk_item = models.ForeignKey(Items,null=True)

class Tipo_Identificacion(models.Model):
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])

class Item_Identicacion(models.Model):
    Valor = models.CharField(max_length=20, validators=[alfanumericos])
    fk_item = models.ForeignKey(Items, null=True)
    fk_tipoIdentifacion = models.ForeignKey(Tipo_Identificacion, null=True)

class Tipo_Movimiento(models.Model):
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])

class Movimientos(models.Model):
    Fecha = models.DateField(auto_now=True)
    fk_tipoMovimiento = models.ForeignKey(Tipo_Movimiento, null=True)

class Movimiento_Detalle(models.Model):
    Cantidad = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    Detalle = models.CharField(max_length=30, validators=[alfanumericos])
    fk_item = models.ForeignKey(Items, null=True)
    fk_movimiento = models.ForeignKey(Movimientos,null=True)

class Movimiento_Detalle_ID(models.Model):
    fk_item = models.ForeignKey(Items,null=True)
    fk_movimientoDetalle = models.ForeignKey(Movimiento_Detalle,null=True)
    fk_tipoIdenticacion = models.ForeignKey(Tipo_Identificacion, null=True)

class Prestarios(models.Model):
    Funcion = models.CharField(max_length=20 , validators=[alfanumericos])
    Activo = models.BooleanField(default=False)
    fk_persona = models.ForeignKey(Personas,null=True)

#falta validar
class Prestamos(models.Model):
    Fecha_vencimiento = models.DateField()
    Fecha_devolucion = models.DateField()
    fk_movimiento = models.ForeignKey(Movimientos,null=True)
    fk_prestario = models.ForeignKey(Prestarios,null=True)

class Proveedores(models.Model):
    activo = models.BooleanField(default=False)
    fk_persona = models.ForeignKey(Personas,null=True)

class Ingresos(models.Model):
    Acta_entrega = models.CharField(max_length=30)
    fk_movimientos = models.ForeignKey(Movimientos,null=True)
    fk_proveedor = models.ForeignKey(Proveedores,null=True)

class Salidas(models.Model):
    Motivo_salida = models.CharField(max_length=30)
    No_Acta_Salida = models.CharField(max_length=30)
    fk_movimientos = models.ForeignKey(Movimientos,null=True)

class Opciones_Sistema(models.Model):
    Descripcion = models.CharField(max_length=30)

class Restricciones(models.Model):
    Puede_leer = models.BooleanField(default=False)
    Puede_ingresar = models.BooleanField(default=False)
    Puede_modificar = models.BooleanField(default=False)
    Puede_eliminar = models.BooleanField(default=False)
    Puede_imprimir = models.BooleanField(default=False)
    fk_opcionesSistema = models.ForeignKey(Opciones_Sistema,null=True)
    fk_usuario = models.ForeignKey(User,null=True)
