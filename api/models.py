#-*- encoding=UTF-8 -*-

from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_unicode

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
    Direccion = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return smart_unicode(self.Email)


@python_2_unicode_compatible
class Proveedor(Persona):
    RUC = models.CharField(max_length=10, validators=[solo_numeros],null=True,blank=True,unique=True)
    Razon_Social = models.CharField(max_length=30, validators=[solo_letras])

    def __str__(self):
        return smart_unicode(self.Razon_Social)


@python_2_unicode_compatible
class Prestador(Persona):
    generoChoices = (
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )
    tipoChoices = (
        ('T', 'Trabajador'),
        ('E' , 'Estudiante'),
        ('X', 'Externo')
    )
    CI = models.CharField(max_length=10, validators=[solo_numeros],unique=True)
    Matricula = models.CharField(max_length=9,unique=True,blank=True)
    Nombre = models.CharField(max_length=30, validators=[solo_letras])
    Apellido = models.CharField(max_length=30, validators=[solo_letras])
    Genero = models.CharField(
        max_length=2,
        choices=generoChoices,
        default='M', blank=True, null=True
    )
    Tipo = models.CharField(
        max_length=2,
        choices=tipoChoices,
        default='E', blank=True, null=True
    )

    def __str__(self):
        return smart_unicode(self.Nombre + '' + self.Apellido)


@python_2_unicode_compatible
class Elemento(models.Model):
    Codigo = models.CharField(max_length=10, unique=True, validators=[alfanumericos])
    Nombre = models.CharField(max_length=20, validators=[alfanumericos])
    Descripcion = models.CharField(max_length=40, blank=True)
    Esta_Prestado = models.BooleanField(default=False)
    Stock = models.IntegerField(default=0)
    Stock_Disponible = models.IntegerField(default=0)
    Image = models.ImageField(upload_to='items', blank=True)
    Proveedor = models.ForeignKey(Proveedor, null=True,blank=True,default=None)

    def __str__(self):
        return smart_unicode(self.Nombre)

@python_2_unicode_compatible
class Dispositivo(Elemento):
    CodigoEspol = models.CharField(max_length=10, unique=True, validators=[alfanumericos], null=True, blank=True,
                                   default=None)
    CodigoSenecyt = models.CharField(max_length=10, unique=True, validators=[alfanumericos], null=True, blank=True,
                                     default=None)
    Marca = models.CharField(max_length=30, blank=True, validators=[alfanumericos])
    Modelo = models.CharField(max_length=30, blank=True, validators=[alfanumericos])
    Serie = models.CharField(max_length=30, blank=True, validators=[alfanumericos])

    def __str__(self):
        return smart_unicode(self.Nombre)



@python_2_unicode_compatible
class Kit(Dispositivo):
    Elementos = models.ManyToManyField(Elemento,related_name='elementos', through='KitContieneElemento')
    Dispositivos = models.ManyToManyField(Dispositivo,related_name='dispositivos')

    def __str__(self):
        return smart_unicode(self.Nombre)

class KitContieneElemento(models.Model):
    Cantidad= models.IntegerField(default=0)
    Kit = models.ForeignKey(Kit,related_name='kit')
    Elemento= models.ForeignKey(Elemento,related_name='elemento')




class Movimiento(models.Model):
    Fecha = models.DateField(auto_now=True)
    Cantidad = models.IntegerField()
    Detalle = models.CharField(max_length=200)
    Elementos = models.ManyToManyField(Elemento)

class IngresoEgreso(Movimiento):
    tipoChoices = (
        ('I', 'Ingreso'),
        ('S', 'Salida')
    )
    Tipo = models.CharField(
        max_length=1,
        choices=tipoChoices
    )

class Prestamo(Movimiento):
    Fecha_vencimiento = models.DateField()
    Fecha_devolucion = models.DateField()
    Prestador = models.ForeignKey(Prestador)

    def __str__(self):
        return smart_unicode(self.Persona)

