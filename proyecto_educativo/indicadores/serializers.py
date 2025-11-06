"""
Serializers para la API REST de Indicadores Educativos
======================================================
Convierte los modelos Django en JSON para la API REST
"""

from rest_framework import serializers
from .models import (
    Grado, Asignatura, PeriodoAcademico, Profesor, Estudiante, 
    Apoderado, Curso, Inscripcion, EstudianteApoderado, 
    Evaluacion, Calificacion, Asistencia
)

class GradoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Grado"""
    class Meta:
        model = Grado
        fields = ['id', 'nombre', 'descripcion']

class AsignaturaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Asignatura"""
    class Meta:
        model = Asignatura
        fields = ['id', 'nombre', 'codigo', 'descripcion']

class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo PeriodoAcademico"""
    class Meta:
        model = PeriodoAcademico
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'activo']

class ProfesorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Profesor"""
    nombre_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Profesor
        fields = ['id', 'nombres', 'apellidos', 'nombre_completo', 'email', 
                 'telefono', 'especialidad', 'activo']

class EstudianteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Estudiante"""
    nombre_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Estudiante
        fields = ['id', 'nombres', 'apellidos', 'nombre_completo', 'ci', 
                 'email', 'telefono', 'fecha_nacimiento', 'direccion', 'activo']

class ApoderadoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Apoderado"""
    nombre_completo = serializers.ReadOnlyField()
    parentesco_display = serializers.CharField(source='get_parentesco_display', read_only=True)
    
    class Meta:
        model = Apoderado
        fields = ['id', 'nombres', 'apellidos', 'nombre_completo', 'ci', 
                 'email', 'telefono', 'direccion', 'parentesco', 'parentesco_display']

class CursoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Curso"""
    grado_nombre = serializers.CharField(source='grado.nombre', read_only=True)
    asignatura_nombre = serializers.CharField(source='asignatura.nombre', read_only=True)
    asignatura_codigo = serializers.CharField(source='asignatura.codigo', read_only=True)
    profesor_nombre = serializers.CharField(source='profesor.nombre_completo', read_only=True)
    periodo_nombre = serializers.CharField(source='periodo_academico.nombre', read_only=True)
    
    class Meta:
        model = Curso
        fields = ['id', 'grado', 'grado_nombre', 'asignatura', 'asignatura_nombre', 
                 'asignatura_codigo', 'profesor', 'profesor_nombre', 'periodo_academico', 
                 'periodo_nombre', 'seccion']

class InscripcionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Inscripcion"""
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    estudiante_ci = serializers.CharField(source='estudiante.ci', read_only=True)
    curso_info = serializers.CharField(source='curso.__str__', read_only=True)
    
    class Meta:
        model = Inscripcion
        fields = ['id', 'estudiante', 'estudiante_nombre', 'estudiante_ci', 
                 'curso', 'curso_info', 'fecha_inscripcion', 'activa']

class EstudianteApoderadoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo EstudianteApoderado"""
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    apoderado_nombre = serializers.CharField(source='apoderado.nombre_completo', read_only=True)
    apoderado_parentesco = serializers.CharField(source='apoderado.get_parentesco_display', read_only=True)
    
    class Meta:
        model = EstudianteApoderado
        fields = ['id', 'estudiante', 'estudiante_nombre', 'apoderado', 
                 'apoderado_nombre', 'apoderado_parentesco', 'es_principal', 
                 'fecha_asignacion', 'activa']

class EvaluacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Evaluacion"""
    curso_info = serializers.CharField(source='curso.__str__', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Evaluacion
        fields = ['id', 'curso', 'curso_info', 'nombre', 'descripcion', 
                 'tipo', 'tipo_display', 'fecha', 'ponderacion']

class CalificacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Calificacion"""
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    estudiante_ci = serializers.CharField(source='estudiante.ci', read_only=True)
    evaluacion_nombre = serializers.CharField(source='evaluacion.nombre', read_only=True)
    evaluacion_tipo = serializers.CharField(source='evaluacion.get_tipo_display', read_only=True)
    curso_info = serializers.CharField(source='evaluacion.curso.__str__', read_only=True)
    
    class Meta:
        model = Calificacion
        fields = ['id', 'evaluacion', 'evaluacion_nombre', 'evaluacion_tipo', 
                 'curso_info', 'estudiante', 'estudiante_nombre', 'estudiante_ci', 
                 'nota', 'fecha_registro', 'observaciones']

class AsistenciaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Asistencia"""
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    estudiante_ci = serializers.CharField(source='estudiante.ci', read_only=True)
    curso_info = serializers.CharField(source='curso.__str__', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Asistencia
        fields = ['id', 'estudiante', 'estudiante_nombre', 'estudiante_ci', 
                 'curso', 'curso_info', 'fecha', 'estado', 'estado_display', 
                 'observaciones']

# Serializers especiales para KPIs y Dashboard
# ============================================

class EstudianteConPromedioSerializer(serializers.ModelSerializer):
    """Serializer con promedio de notas calculado"""
    nombre_completo = serializers.ReadOnlyField()
    promedio_general = serializers.SerializerMethodField()
    total_evaluaciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Estudiante
        fields = ['id', 'nombres', 'apellidos', 'nombre_completo', 'ci', 
                 'promedio_general', 'total_evaluaciones']
    
    def get_promedio_general(self, obj):
        """Calcula el promedio general del estudiante"""
        calificaciones = obj.calificacion_set.all()
        if calificaciones:
            return round(sum(c.nota for c in calificaciones) / len(calificaciones), 2)
        return 0
    
    def get_total_evaluaciones(self, obj):
        """Cuenta total de evaluaciones del estudiante"""
        return obj.calificacion_set.count()

class CursoConEstadisticasSerializer(serializers.ModelSerializer):
    """Serializer con estadísticas del curso"""
    grado_nombre = serializers.CharField(source='grado.nombre', read_only=True)
    asignatura_nombre = serializers.CharField(source='asignatura.nombre', read_only=True)
    profesor_nombre = serializers.CharField(source='profesor.nombre_completo', read_only=True)
    total_estudiantes = serializers.SerializerMethodField()
    promedio_curso = serializers.SerializerMethodField()
    total_evaluaciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ['id', 'grado_nombre', 'asignatura_nombre', 'profesor_nombre', 
                 'seccion', 'total_estudiantes', 'promedio_curso', 'total_evaluaciones']
    
    def get_total_estudiantes(self, obj):
        """Cuenta estudiantes inscritos en el curso"""
        return obj.inscripcion_set.filter(activa=True).count()
    
    def get_promedio_curso(self, obj):
        """Calcula promedio general del curso"""
        from django.db.models import Avg
        evaluaciones = obj.evaluacion_set.all()
        if evaluaciones:
            promedio = Calificacion.objects.filter(
                evaluacion__in=evaluaciones
            ).aggregate(Avg('nota'))['nota__avg']
            return round(promedio, 2) if promedio else 0
        return 0
    
    def get_total_evaluaciones(self, obj):
        """Cuenta evaluaciones del curso"""
        return obj.evaluacion_set.count()