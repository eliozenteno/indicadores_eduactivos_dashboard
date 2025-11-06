"""
Workaround para el bug de encoding de psycopg2 en Windows.
Limpia variables de entorno problemáticas antes de conectar.
"""
import os
import sys

# Limpia TODAS las variables de entorno relacionadas con PostgreSQL
# que podrían tener caracteres problemáticos
postgres_env_vars = [
    'PGAPPNAME', 'PGCLIENTENCODING', 'PGCONNECT_TIMEOUT', 'PGDATABASE',
    'PGDATESTYLE', 'PGGSSLIB', 'PGHOST', 'PGHOSTADDR', 'PGKRBSRVNAME',
    'PGLOCALEDIR', 'PGOPTIONS', 'PGPASSFILE', 'PGPASSWORD', 'PGPORT',
    'PGSERVICE', 'PGSERVICEFILE', 'PGSSLCERT', 'PGSSLCOMPRESSION',
    'PGSSLCRL', 'PGSSLKEY', 'PGSSLMODE', 'PGSSLROOTCERT', 'PGSYSCONFDIR',
    'PGTARGETSESSIONATTRS', 'PGTZ', 'PGUSER', 'PGGEQO', 'PGSYSCONFDIR',
]

for var in postgres_env_vars:
    if var in os.environ:
        del os.environ[var]

# Establece solo lo mínimo necesario en UTF-8
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Ahora importa psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de conexión
DB_CONFIG = {
    'dbname': 'dashboard_colegio',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432,
}

def test_connection():
    """Prueba de conexión simple"""
    try:
        print("Intentando conectar con configuración limpia...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ ¡CONEXIÓN EXITOSA!")
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"✓ PostgreSQL version: {version[:50]}...")
        
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name LIMIT 10;
        """)
        tables = cur.fetchall()
        print(f"✓ Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
