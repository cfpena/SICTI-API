from rest_framework import viewsets,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.parsers import FormParser,MultiPartParser
from base64 import b64decode, b64encode,decodestring
from django.core.files.base import ContentFile
import uuid
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,  Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle,TA_CENTER,TA_LEFT
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime
import time


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username','first_name','last_name')
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
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
    queryset = Item.objects.filter(Es_Dispositivo=False)
    serializer_class = ItemSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Objecto modificado correctamente' })

class ElementoUltimoViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().filter(Es_Dispositivo=False).reverse()[:1]
    serializer_class = ElementoSerializer

class DispositivoUltimoViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().filter(Es_Dispositivo=True).reverse()[:1]
    serializer_class = DispositivoSerializer

class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo", "Nombre","Marca","Modelo")
    queryset = Item.objects.all().filter(kit=None)
    serializer_class = ItemSerializer


class ItemUploadViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):


        imagen=request.data['Imagen']
        if(imagen!=None):
            data=imagen['data']
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            id = uuid.uuid4()

            img = ContentFile(decodestring(imgstr), name=id.urn[9:] + '.' + ext)
            request.data['Imagen'] = img

        serializer_context = {
            'request': Request(request),
        }


        serializer = ItemSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response("OK")
        else:
            return Response(serializer.errors)






class DispositivoViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("Codigo","Nombre")
    queryset = Item.objects.filter(Es_Dispositivo=True)
    serializer_class = ItemSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Objecto modificado correctamente' })

class KitUltimoViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all().filter().reverse()[:1]
    serializer_class = KitUltimoSerializer

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



class KitDetalleViewSet(viewsets.ModelViewSet):
    queryset = KitDetalle.objects.all()
    serializer_class = KitDetalleSerializer

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

class IdentificacionesViewSet(viewsets.ModelViewSet):
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('Cedula,''Nombre','Apellido','Email','Telefono','Genero')
    queryset = Identificaciones.objects.all()
    serializer_class = IdentificacionesSerializer

class ActaUltimoViewSet(viewsets.ModelViewSet):
    queryset = Acta.objects.all().filter().reverse()[1:]
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

class ReporteExistencias(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        query = Item.objects.all()
        serializer_context = {
            'request': Request(request),
        }
        serializer = ItemReporteSerializer(query,context=serializer_context,many=True)
        return Response(serializer.data)

class ReporteInventarioPDF(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        fechaInicio=request.data['Fecha_Inicial']
        fechaFin=request.data['Fecha_Final']
        query = IngresoEgreso.objects.filter(Fecha__range=(fechaInicio,fechaFin))



        response = HttpResponse(content_type='application/pdf')
        pdf_name = "menu-%s.pdf" % str('reporte')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        buff = BytesIO()

        menu_pdf = SimpleDocTemplate(buff, rightMargin=72,
                                     leftMargin=72, topMargin=72, bottomMargin=18)

        # container for pdf elements
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))


        formatted_time = time.ctime()
        ptext = '<font size=12>%s</font>' % formatted_time

        elements.append(Paragraph(ptext, styles["Normal"]))
        elements.append(Spacer(1, 12))
        ptext = '<b><font size=16>%s</font></b>' % 'Reporte de Inventario'
        elements.append(Paragraph(ptext, styles["centered"]))
        elements.append(Spacer(1, 30))
        data = []
        headers=['Fecha','Nombre','Cantidad','Tipo','Detalle']
        data.append(headers)
        for dato in query:
            movimiento=[]
            ptext = '<b><font size=12>%s</font></b>' % str(dato.Fecha)
            movimiento.append(Paragraph(ptext,styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Item.Nombre
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Cantidad
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Tipo
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Detalle
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            data.append(movimiento)
        table=Table(data)
        elements.append(table)


        # Add the content as before then...

        menu_pdf.build(elements)
        response.write(buff.getvalue())
        buff.close()
        return response




class ReportePrestamoPDF(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        fechaInicio=request.data['Fecha_Inicial']
        fechaFin=request.data['Fecha_Final']
        query = Prestamo.objects.filter(Fecha__range=(fechaInicio,fechaFin))



        response = HttpResponse(content_type='application/pdf')
        pdf_name = "menu-%s.pdf" % str('reporte')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        buff = BytesIO()

        menu_pdf = SimpleDocTemplate(buff, rightMargin=72,
                                     leftMargin=72, topMargin=72, bottomMargin=18)

        # container for pdf elements
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))


        formatted_time = time.ctime()
        ptext = '<font size=12>%s</font>' % formatted_time

        elements.append(Paragraph(ptext, styles["Normal"]))
        elements.append(Spacer(1, 12))
        ptext = '<b><font size=16>%s</font></b>' % 'Reporte de Prestamos'
        elements.append(Paragraph(ptext, styles["centered"]))
        elements.append(Spacer(1, 30))
        data = []
        headers=['Fecha','Nombre','Item','Cantidad','Acta','Detalle']
        data.append(headers)
        for dato in query:
            movimiento=[]
            ptext = '<b><font size=12>%s</font></b>' % str(dato.Fecha)
            movimiento.append(Paragraph(ptext,styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % (str(dato.Acta.Prestador.Nombre) +' '+ (dato.Acta.Prestador.Apellido))
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Item.Nombre
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Cantidad
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Acta.Codigo
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Detalle
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            data.append(movimiento)
        table=Table(data)
        elements.append(table)


        # Add the content as before then...

        menu_pdf.build(elements)
        response.write(buff.getvalue())
        buff.close()
        return response


class ReporteExistenciasPDF(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        query = Item.objects.all()



        response = HttpResponse(content_type='application/pdf')
        pdf_name = "menu-%s.pdf" % str('reporte')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        buff = BytesIO()

        menu_pdf = SimpleDocTemplate(buff, rightMargin=72,
                                     leftMargin=72, topMargin=72, bottomMargin=18)

        # container for pdf elements
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))


        formatted_time = time.ctime()
        ptext = '<font size=12>%s</font>' % formatted_time

        elements.append(Paragraph(ptext, styles["Normal"]))
        elements.append(Spacer(1, 12))
        ptext = '<b><font size=16>%s</font></b>' % 'Reporte de Existencias'
        elements.append(Paragraph(ptext, styles["centered"]))
        elements.append(Spacer(1, 30))
        data = []
        headers=['Codigo','Nombre','Marca','Modelo','Stock','Disponible']
        data.append(headers)
        for dato in query:
            movimiento=[]
            ptext = '<b><font size=12>%s</font></b>' % str(dato.Codigo)
            movimiento.append(Paragraph(ptext,styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % (str(dato.Nombre))
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Marca
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Modelo
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Stock
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            ptext = '<b><font size=12>%s</font></b>' % dato.Stock_Disponible
            movimiento.append(Paragraph(ptext, styles["Normal"]))
            data.append(movimiento)
        table=Table(data)
        elements.append(table)


        # Add the content as before then...

        menu_pdf.build(elements)
        response.write(buff.getvalue())
        buff.close()
        return response