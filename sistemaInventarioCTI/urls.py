from django.conf.urls import url,include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)