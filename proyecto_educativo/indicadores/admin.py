from django.contrib import admin
from .models import (
    Grado, Asignatura, PeriodoAcademico, Profesor, Estudiante, 
    Apoderado, Curso, Inscripcion, EstudianteApoderado, 
    Evaluacion, Calificacion, Asistencia
)

@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']
    ordering = ['nombre']

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'descripcion']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']

@admin.register(PeriodoAcademico)
class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['activo', 'fecha_inicio']
    search_fields = ['nombre']
    ordering = ['-fecha_inicio']

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'especialidad', 'activo']
    list_filter = ['activo', 'especialidad']
    search_fields = ['nombres', 'apellidos', 'email']
    ordering = ['apellidos', 'nombres']

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'ci', 'email', 'fecha_nacimiento', 'activo']
    list_filter = ['activo', 'fecha_nacimiento']
    search_fields = ['nombres', 'apellidos', 'ci', 'email']
    ordering = ['apellidos', 'nombres']

@admin.register(Apoderado)
class ApoderadoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'ci', 'parentesco', 'telefono', 'email']
    list_filter = ['parentesco']
    search_fields = ['nombres', 'apellidos', 'ci', 'email']
    ordering = ['apellidos', 'nombres']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['grado', 'asignatura', 'profesor', 'periodo_academico', 'seccion']
    list_filter = ['grado', 'asignatura', 'periodo_academico', 'seccion']
    search_fields = ['grado__nombre', 'asignatura__nombre', 'profesor__nombres', 'profesor__apellidos']
    ordering = ['grado', 'asignatura', 'seccion']

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'fecha_inscripcion', 'activa']
    list_filter = ['activa', 'fecha_inscripcion', 'curso__grado', 'curso__periodo_academico']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos', 'curso__asignatura__nombre']
    ordering = ['curso', 'estudiante']

@admin.register(EstudianteApoderado)
class EstudianteApoderadoAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'apoderado', 'es_principal', 'activa']
    list_filter = ['es_principal', 'activa', 'fecha_asignacion']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos', 'apoderado__nombres', 'apoderado__apellidos']

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['curso', 'nombre', 'tipo', 'fecha', 'ponderacion']
    list_filter = ['tipo', 'fecha', 'curso__grado', 'curso__asignatura']
    search_fields = ['nombre', 'curso__asignatura__nombre', 'curso__grado__nombre']
    ordering = ['curso', 'fecha']

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'evaluacion', 'nota', 'fecha_registro']
    list_filter = ['evaluacion__tipo', 'evaluacion__curso__grado', 'evaluacion__curso__asignatura', 'fecha_registro']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos', 'evaluacion__nombre']
    ordering = ['evaluacion', '-nota']

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'fecha', 'estado']
    list_filter = ['estado', 'fecha', 'curso__grado', 'curso__asignatura']
    search_fields = ['estudiante__nombres', 'estudiante__apellidos', 'curso__asignatura__nombre']
    ordering = ['-fecha', 'curso', 'estudiante']
