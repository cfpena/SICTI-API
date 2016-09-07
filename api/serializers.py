from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from rest_framework.decorators import api_view

#Tipo de Usuario
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name','url')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    Email = serializers.CharField(source='username')
    Nombre = serializers.CharField(source='first_name')
    Apellido = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('url','Email','Nombre','Apellido','groups')

class ChangePasswordSerializer(serializers.Serializer):
    user = serializers.CharField(help_text = 'User',)
    password1 = serializers.CharField(help_text = 'New Password',)
    password2 = serializers.CharField(help_text = 'New Password (confirmation)',)

    def create(self, attrs, instance=None):
        return User(**attrs)

    def update(self, user, instance=None):
        password1=instance.get('password1')
        password2=instance.get('password2')
        usuario = User.objects.get(username=instance.get('user'))
        if(usuario is not None):
            if(user == usuario or user.is_staff):
                if password1 == password2:
                    """ change password """
                    usuario.set_password(instance.get('password2'))
                    usuario.save()
                    return usuario
                else:
                    raise serializers.ValidationError('Password confirmation mismatch')
        return instance

class ReporteSerializer(serializers.Serializer):
    fecha_inicial = serializers.DateField()
    fecha_final = serializers.DateField


class PrestadorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Prestador
        fields = '__all__'

'''
class ElementoSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)

    class Meta:
        model = Elemento
        fields = '__all__'



class DispositivoSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Dispositivo
        fields = '__all__'
        depth = 1
'''

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        depth = 1

class IdentificacionesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Identificaciones
        fields = '__all__'

class ItemReporteSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = ('Codigo','Nombre','Stock','Stock_Disponible')

class ElementoSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        depth = 1

class DispositivoSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        depth = 1
class KitDetalleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = KitDetalle
        fields = '__all__'

class KitSerializer(serializers.HyperlinkedModelSerializer):
    KitDetalle = KitDetalleSerializer(many=True)
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Kit
        fields = '__all__'

class KitUltimoSerializer(serializers.HyperlinkedModelSerializer):
    Stock_Disponible = serializers.CharField(read_only=True)
    Stock = serializers.CharField(read_only=True)
    class Meta:
        model = Kit
        fields = '__all__'





class PrestamoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Prestamo
        fields = '__all__'

class IngresoEgresoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = IngresoEgreso
        fields = '__all__'


class ActaSerializer(serializers.HyperlinkedModelSerializer):
    Prestamo = PrestamoSerializer
    class Meta:
        model = Acta
        fields = '__all__'

class DevolucionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Devolucion
        fields = '__all__'

class FacturaIngresoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FacturaIngreso
        fields = '__all__'
'''
class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='usuarios-detail',
    )
    Usuario = UserSerializer()
    class Meta:
        model = Persona
        fields = '__all__'
    def create(self, validated_data):
        user = User.objects.create(username=validated_data.get('Usuario')['username'])
        groupNames=validated_data.get('Usuario')['groups']
        if(len(groupNames)>0):
            group = Group.objects.get(name=groupNames[0])
            if(group!=None):
                user.groups.add(group)
        return  Persona.objects.create(CI=validated_data.get('CI'),
                                         Nombre=validated_data.get('Nombre'),
                                         Apellido=validated_data.get('Apellido'),
                                         Email=validated_data.get('Email'),
                                         Telefono=validated_data.get('Telefono'),
                                         Genero=validated_data.get('Genero'),
                                         Usuario=user)

class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item

        fields = ("id","Codigo","CodigoEspol","CodigoSenecyt","Nombre","Marca","Modelo","Descripcion","Is_dispositivo","Stock","Images")


class KitSerializer(serializers.HyperlinkedModelSerializer):
    #Items=ItemSerializer(many=True)
    class Meta:
        model = Item

        fields = ("url","Codigo","CodigoEspol","CodigoSenecyt","Nombre","Marca","Modelo","Descripcion","Stock","Items","Is_kit")


class PrestamoSerializer(serializers.HyperlinkedModelSerializer):
    #Persona=PersonaSerializer()
    #Items=ItemSerializer(many=True)
    class Meta:
        model = Prestamo
        fields =  '__all__'
class MovimientoSerializer(serializers.HyperlinkedModelSerializer):
    Prestamo=PrestamoSerializer()
    #Item=ItemSerializer()
    class Meta:
        model = Movimiento
        fields = '__all__'
'''