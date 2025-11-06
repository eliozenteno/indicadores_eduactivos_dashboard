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

## 📈 Desarrollo por Fases

### ✅ Fase 1 - Fundación (COMPLETADO)
- **Modelo de datos completo**: 12 tablas relacionadas en 3NF
- **Interfaz de administración**: Django Admin completamente funcional
- **Base de datos**: Esquemas para SQLite (desarrollo) y PostgreSQL (producción)
- **Migración inicial**: Todas las tablas creadas y validadas

### ✅ Fase 2 - Dashboard Interactivo (COMPLETADO)

**🎉 Sistema completamente funcional: http://127.0.0.1:8000/**

#### ✅ KPIs Implementados:

1. **📊 Promedio de Notas por Curso**
   - ✅ Gráfico de barras interactivo con Chart.js
   - ✅ Top 10 cursos por rendimiento
   - ✅ Actualización automática desde BD

2. **📈 Distribución de Asistencia**
   - ✅ Gráfico circular (dona) con 4 estados
   - ✅ Estados: Presente/Ausente/Tardanza/Justificada
   - ✅ Porcentajes calculados en tiempo real

3. **🚨 Estudiantes en Riesgo Académico**
   - ✅ **Algoritmo implementado**: promedio < 51 puntos
   - ✅ **Tabla dedicada** en dashboard
   - ✅ **Badges de alerta** visuales

4. **📈 Estadísticas Generales**
   - ✅ Total estudiantes activos
   - ✅ Total profesores activos
   - ✅ Cursos vigentes
   - ✅ Promedio general del sistema

5. **📝 Registros Recientes**
   - ✅ Últimas 5 calificaciones
   - ✅ Vista completa con detalles

#### ✅ Formularios de Registro:

1. **👨‍🎓 Gestión de Estudiantes** - Lista, búsqueda, modal de creación
2. **📝 Registro de Calificaciones** - Form con validaciones y help sidebar
3. **📅 Registro de Asistencia** - 4 estados + resumen del día

#### ✅ API REST (12 endpoints CRUD + 4 KPIs):

- `/api/grados/`, `/api/asignaturas/`, `/api/periodos-academicos/`
- `/api/profesores/`, `/api/estudiantes/`, `/api/apoderados/`
- `/api/cursos/`, `/api/inscripciones/`, `/api/evaluaciones/`
- `/api/calificaciones/`, `/api/asistencia/`
- `/api/dashboard/kpis_generales/`
- `/api/dashboard/estudiantes_riesgo/`
- `/api/dashboard/promedio_por_curso/`

#### 🗄️ Datos de Prueba: 2,106 registros
- 30 Estudiantes | 7 Profesores | 42 Cursos
- **630 Calificaciones** | **1,100 Asistencias**

### 🔮 Fase 3 - Análisis Predictivo (FUTURO)
- Predicción de abandono escolar usando ML
- Recomendaciones automáticas de intervención
- Integración con sistemas de notificación (SMS/Email)

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

#### Opción A: SQLite (Desarrollo - Recomendado)
```bash
# Ya está configurado por defecto
# No requiere instalación adicional
cd proyecto_educativo
python manage.py migrate
```

#### Opción B: PostgreSQL (Producción)

**Paso 1: Crear la base de datos**
```bash
# Crear base de datos PostgreSQL
createdb indicadores_educativos

# Aplicar el schema incluido en el proyecto
psql -d indicadores_educativos -f database/schema.sql
```

**Paso 2: Configurar Django**
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

**Paso 3: Sincronizar migraciones**
```bash
cd proyecto_educativo
python manage.py migrate --fake-initial
```

### 5. Aplicar Migraciones
```bash
cd proyecto_educativo
python manage.py makemigrations
python manage.py migrate
```

### 6. Generar Datos de Prueba
```bash
python manage.py generar_datos --reset
```

### 7. Crear Superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 8. Ejecutar el Servidor
```bash
python manage.py runserver
```

## 🖥️ Acceso al Sistema

**✅ Sistema completamente funcional en http://127.0.0.1:8000/**

### Enlaces Principales:
- **Dashboard Principal**: http://127.0.0.1:8000/ (KPIs + gráficos)
- **Lista de Estudiantes**: http://127.0.0.1:8000/estudiantes/
- **Registrar Calificación**: http://127.0.0.1:8000/registrar-calificacion/
- **Registrar Asistencia**: http://127.0.0.1:8000/registrar-asistencia/
- **API REST (Browsable)**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/ (requiere superuser)

## 🗄️ Gestión de Base de Datos

### Schema de PostgreSQL
El proyecto incluye un DDL completo en `database/schema.sql` que puedes usar para:

```bash
# Crear base de datos desde cero
createdb indicadores_educativos
psql -d indicadores_educativos -f database/schema.sql
```

### Datos de Prueba
Para desarrollo, usa los datos ficticios incluidos:

```bash
# Cargar datos de muestra (cuando estén disponibles)
python manage.py loaddata fixtures/sample_data.json
```

### Migración entre Bases de Datos
```bash
# De SQLite a PostgreSQL
python manage.py dumpdata --format=json > data_backup.json
# Cambiar configuración a PostgreSQL
python manage.py migrate
python manage.py loaddata data_backup.json
```

### ⚠️ Importante sobre Backups
- **NO incluir** backups reales de base de datos en Git
- Usar solo datos ficticios para desarrollo
- Mantener backups de producción fuera del repositorio

## 🎯 Próximos Pasos

### Inmediatos (Fase 2)
1. **Crear datos de prueba**: Poblar la base de datos con datos ficticios para testing
2. **Implementar views**: Crear vistas Django para los KPIs principales
3. **Dashboard base**: Configurar Plotly Dash para visualizaciones interactivas
4. **Cálculos KPI**: Implementar funciones de cálculo de métricas

### Comandos sugeridos para continuar:
```bash
# Crear un superusuario para acceder al admin
python manage.py createsuperuser

# Generar datos de prueba (próximo desarrollo)
python manage.py populate_test_data

# Iniciar desarrollo del dashboard
python manage.py startapp dashboard
```

## 📁 Estructura del Proyecto

```
indicadores_eduactivos_dashboard/
├── README.md                    # Documentación principal
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos a excluir de Git
├── DEVELOPMENT.md               # Guía para desarrolladores
├── 
├── database/                    # 🗄️ Esquemas y documentación de BD
│   ├── schema.sql               # DDL completo para PostgreSQL
│   └── README.md                # Documentación de la BD
│
├── proyecto_educativo/          # 🚀 Proyecto Django principal
│   ├── manage.py                # Script de gestión Django
│   ├── db.sqlite3               # Base de datos SQLite (desarrollo)
│   │
│   ├── fixtures/                # 📊 Datos de prueba
│   │   └── README.md            # Instrucciones para fixtures
│   │
│   ├── sample_data/             # 🧪 Scripts para generar datos
│   │   └── README.md            # Guía para datos de muestra
│   │
│   ├── proyecto_educativo/      # ⚙️ Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuración principal
│   │   ├── urls.py              # URLs principales
│   │   ├── wsgi.py              # Configuración WSGI
│   │   └── asgi.py              # Configuración ASGI
│   │
│   └── indicadores/             # 📈 App principal del dashboard
│       ├── __init__.py
│       ├── admin.py             # Configuración Django Admin
│       ├── apps.py              # Configuración de la app
│       ├── models.py            # Modelos de datos (ORM)
│       ├── views.py             # Lógica de vistas
│       ├── tests.py             # Tests unitarios
│       ├── dashboard.py         # Dashboard Plotly Dash (futuro)
│       └── migrations/          # Migraciones de BD
│           └── 0001_initial.py
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

## ✅ Estado del Proyecto

### ✅ Completado (Fase 1 y Fase 2)
- [x] Configuración base de Django 5.2.8
- [x] Modelos de datos completos (12 tablas en 3NF)
- [x] Migraciones de base de datos
- [x] Django Admin completamente configurado
- [x] Sistema de autenticación
- [x] Estructura de proyecto organizada
- [x] **API REST completa con Django REST Framework** (12 endpoints CRUD + 4 KPIs)
- [x] **Dashboard interactivo con Chart.js** (gráficos de barras y dona)
- [x] **Formularios de registro** (Estudiantes, Calificaciones, Asistencia)
- [x] **Sistema de detección de riesgo académico** (promedio < 51)
- [x] **Templates HTML responsive** con Bootstrap 5
- [x] **Datos de prueba generados** (2,106 registros)
- [x] **KPIs en tiempo real** (4 stat cards + 2 gráficos)
- [x] **Management command** para generar datos (`python manage.py generar_datos`)

### 🔄 Posibles Mejoras Futuras
- [ ] Dashboard Plotly Dash (gráficos interactivos avanzados)
- [ ] Sistema de autenticación por roles (Admin, Profesor, Apoderado)
- [ ] Notificaciones por email a apoderados
- [ ] Reportes PDF (boletas, certificados)
- [ ] Exportación CSV/Excel de datos
- [ ] Filtros avanzados en dashboard (por periodo, grado)
- [ ] Edición/eliminación de registros en frontend
- [ ] Tests unitarios y de integración
- [ ] Migración a PostgreSQL (cuando se resuelva bug de Windows)
- [ ] Despliegue en producción (Azure/AWS/Heroku)

### 📋 Uso del Sistema

#### 1. Generar Datos de Prueba
```powershell
cd proyecto_educativo
python manage.py generar_datos --reset
```

#### 2. Iniciar el Servidor
```powershell
python manage.py runserver
```

#### 3. Acceder al Sistema
- **Dashboard Principal**: http://127.0.0.1:8000/
- **Lista de Estudiantes**: http://127.0.0.1:8000/estudiantes/
- **Registrar Calificación**: http://127.0.0.1:8000/registrar-calificacion/
- **Registrar Asistencia**: http://127.0.0.1:8000/registrar-asistencia/
- **API REST**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/ (requiere createsuperuser)

#### 4. Crear Superusuario (opcional)
```powershell
python manage.py createsuperuser
```

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