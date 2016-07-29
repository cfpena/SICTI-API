from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name')

class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = Personas
        fields = '__all__'
