from indicadores.models import *

# Crear o recuperar elementos base
g, _ = Grado.objects.get_or_create(nombre='1° Primaria', defaults={'descripcion':'Primer grado'})
a, _ = Asignatura.objects.get_or_create(codigo='MAT', defaults={'nombre':'Matemáticas','descripcion':'Matemáticas básicas'})
p, _ = PeriodoAcademico.objects.get_or_create(nombre='2025', defaults={'fecha_inicio':'2025-02-01','fecha_fin':'2025-06-30','activo':True})
prof, _ = Profesor.objects.get_or_create(email='prof@test.local', defaults={'nombres':'Juan','apellidos':'Perez','telefono':'','especialidad':'Matemáticas'})
curso, _ = Curso.objects.get_or_create(grado=g, asignatura=a, profesor=prof, periodo_academico=p, seccion='A')
est, _ = Estudiante.objects.get_or_create(ci='123456', defaults={'nombres':'Alumno','apellidos':'Uno','email':'alumno1@test.local','fecha_nacimiento':'2010-05-05'})
ins, _ = Inscripcion.objects.get_or_create(estudiante=est, curso=curso)

# Crear evaluación y calificación
ev, created_ev = Evaluacion.objects.get_or_create(curso=curso, nombre='Parcial 1', fecha='2025-03-01', defaults={'ponderacion':'30.00','tipo':'examen'})
cal = Calificacion.objects.create(evaluacion=ev, estudiante=est, nota=85.5)

print('CREATED: Grado', g.id, 'Asignatura', a.id, 'Profesor', prof.id, 'Estudiante', est.id, 'Curso', curso.id, 'Evaluacion', ev.id, 'Calificacion', cal.id)
print('COUNTS:', 'Grado', Grado.objects.count(), 'Asignatura', Asignatura.objects.count(), 'Estudiante', Estudiante.objects.count(), 'Curso', Curso.objects.count(), 'Evaluacion', Evaluacion.objects.count(), 'Calificacion', Calificacion.objects.count())

# Update
cal.nota = 90.0
cal.save()
print('UPDATED cal id', cal.id, 'nota', Calificacion.objects.get(pk=cal.id).nota)

# Delete (cleanup)
Calificacion.objects.filter(pk=cal.id).delete()
print('DELETED cal id', cal.id, 'now Calificacion count', Calificacion.objects.count())

# Additional read: listar estudiantes activos
print('LIST ACTIVE STUDENTS:')
for s in Estudiante.objects.filter(activo=True)[:5]:
    print('-', s.id, s.nombre_completo, s.ci)

# Finished
print('CRUD test finished')
