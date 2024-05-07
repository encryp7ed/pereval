"""
URL configuration for travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app import views

schema_view = get_schema_view(
    openapi.Info(
        title="Pereval API",
        default_version='v1',
        description='API for all things',
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Подключение маршрутов из viewset'а
    path("create/", views.create),  # Путь для создания записей (POST)
    path("delete/<int:id>/", views.delete),  # Путь для удаления записей (GET)

    # Подключение аутентификации Django REST Framework
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Подключение документации Swagger
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]

# Указание пути Django, куда сохранять изображения
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
