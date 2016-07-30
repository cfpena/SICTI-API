from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name')
class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    Usuario = UserSerializer()

    class Meta:
        model = Persona
        fields = '__all__'

class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ("Codigo","Nombre","Marca","Modelo","Is_dispositivo","Stock","Images")

class KitSerializer(serializers.HyperlinkedModelSerializer):
    Items=ItemSerializer(many=True)
    class Meta:
        model = Item
        fields = ("Codigo","Nombre","Marca","Modelo","Stock","Images","Items")
