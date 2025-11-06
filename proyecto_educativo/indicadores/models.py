from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Grado(models.Model):
    """Niveles académicos del sistema educativo"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    """Materias o asignaturas del currículo"""
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class PeriodoAcademico(models.Model):
    """Períodos académicos (semestres, bimestres, etc.)"""
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Período Académico"
        verbose_name_plural = "Períodos Académicos"
        ordering = ['-fecha_inicio']
        unique_together = ['nombre', 'fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio} - {self.fecha_fin})"

class Profesor(models.Model):
    """Docentes del sistema educativo"""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ['apellidos', 'nombres']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

class Estudiante(models.Model):
    """Estudiantes del sistema educativo"""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ci = models.CharField(max_length=15, unique=True, verbose_name="Cédula de Identidad")
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['apellidos', 'nombres']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} (CI: {self.ci})"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

class Apoderado(models.Model):
    """Apoderados o tutores de los estudiantes"""
    PARENTESCO_CHOICES = [
        ('padre', 'Padre'),
        ('madre', 'Madre'),
        ('tutor', 'Tutor Legal'),
        ('abuelo', 'Abuelo/a'),
        ('hermano', 'Hermano/a'),
        ('tio', 'Tío/a'),
        ('otro', 'Otro'),
    ]
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ci = models.CharField(max_length=15, unique=True, verbose_name="Cédula de Identidad")
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True)
    parentesco = models.CharField(max_length=10, choices=PARENTESCO_CHOICES, default='padre')
    
    class Meta:
        verbose_name = "Apoderado"
        verbose_name_plural = "Apoderados"
        ordering = ['apellidos', 'nombres']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.get_parentesco_display()})"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

class Curso(models.Model):
    """Cursos específicos por período académico"""
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    periodo_academico = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    seccion = models.CharField(max_length=10, default='A')
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        unique_together = ['grado', 'asignatura', 'periodo_academico', 'seccion']
        ordering = ['grado', 'asignatura', 'seccion']
    
    def __str__(self):
        return f"{self.grado} - {self.asignatura} ({self.seccion}) - {self.profesor.nombre_completo}"

class Inscripcion(models.Model):
    """Inscripciones de estudiantes en cursos"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ['estudiante', 'curso']
        ordering = ['curso', 'estudiante']
    
    def __str__(self):
        return f"{self.estudiante.nombre_completo} - {self.curso}"

class EstudianteApoderado(models.Model):
    """Relación entre estudiantes y sus apoderados"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)
    es_principal = models.BooleanField(default=False)
    fecha_asignacion = models.DateField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Estudiante-Apoderado"
        verbose_name_plural = "Estudiantes-Apoderados"
        unique_together = ['estudiante', 'apoderado']
    
    def __str__(self):
        return f"{self.estudiante.nombre_completo} -> {self.apoderado.nombre_completo}"

class Evaluacion(models.Model):
    """Evaluaciones (exámenes, tareas, proyectos)"""
    TIPO_CHOICES = [
        ('examen', 'Examen'),
        ('tarea', 'Tarea'),
        ('proyecto', 'Proyecto'),
        ('practica', 'Práctica'),
        ('participacion', 'Participación'),
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='examen')
    fecha = models.DateField()
    ponderacion = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
        help_text="Porcentaje sobre la nota final (ej: 25.50 para 25.5%)"
    )
    
    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['curso', 'fecha']
    
    def __str__(self):
        return f"{self.curso} - {self.nombre} ({self.get_tipo_display()})"

class Calificacion(models.Model):
    """Calificaciones obtenidas por estudiantes en evaluaciones"""
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        help_text="Nota de 0 a 100"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        unique_together = ['evaluacion', 'estudiante']
        ordering = ['evaluacion', '-nota']
    
    def __str__(self):
        return f"{self.estudiante.nombre_completo} - {self.evaluacion.nombre}: {self.nota}"

class Asistencia(models.Model):
    """Registro diario de asistencia"""
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tardanza', 'Tardanza'),
        ('justificada', 'Ausencia Justificada'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='presente')
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        unique_together = ['estudiante', 'curso', 'fecha']
        ordering = ['-fecha', 'curso', 'estudiante']
    
    def __str__(self):
        return f"{self.estudiante.nombre_completo} - {self.curso} ({self.fecha}): {self.get_estado_display()}"
