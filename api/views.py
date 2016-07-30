from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,filters
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError
from .serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username')
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@token_required
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('Nombre','Apellido','Email','Telefono','Genero')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('Nombre','Apellido','Email','Telefono','Genero')
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
class UsuarioViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('Nombre','Apellido','Email','Telefono','Genero')
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre","Marca","Modelo","Is_dispositivo")
    queryset = Item.objects.filter(Is_kit=False)
    serializer_class = ItemSerializer

class KitViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre","Marca","Modelo")
    queryset = Item.objects.filter(Is_kit=True)
    serializer_class = KitSerializer


# Create your views here.
