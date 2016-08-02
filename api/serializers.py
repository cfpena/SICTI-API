from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from rest_framework.decorators import api_view

#Tipo de Usuario
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
class UserSerializer(serializers.HyperlinkedModelSerializer):
    #groups=GroupSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ('username','groups')
class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Persona
        fields = ('CI','Nombre','Apellido','Email','Telefono','Genero')
class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
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
        persona = Persona.objects.create(CI=validated_data.get('CI'),
                                         Nombre=validated_data.get('Nombre'),
                                         Apellido=validated_data.get('Apellido'),
                                         Email=validated_data.get('Email'),
                                         Telefono=validated_data.get('Telefono'),
                                         Genero=validated_data.get('Genero'),
                                         Usuario=user)

        return persona

class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ("Codigo","Nombre","Marca","Modelo","Is_dispositivo","Stock","Images")

class KitSerializer(serializers.HyperlinkedModelSerializer):
    Items=ItemSerializer(many=True)
    class Meta:
        model = Item
        fields = ("Codigo","Nombre","Marca","Modelo","Stock","Images","Items")
