"""
URLs para la app Indicadores
============================
Configuración de rutas para API REST y Frontend
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Router para API REST
# ===================
router = DefaultRouter()
router.register(r'grados', views.GradoViewSet)
router.register(r'asignaturas', views.AsignaturaViewSet)
router.register(r'periodos-academicos', views.PeriodoAcademicoViewSet)
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'apoderados', views.ApoderadoViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'inscripciones', views.InscripcionViewSet)
router.register(r'estudiante-apoderado', views.EstudianteApoderadoViewSet)
router.register(r'evaluaciones', views.EvaluacionViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)
router.register(r'asistencia', views.AsistenciaViewSet)
router.register(r'dashboard', views.DashboardAPIViewSet, basename='dashboard')

app_name = 'indicadores'

urlpatterns = [
    # API REST endpoints
    path('api/', include(router.urls)),
    
    # Frontend Django views - Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Gestión de Estudiantes
    path('estudiantes/', views.estudiantes_list_view, name='estudiantes_list'),
    
    # Gestión de Profesores
    path('profesores/', views.profesores_list_view, name='profesores_list'),
    
    # Gestión de Cursos
    path('cursos/', views.cursos_list_view, name='cursos_list'),
    
    # Gestión de Inscripciones
    path('inscripciones/', views.inscripciones_list_view, name='inscripciones_list'),
    
    # Gestión de Evaluaciones
    path('evaluaciones/', views.evaluaciones_list_view, name='evaluaciones_list'),
    
    # Registro de Calificaciones
    path('registrar-calificacion/', views.registrar_calificacion_view, name='registrar_calificacion'),
    
    # Registro de Asistencia
    path('registrar-asistencia/', views.registrar_asistencia_view, name='registrar_asistencia'),
    
    # Gestión de Apoderados
    path('apoderados/', views.apoderados_list_view, name='apoderados_list'),
    path('apoderados/vincular/', views.vincular_apoderado_view, name='vincular_apoderado'),
]