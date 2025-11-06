# 🗄️ Database - Esquemas y Documentación

Este directorio contiene la documentación y esquemas de la base de datos.

## 📋 Archivos

### `schema.sql`
DDL completo para PostgreSQL con toda la estructura de tablas.

### `README.md`
Este archivo con la documentación de la base de datos.

## 🏗️ Estructura de la Base de Datos

La base de datos está normalizada en **Tercera Forma Normal (3NF)** y consta de:

### 1. Dimensiones (6 tablas)
- `Grados` - Niveles educativos
- `Asignaturas` - Materias académicas  
- `Periodos_Academicos` - Períodos escolares
- `Profesores` - Docentes del sistema
- `Estudiantes` - Alumnos matriculados
- `Apoderados` - Tutores y contactos

### 2. Contexto (3 tablas)
- `Cursos` - Une profesor + asignatura + grado + período
- `Inscripciones` - Matrícula de estudiantes en cursos
- `Estudiantes_Apoderados` - Relación estudiante-tutor

### 3. Hechos (3 tablas)
- `Evaluaciones` - Pruebas y tareas con ponderación
- `Calificaciones` - Notas obtenidas por evaluación
- `Asistencia` - Registro diario de presencia

## 🚀 Uso

### Para PostgreSQL:
```bash
# Crear base de datos
createdb indicadores_educativos

# Aplicar schema
psql -d indicadores_educativos -f database/schema.sql
```

### Para SQLite (Desarrollo):
```bash
# Django se encarga automáticamente
python manage.py migrate
```

## 📊 KPIs Soportados

1. **Promedio de Notas por Curso**
2. **Tasa de Ausentismo por Curso** 
3. **Estudiantes en Riesgo Académico**

## 🔧 Mantenimiento

- **Backups regulares** (fuera de Git)
- **Migraciones de Django** para cambios de esquema
- **Fixtures** para datos de prueba