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

@python_2_unicode_compatible
class Persona(models.Model):
    generoChoices=(
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )
    CI = models.CharField(max_length=10, validators=[solo_numeros],null=True,blank=True)
    Nombre = models.CharField(max_length=30, validators=[solo_letras])
    Apellido = models.CharField(max_length=30, validators=[solo_letras])
    Email = models.EmailField(max_length=60, unique=True)
    Telefono = models.CharField(max_length=10,blank=True)
    Genero = models.CharField(
        max_length=2,
        choices= generoChoices ,
        default='M',blank=True,null=True
    )
    Usuario = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return smart_unicode(self.Nombre + ' ' + self.Apellido)

@python_2_unicode_compatible
class Item(models.Model):
    Codigo = models.CharField(max_length=10,unique=True, validators=[alfanumericos])
    CodigoEspol = models.CharField(max_length=10,unique=True, validators=[alfanumericos],null=True,blank=True,default=None)
    CodigoSenecyt = models.CharField(max_length=10,unique=True, validators=[alfanumericos],null=True,blank=True,default=None)
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])
    Marca = models.CharField(max_length=20, blank=True, validators=[alfanumericos])
    Modelo = models.CharField(max_length=20, blank=True, validators=[alfanumericos])
    Descripcion = models.CharField(max_length=40, blank=True)
    Is_dispositivo = models.BooleanField(default=False)
    Is_kit = models.BooleanField(default=False)
    Is_Prestado = models.BooleanField(default=False)
    Stock = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
    Images = models.ImageField(upload_to='items', blank=True)
    Items = models.ManyToManyField('self',symmetrical=False,blank=True,default=None,through='Item_Relationship')
    def __str__(self):              # __unicode__ on Python 2
        return smart_unicode(self.Nombre)


class Item_Relationship(models.Model):
    from_item = models.ForeignKey(Item, related_name='from_items',default=None,null=True,blank=True)
    to_item = models.ForeignKey(Item, related_name='to_items',default=None,null=True,blank=True)
    Cantidad = models.IntegerField(default=0, validators=[MaxValueValidator(50),MinValueValidator(1)])
'''
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
'''
#falta validar
class Prestamo(models.Model):
    Fecha_vencimiento = models.DateField()
    Fecha_devolucion = models.DateField()
    Persona = models.ForeignKey(Persona)
class Movimiento(models.Model):
    tipoChoices=(
        ('P', 'Prestamo'),
        ('I', 'Ingreso'),
        ('S', 'Salida')
    )
    Fecha = models.DateField(auto_now=True)
    Tipo = models.CharField(
        max_length=1,
        choices= tipoChoices
    )
    Cantidad = models.IntegerField()
    Detalle = models.CharField(max_length=200)
    Item = models.ForeignKey(Item,null=True,blank=True,default=None)
    Prestamo=models.ForeignKey(Prestamo,null=True,blank=True)
'''
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
class Proveedor(models.Model):
    activo = models.BooleanField(default=False)
    fk_persona = models.ForeignKey(Persona,null=True)

@python_2_unicode_compatible
class Ingreso(models.Model):
    Acta_entrega = models.CharField(max_length=30)
    fk_movimientos = models.ForeignKey(Movimiento,null=True)
    #fk_proveedor = models.ForeignKey(Proveedor,null=True)
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
