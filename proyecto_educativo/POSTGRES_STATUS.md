# Integración con PostgreSQL - Estado y Soluciones

## ⚠️ Problema Detectado

Se encontró un bug de encoding en `psycopg2` en Windows que impide la conexión directa a PostgreSQL desde este proyecto Django:

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xab in position 96: invalid start byte
```

Este es un problema conocido de psycopg2 en Windows cuando hay variables de entorno del sistema con caracteres no-UTF8.

## ✅ Estado Actual del Proyecto

- **Base de datos principal**: SQLite (`db.sqlite3`) - ✓ Funcionando perfectamente
- **Modelos Django**: 12 modelos completos (Estudiante, Profesor, Curso, Calificaciones, etc.) - ✓ Operativos
- **API REST**: Django REST Framework configurado y funcionando - ✓ Endpoints disponibles en `/api/`
- **Conexión PostgreSQL**: ❌ Bloqueada por bug de psycopg2

## 🔧 Soluciones Disponibles

### Opción A: Usar SQLite (Recomendada para desarrollo)

**Estado**: ✅ Funcionando ahora mismo

El proyecto ya funciona completamente con SQLite:
- Todos los modelos funcionan
- API REST operativa
- Admin panel accesible
- CRUD verificado

**Para continuar con esta opción:**
```powershell
# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Acceder:
# - Admin: http://127.0.0.1:8000/admin
# - API: http://127.0.0.1:8000/api/
```

### Opción B: Acceder a PostgreSQL desde fuera de Django

**Herramientas recomendadas:**

1. **pgAdmin** (interfaz gráfica)
   - Conéctate a `localhost:5432`
   - Database: `dashboard_colegio`
   - User: `postgres`
   - Consulta directamente la tabla `indicadores_educativos`

2. **DBeaver** (alternativa multiplataforma)
   - Mismas credenciales que pgAdmin

3. **Script Python externo** (sin Django)
   Creamos un script que se puede ejecutar fuera del proyecto:
   ```powershell
   # Ubicación: scripts/postgres_reader.py
   python scripts\postgres_reader.py
   ```
   ⚠️ Actualmente este script también falla por el mismo bug de encoding.

### Opción C: Exportar/Importar datos

Si necesitas los datos de PostgreSQL en el proyecto Django:

1. **Exportar desde PostgreSQL**:
   ```powershell
   # Usando pg_dump (si tienes psql instalado)
   pg_dump -h localhost -U postgres -d dashboard_colegio -t indicadores_educativos --data-only --column-inserts > data.sql
   ```

2. **Convertir a fixtures de Django**:
   - Usar pgAdmin para exportar a CSV
   - Crear un script que convierta CSV a fixtures JSON de Django
   - Cargar con `python manage.py loaddata`

3. **Copiar tabla directamente** (si ambas DBs están accesibles):
   - Usar herramientas ETL como pgLoader o scripts personalizados

### Opción D: Reparar psycopg2 (Avanzado)

El error sugiere que hay una variable de entorno del sistema con caracteres no-UTF8. 

**Pasos para diagnosticar:**

1. Abre PowerShell como Administrador y ejecuta:
   ```powershell
   # Lista TODAS las variables de entorno
   Get-ChildItem Env: | Format-Table -AutoSize
   
   # Busca variables que puedan tener caracteres raros
   Get-ChildItem Env: | Where-Object { $_.Value -match '[^\x00-\x7F]' }
   ```

2. Busca variables relacionadas con PostgreSQL (`PG*`, `POSTGRES*`) o con rutas que contengan caracteres especiales.

3. Elimina o corrige esas variables de entorno desde:
   - Panel de Control → Sistema → Configuración avanzada del sistema → Variables de entorno

4. Reinicia PowerShell/VSCode y vuelve a intentar.

**Alternativa:** Reinstalar PostgreSQL y psycopg2:
```powershell
pip uninstall psycopg2-binary
pip install psycopg2-binary
```

## 📊 Uso de Datos para el Dashboard

Dado que SQLite ya funciona, puedes:

1. **Crear datos de prueba en SQLite** para desarrollar el dashboard
2. **Importar datos reales desde PostgreSQL** usando pgAdmin → Export CSV → script de carga
3. **Conectar el dashboard a PostgreSQL cuando se resuelva el encoding** (o en otro entorno/máquina sin el bug)

## 🎯 Recomendación Inmediata

**Para avanzar con el proyecto AHORA:**

1. ✅ Usar SQLite como está (ya funciona)
2. ✅ Desarrollar el dashboard con datos de prueba o importados
3. ✅ Crear vistas y KPIs usando los modelos Django existentes
4. ⏳ Resolver el problema de PostgreSQL en paralelo (investigar variables de entorno)
5. ⏳ Migrar a PostgreSQL cuando se resuelva o en otro entorno (ej: Linux, Docker, otra máquina Windows sin el bug)

## 📁 Archivos Creados

- `scripts/check_postgres.py` - Script de verificación inicial
- `scripts/postgres_reader.py` - Script standalone para leer PostgreSQL
- `scripts/test_pg_clean.py` - Script con limpieza de variables de entorno
- `indicadores/management/commands/query_indicadores.py` - Comando Django para consultar Postgres

Todos estos scripts fallan actualmente por el bug de encoding.

## ✉️ Siguiente Paso Sugerido

Dime qué prefieres:

1. **Continuar con SQLite** y desarrollar el dashboard → Te ayudo a poblar datos de prueba y crear las vistas/KPIs
2. **Intentar resolver el bug de psycopg2** → Te guío para limpiar variables de entorno del sistema
3. **Importar datos desde PostgreSQL a SQLite** → Te creo un script de migración usando pgAdmin + CSV
4. **Probar en otro entorno** (Docker, WSL, otra máquina)

Confirma cuál opción prefieres y continuamos inmediatamente.
