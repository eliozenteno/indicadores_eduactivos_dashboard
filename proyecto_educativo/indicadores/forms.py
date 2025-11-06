"""
Formularios Django para el sistema de Indicadores Educativos
============================================================
Formularios para registro y edición de datos del sistema
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Grado, Asignatura, PeriodoAcademico, Profesor, Estudiante, 
    Apoderado, Curso, Inscripcion, EstudianteApoderado, 
    Evaluacion, Calificacion, Asistencia
)


class EstudianteForm(forms.ModelForm):
    """Formulario para crear/editar estudiantes"""
    
    class Meta:
        model = Estudiante
        fields = [
            'nombres', 'apellidos', 'ci', 'email', 'telefono', 
            'fecha_nacimiento', 'direccion', 'activo'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombres del estudiante'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellidos del estudiante'
            }),
            'ci': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cédula de Identidad'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ProfesorForm(forms.ModelForm):
    """Formulario para crear/editar profesores"""
    
    class Meta:
        model = Profesor
        fields = ['nombres', 'apellidos', 'email', 'telefono', 'especialidad', 'activo']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del profesor'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del profesor'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especialidad o área'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CursoForm(forms.ModelForm):
    """Formulario para crear/editar cursos"""
    
    class Meta:
        model = Curso
        fields = ['grado', 'asignatura', 'profesor', 'periodo_academico', 'seccion']
        widgets = {
            'grado': forms.Select(attrs={'class': 'form-select'}),
            'asignatura': forms.Select(attrs={'class': 'form-select'}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
            'periodo_academico': forms.Select(attrs={'class': 'form-select'}),
            'seccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: A, B, C'
            }),
        }


class InscripcionForm(forms.ModelForm):
    """Formulario para inscribir estudiantes en cursos"""
    
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'curso', 'activa']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get('estudiante')
        curso = cleaned_data.get('curso')
        
        # Verificar que el estudiante no esté ya inscrito en este curso
        if estudiante and curso:
            existe = Inscripcion.objects.filter(
                estudiante=estudiante, 
                curso=curso
            ).exclude(pk=self.instance.pk if self.instance.pk else None).exists()
            
            if existe:
                raise ValidationError(
                    f'{estudiante.nombre_completo} ya está inscrito en {curso}'
                )
        
        return cleaned_data


class EvaluacionForm(forms.ModelForm):
    """Formulario para crear/editar evaluaciones"""
    
    class Meta:
        model = Evaluacion
        fields = ['curso', 'nombre', 'descripcion', 'tipo', 'fecha', 'ponderacion']
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la evaluación'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción (opcional)'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ponderacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Porcentaje (0-100)',
                'step': '0.01',
                'min': '0.01',
                'max': '100'
            }),
        }


class CalificacionForm(forms.ModelForm):
    """Formulario para registrar calificaciones"""
    
    class Meta:
        model = Calificacion
        fields = ['evaluacion', 'estudiante', 'nota', 'observaciones']
        widgets = {
            'evaluacion': forms.Select(attrs={'class': 'form-select'}),
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nota (0-100)',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si ya se seleccionó una evaluación, filtrar solo estudiantes inscritos en ese curso
        if 'evaluacion' in self.data:
            try:
                evaluacion_id = int(self.data.get('evaluacion'))
                evaluacion = Evaluacion.objects.get(id=evaluacion_id)
                self.fields['estudiante'].queryset = Estudiante.objects.filter(
                    inscripcion__curso=evaluacion.curso,
                    inscripcion__activa=True
                ).distinct()
            except (ValueError, TypeError, Evaluacion.DoesNotExist):
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        evaluacion = cleaned_data.get('evaluacion')
        estudiante = cleaned_data.get('estudiante')
        
        # Verificar que el estudiante esté inscrito en el curso de la evaluación
        if evaluacion and estudiante:
            inscrito = Inscripcion.objects.filter(
                estudiante=estudiante,
                curso=evaluacion.curso,
                activa=True
            ).exists()
            
            if not inscrito:
                raise ValidationError(
                    f'{estudiante.nombre_completo} no está inscrito en el curso {evaluacion.curso}'
                )
            
            # Verificar que no exista ya una calificación para esta evaluación y estudiante
            existe = Calificacion.objects.filter(
                evaluacion=evaluacion,
                estudiante=estudiante
            ).exclude(pk=self.instance.pk if self.instance.pk else None).exists()
            
            if existe:
                raise ValidationError(
                    f'{estudiante.nombre_completo} ya tiene una calificación registrada para {evaluacion.nombre}'
                )
        
        return cleaned_data


class AsistenciaForm(forms.ModelForm):
    """Formulario para registrar asistencia"""
    
    class Meta:
        model = Asistencia
        fields = ['estudiante', 'curso', 'fecha', 'estado', 'observaciones']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si ya se seleccionó un curso, filtrar solo estudiantes inscritos
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['estudiante'].queryset = Estudiante.objects.filter(
                    inscripcion__curso_id=curso_id,
                    inscripcion__activa=True
                ).distinct()
            except (ValueError, TypeError):
                pass


class AsistenciaMasivaForm(forms.Form):
    """Formulario para registrar asistencia de múltiples estudiantes a la vez"""
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Curso'
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha'
    )
    
    def __init__(self, *args, **kwargs):
        curso = kwargs.pop('curso', None)
        super().__init__(*args, **kwargs)
        
        if curso:
            # Obtener estudiantes inscritos en el curso
            estudiantes = Estudiante.objects.filter(
                inscripcion__curso=curso,
                inscripcion__activa=True
            ).distinct().order_by('apellidos', 'nombres')
            
            # Crear un campo de selección por cada estudiante
            for estudiante in estudiantes:
                field_name = f'estudiante_{estudiante.id}'
                self.fields[field_name] = forms.ChoiceField(
                    choices=Asistencia.ESTADO_CHOICES,
                    initial='presente',
                    widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
                    label=estudiante.nombre_completo
                )


# ============================================
# NUEVOS FORMULARIOS FALTANTES
# ============================================

class ApoderadoForm(forms.ModelForm):
    """Formulario para crear/editar apoderados"""
    
    class Meta:
        model = Apoderado
        fields = ['nombres', 'apellidos', 'ci', 'parentesco', 'telefono', 'email', 'direccion']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del apoderado'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del apoderado'
            }),
            'ci': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cédula de Identidad'
            }),
            'parentesco': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa'
            }),
        }
    
    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        if Apoderado.objects.filter(ci=ci).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un apoderado con este CI.')
        return ci


class EstudianteApoderadoForm(forms.ModelForm):
    """Formulario para vincular estudiante con apoderado"""
    
    class Meta:
        model = EstudianteApoderado
        fields = ['estudiante', 'apoderado', 'es_principal', 'activa']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'apoderado': forms.Select(attrs={'class': 'form-select'}),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get('estudiante')
        apoderado = cleaned_data.get('apoderado')
        
        # Verificar que no exista ya este vínculo
        if estudiante and apoderado:
            if EstudianteApoderado.objects.filter(
                estudiante=estudiante,
                apoderado=apoderado,
                activa=True
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este estudiante ya está vinculado con este apoderado.')
        
        return cleaned_data

