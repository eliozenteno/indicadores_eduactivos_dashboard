# 📊 Dashboard de Indicadores Educativos

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://djangoproject.com/)
[![Plotly](https://img.shields.io/badge/Plotly-Dash-orange.svg)](https://plotly.com/dash/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema de Dashboard para la **Detección Temprana de Riesgo Académico** desarrollado con Django 5, PostgreSQL/SQLite y Plotly Dash. Automatiza el análisis de métricas de rendimiento y asistencia para identificar estudiantes en riesgo académico.

## 🎯 Objetivo del Proyecto

Crear un sistema integral que permita:
- **Monitoreo en tiempo real** de indicadores educativos clave
- **Identificación automática** de estudiantes en riesgo académico
- **Visualización interactiva** de métricas de rendimiento y asistencia
- **Gestión eficiente** de datos académicos a través del panel de administración

## 🏗️ Arquitectura del Sistema

```
Dashboard de Indicadores Educativos
├── Backend (Django 5 MVC)
│   ├── Models (ORM) → Base de Datos
│   ├── Views → Lógica de Negocio
│   └── Admin → Gestión de Datos
├── Frontend (Plotly Dash)
│   ├── Gráficos Interactivos
│   ├── KPIs en Tiempo Real
│   └── Dashboard Responsivo
└── Base de Datos (PostgreSQL/SQLite)
    ├── Dimensiones (Maestros)
    ├── Contexto (Relaciones)
    └── Hechos (Transacciones)
```

## 🗄️ Modelo de Datos (3NF)

### 📋 Dimensiones (Tablas Maestras)
- **Grados**: Niveles educativos y grados
- **Asignaturas**: Materias con códigos únicos
- **Períodos Académicos**: Años y períodos escolares
- **Profesores**: Docentes con especialidades
- **Estudiantes**: Alumnos con datos personales
- **Apoderados**: Tutores y contactos

### 🔗 Contexto (Tablas de Unión)
- **Cursos**: Une Profesor + Asignatura + Grado + Período
- **Inscripciones**: Une Estudiante + Curso
- **Estudiantes-Apoderados**: Relaciones familiares

### 📊 Hechos (Tablas Transaccionales)
- **Evaluaciones**: Pruebas y tareas con ponderación
- **Calificaciones**: Notas obtenidas por evaluación
- **Asistencia**: Registro diario de presencia

## 📈 KPIs Implementados

### 1. **Promedio de Notas por Curso**
Cálculo automático del rendimiento académico promedio por curso.

### 2. **Tasa de Ausentismo por Curso**
Porcentaje de días ausentes sobre el total registrado.

### 3. **Estudiantes en Riesgo Académico** 🚨
Identificación automática basada en:
- Promedio de notas < 4.0
- Ausentismo > 15%

## 🚀 Instalación y Configuración

### Prerrequisitos
- **Python 3.11+**
- **PostgreSQL** (opcional, puede usar SQLite para desarrollo)
- **Git**

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Cristhianzen/indicadores_eduactivos_dashboard.git
cd indicadores_eduactivos_dashboard
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt

# O instalar manualmente:
pip install django==5.2.8 psycopg2-binary plotly dash pandas
```

### 4. Configurar Base de Datos

#### Opción A: SQLite (Desarrollo)
```python
# settings.py (ya configurado)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Opción B: PostgreSQL (Producción)
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'indicadores_educativos',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplicar Migraciones
```bash
cd proyecto_educativo
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 7. Ejecutar el Servidor
```bash
python manage.py runserver
```

## 🖥️ Acceso al Sistema

- **Django Admin**: http://127.0.0.1:8000/admin/
- **Dashboard** (en desarrollo): http://127.0.0.1:8000/dashboard/
- **API Rest** (futuro): http://127.0.0.1:8000/api/

## 📁 Estructura del Proyecto

```
proyecto_educativo/
├── manage.py                    # Script de gestión Django
├── db.sqlite3                   # Base de datos SQLite
├── requirements.txt             # Dependencias del proyecto
├── 
├── proyecto_educativo/          # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py              # Configuración principal
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # Configuración WSGI
│   └── asgi.py                  # Configuración ASGI
│
└── indicadores/                 # App principal
    ├── __init__.py
    ├── admin.py                 # Configuración Django Admin
    ├── apps.py                  # Configuración de la app
    ├── models.py                # Modelos de datos (ORM)
    ├── views.py                 # Lógica de vistas
    ├── tests.py                 # Tests unitarios
    ├── dashboard.py             # Dashboard Plotly Dash (futuro)
    └── migrations/              # Migraciones de BD
        └── 0001_initial.py
```

## 🔧 Comandos Útiles

### Gestión de Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder a shell de Django
python manage.py shell

# Acceder a shell de BD
python manage.py dbshell
```

### Desarrollo
```bash
# Ejecutar tests
python manage.py test

# Verificar configuración
python manage.py check

# Recopilar archivos estáticos
python manage.py collectstatic
```

### Verificación del Sistema
```bash
# Verificar tablas creadas
python check_tables.py

# Verificación completa de BD
python verify_database.py
```

## 👥 Gestión de Datos

### Django Admin
El sistema incluye un panel de administración completo para gestionar:

1. **Datos Maestros**: Grados, Asignaturas, Profesores, Estudiantes
2. **Configuración Académica**: Períodos, Cursos, Inscripciones
3. **Datos Operacionales**: Evaluaciones, Calificaciones, Asistencia

### Flujo de Datos Recomendado
1. **Configurar** Grados y Asignaturas
2. **Crear** Período Académico actual
3. **Registrar** Profesores y Estudiantes
4. **Definir** Cursos (Profesor + Asignatura + Grado + Período)
5. **Inscribir** Estudiantes en Cursos
6. **Registrar** Evaluaciones, Calificaciones y Asistencia

## 🚧 Estado del Proyecto

### ✅ Completado
- [x] Configuración base de Django
- [x] Modelos de datos (12 tablas)
- [x] Migraciones de base de datos
- [x] Django Admin configurado
- [x] Sistema de autenticación
- [x] Estructura de proyecto organizada

### 🔄 En Desarrollo
- [ ] Dashboard Plotly Dash
- [ ] Funciones de cálculo de KPIs
- [ ] API REST para datos
- [ ] Sistema de notificaciones
- [ ] Reportes en PDF

### 📋 Próximos Pasos
1. Implementar funciones de cálculo de KPIs
2. Crear dashboard interactivo con Plotly Dash
3. Integrar dashboard con Django
4. Desarrollar sistema de alertas
5. Implementar tests unitarios
6. Despliegue en producción

## 🤝 Contribución

### Flujo de Trabajo
1. **Fork** del repositorio
2. **Crear** rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

### Estándares de Código
- **PEP 8** para Python
- **Documentación** de funciones y clases
- **Tests unitarios** para nueva funcionalidad
- **Commits descriptivos** en español

## 📞 Soporte

### Desarrollador Principal
- **Nombre**: Cristhian Zenteno
- **GitHub**: [@Cristhianzen](https://github.com/Cristhianzen)
- **Email**: cristhianeliozzen@gmail.com

### Reportar Problemas
1. Verificar que el problema no esté reportado
2. Crear **Issue** detallado en GitHub
3. Incluir pasos para reproducir el error
4. Agregar capturas de pantalla si es necesario

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Universidad Autónoma Juan Misael Saracho (UAJMS)**
- **Carrera de Ingeniería de Sistemas**
- **Materia**: SOF522 - Optativa IV - Automatización de Procesos de Negocio
- **Docente**: [Nombre del Docente]

---

**📊 Dashboard de Indicadores Educativos - Detectando el futuro académico hoy** ✨