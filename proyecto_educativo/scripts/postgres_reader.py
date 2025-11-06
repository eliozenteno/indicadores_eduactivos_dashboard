#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para consumir datos de PostgreSQL tabla indicadores_educativos
sin pasar por Django (evita el bug de encoding de psycopg2 en Windows).

Este script se puede ejecutar directamente o importar sus funciones
desde views de Django.
"""
import os
import sys

# Configurar encoding antes de importar psycopg2
if sys.platform == 'win32':
    # Estos settings ayudan con el encoding en Windows
    os.environ.setdefault('PGCLIENTENCODING', 'UTF8')
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 no instalado. Ejecuta: pip install psycopg2-binary")
    sys.exit(1)


# Configuración de conexión (ajusta si es necesario)
DB_CONFIG = {
    'dbname': 'dashboard_colegio',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432,
}


def get_connection():
    """
    Obtiene una conexión a PostgreSQL.
    Retorna: conexión psycopg2 o None si falla
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return None


def fetch_indicadores_educativos(limit=100, offset=0):
    """
    Obtiene registros de la tabla indicadores_educativos.
    
    Args:
        limit: número máximo de registros a retornar
        offset: número de registros a saltar (para paginación)
    
    Returns:
        Lista de diccionarios con los datos, o lista vacía si hay error
    """
    conn = get_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Verifica si la tabla existe
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'indicadores_educativos'
                );
            """)
            exists = cur.fetchone()['exists']
            
            if not exists:
                print("ADVERTENCIA: Tabla 'indicadores_educativos' no encontrada")
                return []
            
            # Obtiene los datos
            cur.execute(
                "SELECT * FROM indicadores_educativos ORDER BY id LIMIT %s OFFSET %s;",
                (limit, offset)
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]
            
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        return []
    finally:
        conn.close()


def get_indicadores_count():
    """
    Cuenta el número total de registros en indicadores_educativos.
    
    Returns:
        Número entero con el conteo, o 0 si hay error
    """
    conn = get_connection()
    if not conn:
        return 0
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM indicadores_educativos;")
            count = cur.fetchone()[0]
            return count
    except Exception as e:
        print(f"Error contando registros: {e}")
        return 0
    finally:
        conn.close()


def get_indicadores_by_filter(filters=None, limit=100):
    """
    Obtiene registros filtrados de indicadores_educativos.
    
    Args:
        filters: diccionario con filtros, ej: {'columna': 'valor'}
        limit: número máximo de registros
    
    Returns:
        Lista de diccionarios con los datos filtrados
    """
    conn = get_connection()
    if not conn:
        return []
    
    filters = filters or {}
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Construye la query con filtros
            where_clauses = []
            params = []
            
            for key, value in filters.items():
                where_clauses.append(f"{key} = %s")
                params.append(value)
            
            where_str = " AND ".join(where_clauses) if where_clauses else "1=1"
            query = f"SELECT * FROM indicadores_educativos WHERE {where_str} LIMIT %s;"
            params.append(limit)
            
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            return [dict(row) for row in rows]
            
    except Exception as e:
        print(f"Error ejecutando query filtrada: {e}")
        return []
    finally:
        conn.close()


# Función de prueba para ejecutar desde línea de comandos
if __name__ == '__main__':
    print("=" * 60)
    print("PRUEBA DE CONEXIÓN A POSTGRESQL")
    print("=" * 60)
    
    # Test 1: Conexión
    print("\n1. Probando conexión...")
    conn = get_connection()
    if conn:
        print("   ✓ Conexión exitosa")
        conn.close()
    else:
        print("   ✗ Conexión fallida")
        sys.exit(1)
    
    # Test 2: Conteo
    print("\n2. Contando registros...")
    count = get_indicadores_count()
    print(f"   Total de registros: {count}")
    
    # Test 3: Obtener primeros 5 registros
    print("\n3. Obteniendo primeros 5 registros...")
    registros = fetch_indicadores_educativos(limit=5)
    if registros:
        print(f"   ✓ Obtenidos {len(registros)} registros")
        print("\n   Primer registro (muestra):")
        primer_reg = registros[0]
        for key, value in list(primer_reg.items())[:10]:  # Muestra primeras 10 columnas
            print(f"      {key}: {value}")
        if len(primer_reg) > 10:
            print(f"      ... y {len(primer_reg) - 10} columnas más")
    else:
        print("   ✗ No se obtuvieron registros (tabla vacía o no existe)")
    
    print("\n" + "=" * 60)
    print("FIN DE PRUEBA")
    print("=" * 60)
