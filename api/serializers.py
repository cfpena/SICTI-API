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
    #groups=GroupSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ('username','groups','url','id')
class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    Usuario = UserSerializer()
    class Meta:
        model = Persona
        fields = '__all__'
    def create(self, validated_data):

        user = User.objects.create(username=validated_data.get('Usuario')['username'])
        print(validated_data.get('Usuario'))

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

class ChangePasswordSerializer(serializers.Serializer):
    user = serializers.CharField(
        help_text = 'User',
    )
    password1 = serializers.CharField(
        help_text = 'New Password',
    )
    password2 = serializers.CharField(
        help_text = 'New Password (confirmation)',
    )


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


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ("Codigo","Nombre","Marca","Modelo","Is_dispositivo","Stock","Images")

class KitSerializer(serializers.HyperlinkedModelSerializer):
    #Items=ItemSerializer(many=True)
    class Meta:
        model = Item
        fields = ("Codigo","Nombre","Marca","Modelo","Stock","Images","Items")
