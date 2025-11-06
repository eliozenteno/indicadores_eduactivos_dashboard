# 📊 Esquemas de Base de Datos

Este directorio contiene los esquemas DDL para diferentes bases de datos:

## Archivos Disponibles

### `schema.sql` - PostgreSQL Schema
Esquema completo en PostgreSQL para producción:
- 12 tablas relacionadas en 3NF
- Constraints, índices y relaciones
- Compatible con Django ORM

### Uso

```bash
# Para PostgreSQL
createdb indicadores_educativos
psql -d indicadores_educativos -f database/schema.sql

# Para desarrollo (SQLite)
cd proyecto_educativo
python manage.py migrate
```

## Modelos Incluidos

| Tabla | Descripción |
|-------|-------------|
| `grado` | Niveles académicos (Primaria, Secundaria, etc.) |
| `asignatura` | Materias del currículo |
| `periodo_academico` | Semestres, bimestres, años lectivos |
| `profesor` | Docentes del sistema |
| `estudiante` | Alumnos matriculados |
| `apoderado` | Tutores y representantes |
| `curso` | Clases específicas por período |
| `inscripcion` | Matriculación estudiante-curso |
| `estudiante_apoderado` | Relación tutor-alumno |
| `evaluacion` | Exámenes, tareas, proyectos |
| `calificacion` | Notas obtenidas |
| `asistencia` | Registro de presencia diaria |

## ⚠️ Importante

- **NO subir backups reales** al repositorio
- Usar solo datos ficticios para desarrollo
- Mantener backups de producción externamente