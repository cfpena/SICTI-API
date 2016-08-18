from django.conf.urls import url,include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'usuarios', views.UserViewSet)
router.register(r'groupos', views.GroupViewSet)
router.register(r'prestador', views.PrestadorViewSet)
router.register(r'elementos', views.ElementoViewSet)
router.register(r'dispositivos', views.DispositivoViewSet)
router.register(r'kits', views.KitViewSet)
router.register(r'kitelemento', views.KitElementoViewSet)
router.register(r'prestamos', views.PrestamoViewSet)
router.register(r'ingresosegresos', views.IngresoEgresoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^password/$',views.AccountPassword.as_view()),
]

