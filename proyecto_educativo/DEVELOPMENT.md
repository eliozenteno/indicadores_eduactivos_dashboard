# 🔧 Guía de Desarrollo - Dashboard Indicadores Educativos

## 🚀 Configuración Rápida para Desarrolladores

### 1. Primer Setup (Solo una vez)
```bash
# Clonar repositorio
git clone https://github.com/Cristhianzen/indicadores_eduactivos_dashboard.git
cd indicadores_eduactivos_dashboard

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Navegar al proyecto Django
cd proyecto_educativo

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 2. Desarrollo Diario
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Navegar al proyecto
cd proyecto_educativo

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## 🌐 URLs del Sistema

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Admin Django** | http://127.0.0.1:8000/admin/ | Panel de administración |
| **Página Principal** | http://127.0.0.1:8000/ | Página de inicio |
| **Dashboard** | http://127.0.0.1:8000/dashboard/ | Dashboard principal (en desarrollo) |

## 📊 Datos de Prueba Recomendados

### Orden de Creación (vía Django Admin):

1. **Grados**
   ```
   - Primero A (Primaria)
   - Segundo A (Primaria) 
   - Tercero A (Primaria)
   - Cuarto A (Secundaria)
   ```

2. **Asignaturas**
   ```
   MAT001 - Matemáticas
   LEN002 - Lenguaje
   CIE003 - Ciencias Naturales
   SOC004 - Ciencias Sociales
   ```

3. **Período Académico**
   ```
   2025 - Primer Semestre
   Fecha inicio: 2025-03-01
   Fecha fin: 2025-07-31
   ```

4. **Profesores** (mínimo 4)
5. **Estudiantes** (mínimo 10 por grado)
6. **Cursos** (combinar profesor + asignatura + grado + período)
7. **Inscripciones** (inscribir estudiantes en cursos)
8. **Evaluaciones** (crear pruebas con ponderación)
9. **Calificaciones** (registrar notas)
10. **Asistencia** (registrar presencia/ausencia)

## 🛠️ Comandos de Desarrollo

### Base de Datos
```bash
# Reset completo de BD (¡CUIDADO! Borra todos los datos)
python manage.py flush

# Crear nueva migración después de cambiar models.py
python manage.py makemigrations

# Ver SQL de las migraciones
python manage.py sqlmigrate indicadores 0001

# Ver estado de migraciones
python manage.py showmigrations
```

### Django Shell (Para pruebas rápidas)
```bash
python manage.py shell

# Ejemplo: Contar estudiantes
>>> from indicadores.models import Estudiante
>>> Estudiante.objects.count()

# Ejemplo: Ver estudiantes en riesgo (futuro)
>>> from indicadores.utils import get_estudiantes_en_riesgo
>>> get_estudiantes_en_riesgo()
```

### Tests
```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests específicos
python manage.py test indicadores.tests.TestModels
```

## 📁 Estructura para Nuevas Funcionalidades

```
indicadores/
├── models.py           # ✅ Modelos ya definidos
├── admin.py            # ✅ Admin configurado
├── views.py            # 🔄 Agregar views del dashboard
├── urls.py             # 🆕 Crear URLs de la app
├── dashboard.py        # 🆕 Dashboard Plotly Dash
├── utils.py            # 🆕 Funciones de cálculo KPIs
├── templates/          # 🆕 Templates HTML
│   └── indicadores/
└── static/            # 🆕 CSS, JS, imágenes
    └── indicadores/
```

## 🎯 KPIs a Implementar

### 1. KPI Promedio de Notas por Curso
```python
def calcular_promedio_notas_curso(curso_id):
    # Lógica para calcular promedio
    pass
```

### 2. KPI Tasa de Ausentismo
```python
def calcular_ausentismo_curso(curso_id):
    # Lógica para calcular % ausentismo
    pass
```

### 3. KPI Estudiantes en Riesgo
```python
def get_estudiantes_en_riesgo():
    # Criterios:
    # - Promedio < 4.0
    # - Ausentismo > 15%
    pass
```

## 🔄 Flujo de Git Recomendado

```bash
# 1. Crear nueva rama para funcionalidad
git checkout -b feature/dashboard-kpis

# 2. Hacer cambios y commits frecuentes
git add .
git commit -m "Agregar cálculo de promedio de notas"

# 3. Actualizar rama principal periódicamente
git checkout main
git pull origin main
git checkout feature/dashboard-kpis
git merge main

# 4. Cuando esté listo, crear Pull Request
git push origin feature/dashboard-kpis
```

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'indicadores'"
```bash
# Verificar que estás en el directorio correcto
cd proyecto_educativo
python manage.py runserver
```

### Error: "Port already in use"
```bash
# Usar puerto diferente
python manage.py runserver 8001
```

### Error de migraciones
```bash
# Reset de migraciones (desarrollo)
rm indicadores/migrations/0*.py
python manage.py makemigrations indicadores
python manage.py migrate
```

### Problema con PostgreSQL
```bash
# Cambiar temporalmente a SQLite en settings.py
# Usar la configuración SQLite comentada
```

## 📧 Contacto de Desarrollo

- **Issues**: [GitHub Issues](https://github.com/Cristhianzen/indicadores_eduactivos_dashboard/issues)
- **Discussiones**: [GitHub Discussions](https://github.com/Cristhianzen/indicadores_eduactivos_dashboard/discussions)
- **Email**: cristhianeliozzen@gmail.com

---
**¡Happy Coding! 🚀**