"""
Management command para generar datos de prueba
================================================
Crea datos ficticios pero realistas para poblar el sistema
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from indicadores.models import (
    Grado, Asignatura, PeriodoAcademico, Profesor, Estudiante,
    Apoderado, Curso, Inscripcion, EstudianteApoderado,
    Evaluacion, Calificacion, Asistencia
)


class Command(BaseCommand):
    help = 'Genera datos de prueba para el sistema de indicadores educativos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos antes de generar nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando datos existentes...')
            Asistencia.objects.all().delete()
            Calificacion.objects.all().delete()
            Evaluacion.objects.all().delete()
            EstudianteApoderado.objects.all().delete()
            Inscripcion.objects.all().delete()
            Curso.objects.all().delete()
            Apoderado.objects.all().delete()
            Estudiante.objects.all().delete()
            Profesor.objects.all().delete()
            PeriodoAcademico.objects.all().delete()
            Asignatura.objects.all().delete()
            Grado.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Datos eliminados'))

        self.stdout.write('Generando datos de prueba...\n')

        # 1. Grados
        self.stdout.write('Creando grados...')
        grados_data = [
            ('1° Primaria', 'Primer año de primaria'),
            ('2° Primaria', 'Segundo año de primaria'),
            ('3° Primaria', 'Tercer año de primaria'),
            ('4° Primaria', 'Cuarto año de primaria'),
            ('5° Primaria', 'Quinto año de primaria'),
            ('6° Primaria', 'Sexto año de primaria'),
        ]
        grados = []
        for nombre, desc in grados_data:
            grado, _ = Grado.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
            grados.append(grado)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(grados)} grados creados'))

        # 2. Asignaturas
        self.stdout.write('Creando asignaturas...')
        asignaturas_data = [
            ('MAT', 'Matemáticas', 'Cálculo y álgebra básica'),
            ('LEN', 'Lenguaje', 'Lectura y escritura'),
            ('CIE', 'Ciencias Naturales', 'Biología, física y química'),
            ('SOC', 'Ciencias Sociales', 'Historia y geografía'),
            ('EDF', 'Educación Física', 'Deportes y actividad física'),
            ('ART', 'Artes', 'Música y artes plásticas'),
            ('ING', 'Inglés', 'Idioma extranjero'),
        ]
        asignaturas = []
        for codigo, nombre, desc in asignaturas_data:
            asig, _ = Asignatura.objects.get_or_create(
                codigo=codigo, 
                defaults={'nombre': nombre, 'descripcion': desc}
            )
            asignaturas.append(asig)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(asignaturas)} asignaturas creadas'))

        # 3. Periodo Académico
        self.stdout.write('Creando periodo académico...')
        periodo, _ = PeriodoAcademico.objects.get_or_create(
            nombre='Primer Semestre 2025',
            defaults={
                'fecha_inicio': date(2025, 2, 1),
                'fecha_fin': date(2025, 7, 31),
                'activo': True
            }
        )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Periodo académico creado: {periodo}'))

        # 4. Profesores
        self.stdout.write('Creando profesores...')
        profesores_data = [
            ('Juan', 'Pérez García', 'juan.perez@colegio.edu', '77123456', 'Matemáticas'),
            ('María', 'López Silva', 'maria.lopez@colegio.edu', '77234567', 'Lenguaje'),
            ('Carlos', 'González Rojas', 'carlos.gonzalez@colegio.edu', '77345678', 'Ciencias'),
            ('Ana', 'Martínez Vega', 'ana.martinez@colegio.edu', '77456789', 'Sociales'),
            ('Pedro', 'Sánchez Torres', 'pedro.sanchez@colegio.edu', '77567890', 'Educación Física'),
            ('Laura', 'Fernández Cruz', 'laura.fernandez@colegio.edu', '77678901', 'Artes'),
            ('Diego', 'Rodríguez Ortiz', 'diego.rodriguez@colegio.edu', '77789012', 'Inglés'),
        ]
        profesores = []
        for nombres, apellidos, email, tel, esp in profesores_data:
            prof, _ = Profesor.objects.get_or_create(
                email=email,
                defaults={
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'telefono': tel,
                    'especialidad': esp,
                    'activo': True
                }
            )
            profesores.append(prof)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(profesores)} profesores creados'))

        # 5. Estudiantes
        self.stdout.write('Creando estudiantes...')
        nombres_masculinos = ['Juan', 'Carlos', 'Pedro', 'Luis', 'Miguel', 'José', 'Diego', 'Andrés', 'Daniel', 'Fernando']
        nombres_femeninos = ['María', 'Ana', 'Laura', 'Carmen', 'Isabel', 'Patricia', 'Sandra', 'Lucía', 'Elena', 'Rosa']
        apellidos = ['García', 'López', 'Martínez', 'González', 'Rodríguez', 'Fernández', 'Pérez', 'Sánchez', 'Torres', 'Ramírez', 'Flores', 'Vega', 'Silva', 'Cruz', 'Ortiz']
        
        estudiantes = []
        ci_counter = 10000000
        for i in range(30):  # 30 estudiantes
            nombres_list = nombres_masculinos if i % 2 == 0 else nombres_femeninos
            nombre = random.choice(nombres_list)
            apellido1 = random.choice(apellidos)
            apellido2 = random.choice(apellidos)
            
            edad = random.randint(6, 12)
            fecha_nac = date.today() - timedelta(days=365 * edad + random.randint(0, 365))
            
            est, _ = Estudiante.objects.get_or_create(
                ci=str(ci_counter + i),
                defaults={
                    'nombres': nombre,
                    'apellidos': f'{apellido1} {apellido2}',
                    'email': f'{nombre.lower()}.{apellido1.lower()}@estudiante.edu',
                    'telefono': f'7{random.randint(1000000, 9999999)}',
                    'fecha_nacimiento': fecha_nac,
                    'direccion': f'Calle {random.choice(["Los Pinos", "Las Rosas", "El Sol", "La Luna"])} #{random.randint(100, 999)}',
                    'activo': True
                }
            )
            estudiantes.append(est)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(estudiantes)} estudiantes creados'))

        # 6. Cursos (cada asignatura para cada grado)
        self.stdout.write('Creando cursos...')
        cursos = []
        for grado in grados:
            for asignatura in asignaturas:
                profesor = random.choice(profesores)
                curso, _ = Curso.objects.get_or_create(
                    grado=grado,
                    asignatura=asignatura,
                    periodo_academico=periodo,
                    seccion='A',
                    defaults={'profesor': profesor}
                )
                cursos.append(curso)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(cursos)} cursos creados'))

        # 7. Inscripciones (asignar estudiantes a cursos)
        self.stdout.write('Creando inscripciones...')
        inscripciones_count = 0
        estudiantes_por_grado = {}
        for grado in grados:
            estudiantes_grado = random.sample(estudiantes, min(5, len(estudiantes)))
            estudiantes_por_grado[grado] = estudiantes_grado
            
            cursos_grado = [c for c in cursos if c.grado == grado]
            for estudiante in estudiantes_grado:
                for curso in cursos_grado:
                    Inscripcion.objects.get_or_create(
                        estudiante=estudiante,
                        curso=curso,
                        defaults={'activa': True}
                    )
                    inscripciones_count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {inscripciones_count} inscripciones creadas'))

        # 8. Evaluaciones
        self.stdout.write('Creando evaluaciones...')
        tipos_eval = ['examen', 'tarea', 'proyecto', 'practica']
        evaluaciones = []
        for curso in cursos:
            # Crear 3 evaluaciones por curso
            for j in range(3):
                tipo = random.choice(tipos_eval)
                nombre = f'{tipo.capitalize()} {j+1}'
                fecha_eval = periodo.fecha_inicio + timedelta(days=30 * j + random.randint(0, 20))
                
                eval_obj, _ = Evaluacion.objects.get_or_create(
                    curso=curso,
                    nombre=nombre,
                    defaults={
                        'descripcion': f'Evaluación de {curso.asignatura.nombre}',
                        'tipo': tipo,
                        'fecha': fecha_eval,
                        'ponderacion': Decimal('33.33')
                    }
                )
                evaluaciones.append(eval_obj)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(evaluaciones)} evaluaciones creadas'))

        # 9. Calificaciones
        self.stdout.write('Creando calificaciones...')
        calificaciones_count = 0
        for evaluacion in evaluaciones:
            # Obtener estudiantes inscritos en el curso
            estudiantes_curso = Estudiante.objects.filter(
                inscripcion__curso=evaluacion.curso,
                inscripcion__activa=True
            )
            
            for estudiante in estudiantes_curso:
                # Generar nota realista (con distribución normal alrededor de 70)
                nota_base = random.gauss(70, 15)
                nota = max(0, min(100, round(nota_base, 2)))
                
                Calificacion.objects.get_or_create(
                    evaluacion=evaluacion,
                    estudiante=estudiante,
                    defaults={
                        'nota': Decimal(str(nota)),
                        'observaciones': '' if nota >= 51 else 'Requiere apoyo adicional'
                    }
                )
                calificaciones_count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {calificaciones_count} calificaciones creadas'))

        # 10. Asistencia (últimos 30 días)
        self.stdout.write('Creando registros de asistencia...')
        asistencia_count = 0
        estados = ['presente', 'presente', 'presente', 'presente', 'ausente', 'tardanza', 'justificada']
        
        for i in range(30):  # Últimos 30 días
            fecha_asist = date.today() - timedelta(days=i)
            
            # Solo días hábiles
            if fecha_asist.weekday() < 5:  # Lunes=0, Viernes=4
                for curso in random.sample(cursos, min(10, len(cursos))):
                    estudiantes_curso = Estudiante.objects.filter(
                        inscripcion__curso=curso,
                        inscripcion__activa=True
                    )
                    
                    for estudiante in estudiantes_curso:
                        estado = random.choice(estados)
                        Asistencia.objects.get_or_create(
                            estudiante=estudiante,
                            curso=curso,
                            fecha=fecha_asist,
                            defaults={'estado': estado}
                        )
                        asistencia_count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {asistencia_count} registros de asistencia creados'))

        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('DATOS DE PRUEBA GENERADOS EXITOSAMENTE'))
        self.stdout.write('='*50)
        self.stdout.write(f'  Grados: {Grado.objects.count()}')
        self.stdout.write(f'  Asignaturas: {Asignatura.objects.count()}')
        self.stdout.write(f'  Profesores: {Profesor.objects.count()}')
        self.stdout.write(f'  Estudiantes: {Estudiante.objects.count()}')
        self.stdout.write(f'  Cursos: {Curso.objects.count()}')
        self.stdout.write(f'  Inscripciones: {Inscripcion.objects.count()}')
        self.stdout.write(f'  Evaluaciones: {Evaluacion.objects.count()}')
        self.stdout.write(f'  Calificaciones: {Calificacion.objects.count()}')
        self.stdout.write(f'  Asistencias: {Asistencia.objects.count()}')
        self.stdout.write('='*50 + '\n')
        self.stdout.write(self.style.SUCCESS('✓ Ahora puedes acceder al sistema en http://127.0.0.1:8000/'))
