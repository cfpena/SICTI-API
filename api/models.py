#-*- encoding=UTF-8 -*-

from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_unicode


#validaciones
solo_letras = RegexValidator(r'^[ña-zA-Z]*$','Solo letras')
solo_numeros = RegexValidator(r'^\d{1,10}$','Solo numeros')
alfanumericos = RegexValidator(r'^[0-9a-zA-Z]*$','Solo alfanumericos')

# Create your models here.

'''
@python_2_unicode_compatible
class Tipo_Usuario(models.Model):
    Tipo_usuario = models.CharField(max_length=15)
    Descripcion = models.CharField(max_length=30, blank=True)
    Usuario = models.ManyToManyField(User,symmetrical=False,related_name='usuario')
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Tipo_usuario)
'''

@python_2_unicode_compatible
class Persona(models.Model):
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
    Usuario = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return smart_unicode(self.Nombre + ' ' + self.Apellido)

@python_2_unicode_compatible
class Item(models.Model):
    Codigo = models.CharField(max_length=10,unique=True, validators=[alfanumericos])
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])
    Marca = models.CharField(max_length=20, blank=True, validators=[alfanumericos])
    Modelo = models.CharField(max_length=20, blank=True, validators=[alfanumericos])
    Is_dispositivo = models.BooleanField(default=False)
    Is_kit = models.BooleanField(default=False)
    Stock = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    Images = models.ImageField(upload_to='items', blank=True)
    Items = models.ManyToManyField('self',symmetrical=False,related_name='contenido')

    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Nombre)


class Item_Detalle_Kit(models.Model):
    Cantidad = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    fk_item = models.ForeignKey(Item,null=True)

@python_2_unicode_compatible
class Tipo_Identificacion(models.Model):
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Nombre)

class Item_Identicacion(models.Model):
    Valor = models.CharField(max_length=20, validators=[alfanumericos])
    fk_item = models.ForeignKey(Item, null=True)
    fk_tipoIdentifacion = models.ForeignKey(Tipo_Identificacion, null=True)
@python_2_unicode_compatible
class Tipo_Movimiento(models.Model):
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Nombre)

class Movimiento(models.Model):
    Fecha = models.DateField(auto_now=True)
    fk_tipoMovimiento = models.ForeignKey(Tipo_Movimiento, null=True)
@python_2_unicode_compatible
class Movimiento_Detalle(models.Model):
    Cantidad = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    Detalle = models.CharField(max_length=30, validators=[alfanumericos])
    fk_item = models.ForeignKey(Item, null=True)
    fk_movimiento = models.ForeignKey(Movimiento,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Detalle)

class Movimiento_Detalle_ID(models.Model):
    fk_item = models.ForeignKey(Item,null=True)
    fk_movimientoDetalle = models.ForeignKey(Movimiento_Detalle,null=True)
    fk_tipoIdenticacion = models.ForeignKey(Tipo_Identificacion, null=True)

@python_2_unicode_compatible
class Prestario(models.Model):
    Funcion = models.CharField(max_length=20 , validators=[alfanumericos])
    Activo = models.BooleanField(default=False)
    fk_persona = models.ForeignKey(Persona,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Funcion)

#falta validar
class Prestamo(models.Model):
    Fecha_vencimiento = models.DateField()
    Fecha_devolucion = models.DateField()
    fk_movimiento = models.ForeignKey(Movimiento,null=True)
    fk_prestario = models.ForeignKey(Prestario,null=True)
class Proveedor(models.Model):
    activo = models.BooleanField(default=False)
    fk_persona = models.ForeignKey(Persona,null=True)
@python_2_unicode_compatible
class Ingreso(models.Model):
    Acta_entrega = models.CharField(max_length=30)
    fk_movimientos = models.ForeignKey(Movimiento,null=True)
    fk_proveedor = models.ForeignKey(Proveedor,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Acta_entrega)
@python_2_unicode_compatible
class Salida(models.Model):
    Motivo_salida = models.CharField(max_length=30)
    No_Acta_Salida = models.CharField(max_length=30)
    fk_movimientos = models.ForeignKey(Movimiento,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Motivo_salida)
'''
@python_2_unicode_compatible
class Opciones_Sistema(models.Model):
    Descripcion = models.CharField(max_length=30)
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Descripcion)
class Restriccion(models.Model):
    Puede_leer = models.BooleanField(default=False)
    Puede_ingresar = models.BooleanField(default=False)
    Puede_modificar = models.BooleanField(default=False)
    Puede_eliminar = models.BooleanField(default=False)
    Puede_imprimir = models.BooleanField(default=False)
    fk_opcionesSistema = models.ForeignKey(Opciones_Sistema,null=True)
    fk_tipo_usuario = models.ForeignKey(Tipo_Usuario, null=True)
'''
