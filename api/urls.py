from django.conf.urls import url,include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'usuarios', views.UserViewSet)
router.register(r'grupos', views.GroupViewSet)
router.register(r'prestador', views.PrestadorViewSet)
router.register(r'elementos', views.ElementoViewSet)
router.register(r'dispositivos', views.DispositivoViewSet)
router.register(r'ultimoelemento', views.ElementoUltimoViewSet)
router.register(r'ultimodispositivo', views.DispositivoUltimoViewSet)
router.register(r'ultimaacta', views.ActaUltimoViewSet)
router.register(r'ultimokit', views.KitUltimoViewSet)
router.register(r'kits', views.KitViewSet)
router.register(r'kitdetalle', views.KitDetalleViewSet)
router.register(r'prestamos', views.PrestamoViewSet)
router.register(r'ingresosegresos', views.IngresoEgresoViewSet)
router.register(r'actas', views.ActaViewSet)
router.register(r'devoluciones', views.DevolucionViewSet)
router.register(r'facturaingreso', views.FacturaIngresoViewSet)
router.register(r'identificaciones', views.IdentificacionesViewSet)


router.register(r'items', views.ItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^password/$',views.AccountPassword.as_view()),
    url(r'reporteinventariopdf', views.ReporteInventarioPDF.as_view()),
    url(r'reporteinventario', views.ReporteInventario.as_view()),
    url(r'reporteprestamo', views.ReportePrestamo.as_view()),
    url(r'reporteexistencia', views.ReporteExistencias.as_view()),
    url(r'itemupload', views.ItemUploadViewSet.as_view())
]


