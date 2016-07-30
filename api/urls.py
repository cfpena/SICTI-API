from django.conf.urls import url,include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'personas', views.PersonaViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'kits', views.KitViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^$', views.index, name='index'),
]
