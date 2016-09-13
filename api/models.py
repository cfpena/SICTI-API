#-*- encoding=UTF-8 -*-

from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_unicode
from django.core.exceptions import ValidationError
from datetime import datetime
#validaciones
#puede contener espacios
solo_letras = RegexValidator(r'^[ña-zA-Z]*$','Solo letras')
solo_numeros = RegexValidator(r'^\d{1,10}$','Solo numeros')

#puede contener espacios
alfanumericos = RegexValidator(r'^[0-9a-zA-Z]*$','Solo alfanumericos')


@python_2_unicode_compatible
class Persona(models.Model):
    Email = models.EmailField(max_length=60, unique=True)
    Telefono = models.CharField(max_length=10,blank=True)
    Direccion = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return smart_unicode(self.Email)


@python_2_unicode_compatible
class Proveedor(Persona):
    RUC = models.CharField(max_length=10,null=True,blank=True,unique=True)
    Razon_Social = models.CharField(max_length=50)

    def __str__(self):
        return smart_unicode(self.Razon_Social)


@python_2_unicode_compatible
class Prestador(Persona):
    generoChoices = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino')
    )
    tipoChoices = (
        ('Trabajador', 'Trabajador'),
        ('Estudiante' , 'Estudiante'),
        ('Externo', 'Externo')
    )
    CI = models.CharField(max_length=10,unique=True)
    Matricula = models.CharField(max_length=10,blank=True,null=True)
    Nombre = models.CharField(max_length=30)
    Apellido = models.CharField(max_length=30)
    Genero = models.CharField(
        max_length=10,
        choices=generoChoices,
        default='Masculino', blank=True, null=True
    )
    Tipo = models.CharField(
        max_length=11,
        choices=tipoChoices,
        default='Trabajador', blank=True, null=True
    )

    def __str__(self):
        return smart_unicode(self.Nombre + '' + self.Apellido)

'''
@python_2_unicode_compatible
class Elemento(models.Model):
    Codigo = models.CharField(max_length=10, unique=True, )
    Nombre = models.CharField(max_length=50)
    Descripcion = models.CharField(max_length=200, blank=True)
    Stock = models.IntegerField(default=0)
    Stock_Disponible = models.IntegerField(default=0)
    Imagen = models.ImageField(upload_to='items', blank=True,null=True)
    Proveedor = models.ForeignKey(Proveedor, null=True,blank=True,default=None)

    def save(self, *args, **kwargs):
        if not self.pk or kwargs.get('force_insert', False):
            self.Stock_Disponible=self.Stock
        super(Elemento, self).save(*args, **kwargs)

    def __str__(self):
        return smart_unicode(self.Nombre)

@python_2_unicode_compatible
class Dispositivo(Elemento):
    CodigoEspol = models.CharField(max_length=20, null=True, blank=True,
                                   default=None)
    CodigoSenecyt = models.CharField(max_length=20,null=True, blank=True,
                                     default=None)
    Marca = models.CharField(max_length=50, blank=True)
    Modelo = models.CharField(max_length=50, blank=True)
    Serie = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return smart_unicode(self.Nombre)
    '''
class Identificaciones(models.Model):
    Codigo_Espol = models.CharField(max_length=50,blank=True,null=True )
    Codigo_Senecyt = models.CharField(max_length=50,blank=True,null=True )
    Serie = models.CharField(max_length=50, blank=True,null=True )

@python_2_unicode_compatible
class Item(models.Model):

    Marca = models.CharField(max_length=50, blank=True)
    Modelo = models.CharField(max_length=50, blank=True)
    Serie = models.CharField(max_length=50, blank=True)
    Codigo = models.CharField(max_length=10, unique=True, )
    Nombre = models.CharField(max_length=50)
    Descripcion = models.CharField(max_length=200, blank=True)
    Stock = models.IntegerField(default=0)
    Stock_Disponible = models.IntegerField(default=0)
    Imagen = models.ImageField(upload_to='items', blank=True, null=True)
    Proveedor = models.ForeignKey(Prestador, null=True, blank=True, default=None)
    Es_Dispositivo= models.BooleanField()
    Identificaciones= models.ManyToManyField(Identificaciones,blank=True,default=None)

    def save(self, *args, **kwargs):
        if not self.pk or kwargs.get('force_insert', False):
            self.Stock_Disponible = self.Stock
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return smart_unicode(self.Nombre)

    def __str__(self):
        return smart_unicode(self.Nombre)

class KitDetalle(models.Model):
    Cantidad= models.IntegerField(default=0)
    Item= models.ForeignKey(Item,related_name='elemento')

@python_2_unicode_compatible
class Kit(Item):
    KitDetalle = models.ManyToManyField(KitDetalle,null=True,blank=True)


    def __str__(self):
        return smart_unicode(self.Nombre)


class Movimiento(models.Model):
    Fecha = models.DateField(auto_now=True)
    Cantidad = models.IntegerField()
    Detalle = models.CharField(max_length=200,null=True,blank=True)

class IngresoEgreso(Movimiento):
    Item = models.ForeignKey(Item)
    tipoChoices = (
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso')
    )
    Tipo = models.CharField(
        choices=tipoChoices,
        max_length = 7

    )

    def save(self, *args, **kwargs):

        if self.Tipo=='Egreso':
            if self.Item.Stock_Disponible-self.Cantidad<0:
                raise ValidationError('Stock no dispobible', code=0001)
            else:
                self.Item.Stock = self.Item.Stock-self.Cantidad
                self.Item.Stock_Disponible = self.Item.Stock_Disponible-self.Cantidad
                self.Item.save()
                super(IngresoEgreso, self).save(*args, **kwargs)
        elif self.Tipo=='Ingreso':
            self.Item.Stock = self.Item.Stock + self.Cantidad
            self.Item.Stock_Disponible = self.Item.Stock_Disponible + self.Cantidad
            self.Item.save()
            super(IngresoEgreso, self).save(*args, **kwargs)

class Acta(models.Model):
    Fecha= models.DateField(auto_now=True)
    Codigo = models.CharField(max_length=20,null=True,blank=True)
    Prestador = models.ForeignKey(Prestador)
    Fecha_vencimiento = models.DateField(default=datetime.now(),null=True)

class Prestamo(Movimiento):
    Item = models.ForeignKey(Item)
    Acta = models.ForeignKey(Acta, null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.Item.Stock_Disponible-self.Cantidad<0:
            raise ValidationError('Stock no dispobible', code=0001)
        else:
            self.Item.Stock_Disponible = self.Item.Stock_Disponible-self.Cantidad
            self.Item.save()
            super(Prestamo, self).save(*args, **kwargs)




class FacturaIngreso(models.Model):
    Acta = models.CharField(max_length=20,null=True,blank=True)
    Proveedor= models.ForeignKey(Prestador,null=True,blank=True)
    Fecha = models.DateField()
    IngresoEgreso = models.ManyToManyField(IngresoEgreso,null=True,blank=True)
    Descripcion = models.CharField(max_length=200,null=True,blank=True)


class Devolucion(Movimiento):
    Prestamo = models.OneToOneField(Prestamo)

    def __str__(self):
        return smart_unicode(self.Prestamo)

    def save(self, *args, **kwargs):
        if not self.pk or kwargs.get('force_insert', False):
            self.Prestamo.Item.Stock_Disponible = self.Prestamo.Item.Stock_Disponible + self.Cantidad
            self.Prestamo.Item.save()
            super(Devolucion, self).save(*args, **kwargs)

