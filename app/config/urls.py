from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('layout.urls')),
    path("users/", include('users.urls')),
    path("posts/", include('posts.urls')),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
