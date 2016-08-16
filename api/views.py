from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,filters
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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
    queryset = Persona.objects.filter(Usuario=None)
    serializer_class = PersonaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('Nombre','Apellido','Email','Telefono','Genero','id')
    queryset = Persona.objects.exclude(Usuario=None)
    serializer_class = UsuarioSerializer
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Object successfully changed' })
class AccountPassword(generics.GenericAPIView):

    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def post(self, request, format=None):
        """ validate password change operation and return result """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data, instance=request.user)

        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Password successfully changed' })
        return Response(serializer.errors, status=400)

class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre","Marca","Modelo","Is_dispositivo")
    queryset = Item.objects.filter(Is_kit=False)
    serializer_class = ItemSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Object successfully changed' })

class KitViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre","Marca","Modelo")
    queryset = Item.objects.filter(Is_kit=True)
    serializer_class = KitSerializer
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Object successfully changed' })
class PrestamoViewSet(viewsets.ModelViewSet):
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ("Codigo","Nombre","Marca","Modelo")
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
class MovimientoViewSet(viewsets.ModelViewSet):
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ("Codigo","Nombre","Marca","Modelo")
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

# Create your views here.
