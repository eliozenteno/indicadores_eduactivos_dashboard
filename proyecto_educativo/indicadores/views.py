"""
Views para la API REST y Frontend de Indicadores Educativos
===========================================================
"""

from django.shortcuts import render, redirect
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Grado, Asignatura, PeriodoAcademico, Profesor, Estudiante, 
    Apoderado, Curso, Inscripcion, EstudianteApoderado, 
    Evaluacion, Calificacion, Asistencia
)

from .serializers import (
    GradoSerializer, AsignaturaSerializer, PeriodoAcademicoSerializer,
    ProfesorSerializer, EstudianteSerializer, ApoderadoSerializer,
    CursoSerializer, InscripcionSerializer, EstudianteApoderadoSerializer,
    EvaluacionSerializer, CalificacionSerializer, AsistenciaSerializer,
    EstudianteConPromedioSerializer, CursoConEstadisticasSerializer
)

# ============================================
# VIEWSETS PARA API REST (Backend)
# ============================================

class GradoViewSet(viewsets.ModelViewSet):
    """API ViewSet para Grados"""
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre']
    ordering = ['nombre']

class AsignaturaViewSet(viewsets.ModelViewSet):
    """API ViewSet para Asignaturas"""
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'codigo']
    ordering = ['codigo']

class PeriodoAcademicoViewSet(viewsets.ModelViewSet):
    """API ViewSet para Períodos Académicos"""
    queryset = PeriodoAcademico.objects.all()
    serializer_class = PeriodoAcademicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre']
    ordering = ['-fecha_inicio']

class ProfesorViewSet(viewsets.ModelViewSet):
    """API ViewSet para Profesores"""
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['activo', 'especialidad']
    search_fields = ['nombres', 'apellidos', 'email']
    ordering = ['apellidos', 'nombres']

class EstudianteViewSet(viewsets.ModelViewSet):
    """API ViewSet para Estudiantes"""
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['activo']
    search_fields = ['nombres', 'apellidos', 'ci', 'email']
    ordering = ['apellidos', 'nombres']
    
    @action(detail=False, methods=['get'])
    def con_promedio(self, request):
        """Endpoint para estudiantes con promedio calculado"""
        estudiantes = self.get_queryset()
        serializer = EstudianteConPromedioSerializer(estudiantes, many=True)
        return Response(serializer.data)

class ApoderadoViewSet(viewsets.ModelViewSet):
    """API ViewSet para Apoderados"""
    queryset = Apoderado.objects.all()
    serializer_class = ApoderadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['parentesco']
    search_fields = ['nombres', 'apellidos', 'ci']
    ordering = ['apellidos', 'nombres']

class CursoViewSet(viewsets.ModelViewSet):
    """API ViewSet para Cursos"""
    queryset = Curso.objects.select_related('grado', 'asignatura', 'profesor', 'periodo_academico')
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['grado', 'asignatura', 'profesor', 'periodo_academico', 'seccion']
    search_fields = ['grado__nombre', 'asignatura__nombre', 'profesor__nombres', 'profesor__apellidos']
    ordering = ['grado__nombre', 'asignatura__codigo']
    
    @action(detail=False, methods=['get'])
    def con_estadisticas(self, request):
        """Endpoint para cursos con estadísticas calculadas"""
        cursos = self.get_queryset()
        serializer = CursoConEstadisticasSerializer(cursos, many=True)
        return Response(serializer.data)

class InscripcionViewSet(viewsets.ModelViewSet):
    """API ViewSet para Inscripciones"""
    queryset = Inscripcion.objects.select_related('estudiante', 'curso')
    serializer_class = InscripcionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['activa', 'curso', 'estudiante']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos', 'estudiante__ci']
    ordering = ['-fecha_inscripcion']

class EstudianteApoderadoViewSet(viewsets.ModelViewSet):
    """API ViewSet para relación Estudiante-Apoderado"""
    queryset = EstudianteApoderado.objects.select_related('estudiante', 'apoderado')
    serializer_class = EstudianteApoderadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['es_principal', 'activa', 'estudiante', 'apoderado']
    ordering = ['estudiante__apellidos']

class EvaluacionViewSet(viewsets.ModelViewSet):
    """API ViewSet para Evaluaciones"""
    queryset = Evaluacion.objects.select_related('curso')
    serializer_class = EvaluacionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipo', 'curso', 'fecha']
    search_fields = ['nombre', 'curso__asignatura__nombre']
    ordering = ['-fecha']

class CalificacionViewSet(viewsets.ModelViewSet):
    """API ViewSet para Calificaciones"""
    queryset = Calificacion.objects.select_related('evaluacion', 'estudiante')
    serializer_class = CalificacionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['evaluacion', 'estudiante', 'evaluacion__curso']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos', 'evaluacion__nombre']
    ordering = ['-fecha_registro']

class AsistenciaViewSet(viewsets.ModelViewSet):
    """API ViewSet para Asistencia"""
    queryset = Asistencia.objects.select_related('estudiante', 'curso')
    serializer_class = AsistenciaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'curso', 'estudiante', 'fecha']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos']
    ordering = ['-fecha']

# ============================================
# VIEWS PARA DASHBOARD Y KPIs
# ============================================

class DashboardAPIViewSet(viewsets.ViewSet):
    """API especializada para KPIs del Dashboard"""
    
    @action(detail=False, methods=['get'])
    def kpis_generales(self, request):
        """KPIs generales del sistema"""
        data = {
            'total_estudiantes': Estudiante.objects.filter(activo=True).count(),
            'total_profesores': Profesor.objects.filter(activo=True).count(),
            'total_cursos': Curso.objects.count(),
            'total_evaluaciones': Evaluacion.objects.count(),
            'promedio_general': Calificacion.objects.aggregate(Avg('nota'))['nota__avg'] or 0,
        }
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def estudiantes_riesgo(self, request):
        """Estudiantes en riesgo académico"""
        # Estudiantes con promedio < 60 o ausentismo > 20%
        estudiantes_riesgo = []
        
        for estudiante in Estudiante.objects.filter(activo=True):
            # Calcular promedio
            calificaciones = Calificacion.objects.filter(estudiante=estudiante)
            if calificaciones.exists():
                promedio = calificaciones.aggregate(Avg('nota'))['nota__avg']
                
                # Calcular ausentismo
                total_asistencias = Asistencia.objects.filter(estudiante=estudiante).count()
                ausencias = Asistencia.objects.filter(
                    estudiante=estudiante, 
                    estado__in=['ausente', 'tardanza']
                ).count()
                
                porcentaje_ausentismo = (ausencias / total_asistencias * 100) if total_asistencias > 0 else 0
                
                # Determinar nivel de riesgo
                if promedio < 60 or porcentaje_ausentismo > 20:
                    nivel = 'ALTO' if (promedio < 50 or porcentaje_ausentismo > 30) else 'MEDIO'
                    estudiantes_riesgo.append({
                        'id': estudiante.id,
                        'nombre_completo': estudiante.nombre_completo,
                        'ci': estudiante.ci,
                        'promedio': round(promedio, 2),
                        'ausentismo': round(porcentaje_ausentismo, 2),
                        'nivel_riesgo': nivel
                    })
        
        return Response(estudiantes_riesgo)
    
    @action(detail=False, methods=['get'])
    def promedio_por_curso(self, request):
        """Promedio de notas por curso"""
        cursos_data = []
        
        for curso in Curso.objects.all():
            evaluaciones = Evaluacion.objects.filter(curso=curso)
            if evaluaciones.exists():
                promedio = Calificacion.objects.filter(
                    evaluacion__in=evaluaciones
                ).aggregate(Avg('nota'))['nota__avg']
                
                cursos_data.append({
                    'curso_id': curso.id,
                    'grado': curso.grado.nombre,
                    'asignatura': curso.asignatura.nombre,
                    'seccion': curso.seccion,
                    'profesor': curso.profesor.nombre_completo,
                    'promedio': round(promedio, 2) if promedio else 0,
                    'total_estudiantes': curso.inscripcion_set.filter(activa=True).count()
                })
        
        return Response(cursos_data)
    
    @action(detail=False, methods=['get'])
    def ausentismo_por_curso(self, request):
        """Tasa de ausentismo por curso"""
        ausentismo_data = []
        
        for curso in Curso.objects.all():
            total_registros = Asistencia.objects.filter(curso=curso).count()
            ausencias = Asistencia.objects.filter(
                curso=curso, 
                estado__in=['ausente', 'tardanza']
            ).count()
            
            porcentaje_ausentismo = (ausencias / total_registros * 100) if total_registros > 0 else 0
            
            ausentismo_data.append({
                'curso_id': curso.id,
                'grado': curso.grado.nombre,
                'asignatura': curso.asignatura.nombre,
                'seccion': curso.seccion,
                'total_registros': total_registros,
                'ausencias': ausencias,
                'porcentaje_ausentismo': round(porcentaje_ausentismo, 2)
            })
        
        return Response(ausentismo_data)

# ============================================
# VIEWS PARA FRONTEND DJANGO (Templates)
# ============================================

def dashboard_view(request):
    """Vista principal del dashboard con KPIs mejorados"""
    from django.db.models import Avg, Count, Q, Case, When, IntegerField
    import json
    from datetime import date, timedelta
    from django.db.models.functions import TruncMonth
    
    # ============================================
    # ESTADÍSTICAS GENERALES
    # ============================================
    total_estudiantes = Estudiante.objects.filter(activo=True).count()
    total_profesores = Profesor.objects.filter(activo=True).count()
    total_cursos = Curso.objects.count()
    total_evaluaciones = Evaluacion.objects.count()
    
    # Promedio general de calificaciones
    promedio_general = Calificacion.objects.aggregate(Avg('nota'))['nota__avg']
    
    # ============================================
    # NUEVO KPI: TASA DE APROBACIÓN
    # ============================================
    total_calificaciones = Calificacion.objects.count()
    aprobados = Calificacion.objects.filter(nota__gte=51).count()
    tasa_aprobacion = round((aprobados / total_calificaciones * 100), 1) if total_calificaciones > 0 else 0
    
    # ============================================
    # NUEVO KPI: TOP 5 ESTUDIANTES
    # ============================================
    top_estudiantes = Estudiante.objects.filter(
        activo=True,
        calificacion__isnull=False
    ).annotate(
        promedio=Avg('calificacion__nota'),
        total_notas=Count('calificacion')
    ).filter(total_notas__gte=3).order_by('-promedio')[:5]
    
    # ============================================
    # NUEVO KPI: DISTRIBUCIÓN DE NOTAS
    # ============================================
    distribucion_notas = {
        'excelente': Calificacion.objects.filter(nota__gte=90).count(),
        'bueno': Calificacion.objects.filter(nota__gte=70, nota__lt=90).count(),
        'regular': Calificacion.objects.filter(nota__gte=51, nota__lt=70).count(),
        'insuficiente': Calificacion.objects.filter(nota__lt=51).count(),
    }
    
    distribucion_notas_json = json.dumps({
        'labels': ['Excelente (90-100)', 'Bueno (70-89)', 'Regular (51-69)', 'Insuficiente (0-50)'],
        'data': [
            distribucion_notas['excelente'],
            distribucion_notas['bueno'],
            distribucion_notas['regular'],
            distribucion_notas['insuficiente']
        ]
    })
    
    # ============================================
    # NUEVO KPI: TENDENCIA MENSUAL
    # ============================================
    # Últimos 6 meses de promedios
    fecha_inicio = date.today() - timedelta(days=180)
    tendencia_mensual = Calificacion.objects.filter(
        fecha_registro__gte=fecha_inicio
    ).annotate(
        mes=TruncMonth('fecha_registro')
    ).values('mes').annotate(
        promedio=Avg('nota')
    ).order_by('mes')
    
    tendencia_mensual_json = json.dumps({
        'labels': [item['mes'].strftime('%B %Y') for item in tendencia_mensual],
        'data': [float(item['promedio']) for item in tendencia_mensual]
    })
    
    # ============================================
    # NUEVO KPI: AUSENTISMO MENSUAL
    # ============================================
    ausentismo_mensual = Asistencia.objects.filter(
        fecha__gte=fecha_inicio
    ).annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total=Count('id'),
        ausentes=Count(Case(When(estado='ausente', then=1), output_field=IntegerField()))
    ).order_by('mes')
    
    ausentismo_mensual_json = json.dumps({
        'labels': [item['mes'].strftime('%B %Y') for item in ausentismo_mensual],
        'data': [round((item['ausentes'] / item['total'] * 100), 1) if item['total'] > 0 else 0 
                 for item in ausentismo_mensual]
    })
    
    # ============================================
    # NUEVO KPI: PROFESORES DESTACADOS
    # ============================================
    profesores_destacados = Profesor.objects.filter(
        activo=True,
        curso__evaluacion__calificacion__isnull=False
    ).annotate(
        promedio_curso=Avg('curso__evaluacion__calificacion__nota'),
        total_estudiantes=Count('curso__inscripcion', distinct=True)
    ).order_by('-promedio_curso')[:5]
    
    # ============================================
    # CALIFICACIONES RECIENTES
    # ============================================
    calificaciones_recientes = Calificacion.objects.select_related(
        'estudiante', 'evaluacion', 'evaluacion__curso'
    ).order_by('-fecha_registro')[:5]
    
    # ============================================
    # ESTUDIANTES EN RIESGO (promedio < 51)
    # ============================================
    estudiantes_riesgo = Estudiante.objects.filter(
        activo=True,
        calificacion__isnull=False
    ).annotate(
        promedio=Avg('calificacion__nota')
    ).filter(promedio__lt=51).order_by('promedio')[:5]
    
    # ============================================
    # NUEVO: EVALUACIONES PRÓXIMAS (próximos 7 días)
    # ============================================
    fecha_fin = date.today() + timedelta(days=7)
    evaluaciones_proximas = Evaluacion.objects.filter(
        fecha__gte=date.today(),
        fecha__lte=fecha_fin
    ).select_related('curso', 'curso__asignatura', 'curso__grado').order_by('fecha')[:5]
    
    # ============================================
    # GRÁFICO: PROMEDIOS POR CURSO
    # ============================================
    promedios_cursos = Curso.objects.annotate(
        promedio=Avg('evaluacion__calificacion__nota')
    ).filter(promedio__isnull=False).order_by('-promedio')[:10]
    
    promedios_cursos_json = json.dumps({
        'labels': [f"{c.grado} - {c.asignatura.nombre[:15]}" for c in promedios_cursos],
        'data': [float(c.promedio) if c.promedio else 0 for c in promedios_cursos]
    })
    
    # ============================================
    # GRÁFICO: DISTRIBUCIÓN ASISTENCIA HOY
    # ============================================
    asistencia_stats = Asistencia.objects.filter(
        fecha=date.today()
    ).values('estado').annotate(total=Count('id'))
    
    asistencia_dict = {item['estado']: item['total'] for item in asistencia_stats}
    asistencia_data_json = json.dumps({
        'labels': ['Presente', 'Ausente', 'Tardanza', 'Justificada'],
        'data': [
            asistencia_dict.get('presente', 0),
            asistencia_dict.get('ausente', 0),
            asistencia_dict.get('tardanza', 0),
            asistencia_dict.get('justificada', 0),
        ]
    })
    
    context = {
        'title': 'Dashboard de Indicadores Educativos',
        # KPIs básicos
        'total_estudiantes': total_estudiantes,
        'total_profesores': total_profesores,
        'total_cursos': total_cursos,
        'total_evaluaciones': total_evaluaciones,
        'promedio_general': promedio_general,
        # Nuevos KPIs
        'tasa_aprobacion': tasa_aprobacion,
        'top_estudiantes': top_estudiantes,
        'distribucion_notas': distribucion_notas,
        'profesores_destacados': profesores_destacados,
        'evaluaciones_proximas': evaluaciones_proximas,
        # Tablas
        'calificaciones_recientes': calificaciones_recientes,
        'estudiantes_riesgo': estudiantes_riesgo,
        # JSON para gráficos
        'promedios_cursos_json': promedios_cursos_json,
        'asistencia_data_json': asistencia_data_json,
        'distribucion_notas_json': distribucion_notas_json,
        'tendencia_mensual_json': tendencia_mensual_json,
        'ausentismo_mensual_json': ausentismo_mensual_json,
    }
    return render(request, 'dashboard/index.html', context)

def estudiantes_list_view(request):
    """Vista para listar y registrar estudiantes"""
    from .forms import EstudianteForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estudiante registrado correctamente.')
            return redirect('indicadores:estudiantes_list')
    else:
        form = EstudianteForm()
    
    estudiantes = Estudiante.objects.filter(activo=True).order_by('apellidos', 'nombres')
    return render(request, 'estudiantes/list.html', {
        'estudiantes': estudiantes,
        'form': form
    })

def registrar_calificacion_view(request):
    """Vista para registrar calificaciones"""
    from .forms import CalificacionForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calificación registrada correctamente.')
            return redirect('indicadores:registrar_calificacion')
    else:
        form = CalificacionForm()
    
    # Últimas calificaciones registradas
    ultimas_calificaciones = Calificacion.objects.select_related(
        'estudiante', 'evaluacion'
    ).order_by('-fecha_registro')[:5]
    
    return render(request, 'calificaciones/registrar.html', {
        'form': form,
        'ultimas_calificaciones': ultimas_calificaciones
    })

def registrar_asistencia_view(request):
    """Vista para registrar asistencia"""
    from .forms import AsistenciaForm
    from django.contrib import messages
    from datetime import date
    
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia registrada correctamente.')
            return redirect('indicadores:registrar_asistencia')
    else:
        form = AsistenciaForm()
    
    # Resumen de asistencia de hoy
    from django.db.models import Count
    resumen_hoy = Asistencia.objects.filter(fecha=date.today()).values('estado').annotate(
        total=Count('id')
    )
    
    resumen_dict = {item['estado']: item['total'] for item in resumen_hoy}
    resumen_data = {
        'presentes': resumen_dict.get('presente', 0),
        'ausentes': resumen_dict.get('ausente', 0),
        'tardanzas': resumen_dict.get('tardanza', 0),
        'justificadas': resumen_dict.get('justificada', 0),
    }
    
    return render(request, 'asistencia/registrar.html', {
        'form': form,
        'resumen_hoy': resumen_data if sum(resumen_data.values()) > 0 else None
    })

# ============================================
# NUEVAS VIEWS PARA FORMULARIOS FALTANTES
# ============================================

def profesores_list_view(request):
    """Vista para listar y registrar profesores"""
    from .forms import ProfesorForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profesor registrado correctamente.')
            return redirect('indicadores:profesores_list')
    else:
        form = ProfesorForm()
    
    profesores = Profesor.objects.filter(activo=True).order_by('apellidos', 'nombres')
    return render(request, 'profesores/list.html', {
        'profesores': profesores,
        'form': form
    })

def cursos_list_view(request):
    """Vista para listar y crear cursos"""
    from .forms import CursoForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Curso creado correctamente.')
            return redirect('indicadores:cursos_list')
    else:
        form = CursoForm()
    
    cursos = Curso.objects.select_related(
        'grado', 'asignatura', 'profesor', 'periodo_academico'
    ).order_by('grado__nombre', 'asignatura__codigo')
    
    return render(request, 'cursos/list.html', {
        'cursos': cursos,
        'form': form
    })

def inscripciones_list_view(request):
    """Vista para listar y crear inscripciones"""
    from .forms import InscripcionForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Inscripción realizada correctamente.')
            return redirect('indicadores:inscripciones_list')
    else:
        form = InscripcionForm()
    
    inscripciones = Inscripcion.objects.select_related(
        'estudiante', 'curso', 'curso__asignatura', 'curso__grado'
    ).filter(activa=True).order_by('-fecha_inscripcion')[:50]
    
    return render(request, 'inscripciones/list.html', {
        'inscripciones': inscripciones,
        'form': form
    })

def evaluaciones_list_view(request):
    """Vista para listar y crear evaluaciones"""
    from .forms import EvaluacionForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Evaluación creada correctamente.')
            return redirect('indicadores:evaluaciones_list')
    else:
        form = EvaluacionForm()
    
    evaluaciones = Evaluacion.objects.select_related(
        'curso', 'curso__asignatura', 'curso__grado', 'curso__profesor'
    ).order_by('-fecha')[:30]
    
    return render(request, 'evaluaciones/list.html', {
        'evaluaciones': evaluaciones,
        'form': form
    })

def apoderados_list_view(request):
    """Vista para listar y registrar apoderados"""
    from .forms import ApoderadoForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Apoderado registrado correctamente.')
            return redirect('indicadores:apoderados_list')
    else:
        form = ApoderadoForm()
    
    apoderados = Apoderado.objects.all().order_by('apellidos', 'nombres')
    return render(request, 'apoderados/list.html', {
        'apoderados': apoderados,
        'form': form
    })

def vincular_apoderado_view(request):
    """Vista para vincular estudiante con apoderado"""
    from .forms import EstudianteApoderadoForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = EstudianteApoderadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Estudiante vinculado con apoderado correctamente.')
            return redirect('indicadores:vincular_apoderado')
    else:
        form = EstudianteApoderadoForm()
    
    # Vínculos activos recientes
    vinculos = EstudianteApoderado.objects.select_related(
        'estudiante', 'apoderado'
    ).filter(activa=True).order_by('-estudiante__apellidos')[:20]
    
    return render(request, 'apoderados/vincular.html', {
        'form': form,
        'vinculos': vinculos
    })

