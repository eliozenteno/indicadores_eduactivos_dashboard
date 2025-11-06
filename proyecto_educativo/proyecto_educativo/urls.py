"""
URL configuration for proyecto_educativo project.

Dashboard de Indicadores Educativos
===================================
Sistema para la Detección Temprana de Riesgo Académico
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API REST y Frontend de Indicadores
    path('', include('indicadores.urls')),
    
    # Django REST Framework browsable API (para desarrollo)
    path('api-auth/', include('rest_framework.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
