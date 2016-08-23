from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,filters
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username','first_name','last_name')
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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

class PrestadorViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('CI','Nombre','Apellido','Email','Telefono','Genero')
    queryset = Prestador.objects.all()
    serializer_class = PrestadorSerializer

class ElementoViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre")
    queryset = Elemento.objects.filter(dispositivo=None)
    serializer_class = ElementoSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Objecto modificado correctamente' })

class DispositivoViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre")
    queryset = Dispositivo.objects.filter(kit=None)
    serializer_class = DispositivoSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Objecto modificado correctamente' })
class KitViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre")
    queryset = Kit.objects.all()
    serializer_class = KitSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Objecto modificado correctamente' })
class KitElementoViewSet(viewsets.ModelViewSet):
    queryset = KitContieneElemento.objects.all()
    serializer_class = KitContieneElementoSerializer

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

class IngresoEgresoViewSet(viewsets.ModelViewSet):
    queryset = IngresoEgreso.objects.all()
    serializer_class = IngresoEgresoSerializer


class ActaViewSet(viewsets.ModelViewSet):
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('Cedula,''Nombre','Apellido','Email','Telefono','Genero')
    queryset = Acta.objects.all()
    serializer_class = ActaSerializer

class DevolucionViewSet(viewsets.ModelViewSet):
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('Cedula,''Nombre','Apellido','Email','Telefono','Genero')
    queryset = Devolucion.objects.all()
    serializer_class = DevolucionSerializer
class FacturaIngresoViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('Acta','Fecha')
    queryset = FacturaIngreso.objects.all()
    serializer_class = FacturaIngresoSerializer

class ReporteInventario(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        fechaInicio=request.data['Fecha_Inicial']
        fechaFin=request.data['Fecha_Final']
        query = IngresoEgreso.objects.filter(Fecha__range=(fechaInicio,fechaFin))
        serializer_context = {
            'request': Request(request),
        }
        serializer = IngresoEgresoSerializer(query,context=serializer_context,many=True)
        return Response(serializer.data)
class ReportePrestamo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        fechaInicio=request.data['Fecha_Inicial']
        fechaFin=request.data['Fecha_Final']
        query = Prestamo.objects.filter(Fecha__range=(fechaInicio,fechaFin))
        serializer_context = {
            'request': Request(request),
        }
        serializer = PrestamoSerializer(query,context=serializer_context,many=True)
        return Response(serializer.data)

'''
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
'''