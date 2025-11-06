#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test direct PostgreSQL connection without Django to diagnose encoding issues.
"""
import sys
import os

# Force UTF-8 encoding
if sys.platform == 'win32':
    os.environ['PGCLIENTENCODING'] = 'UTF8'

try:
    import psycopg2
    print("✓ psycopg2 imported successfully")
except ImportError as e:
    print(f"✗ Failed to import psycopg2: {e}")
    sys.exit(1)

# Test connection
conn_params = {
    'dbname': 'dashboard_colegio',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1',  # Use IP to avoid encoding issues
    'port': 5432,
}

print(f"\nTrying to connect to PostgreSQL...")
print(f"  Database: {conn_params['dbname']}")
print(f"  Host: {conn_params['host']}:{conn_params['port']}")
print(f"  User: {conn_params['user']}")

try:
    conn = psycopg2.connect(**conn_params)
    print("✓ Connection successful!")
    
    # Test query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"\n✓ PostgreSQL version: {version[0]}")
    
    # Check for indicadores_educativos table
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    print(f"\n✓ Found {len(tables)} tables in public schema:")
    for table in tables[:10]:  # Show first 10
        print(f"  - {table[0]}")
    if len(tables) > 10:
        print(f"  ... and {len(tables) - 10} more")
    
    # Check specifically for indicadores_educativos
    cur.execute("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'indicadores_educativos'
        );
    """)
    exists = cur.fetchone()[0]
    if exists:
        print(f"\n✓ Table 'indicadores_educativos' EXISTS")
        cur.execute("SELECT COUNT(*) FROM indicadores_educativos;")
        count = cur.fetchone()[0]
        print(f"  Rows in table: {count}")
    else:
        print(f"\n✗ Table 'indicadores_educativos' NOT FOUND")
    
    cur.close()
    conn.close()
    print("\n✓ Connection closed successfully")
    
except psycopg2.OperationalError as e:
    print(f"\n✗ OperationalError: {e}")
    print("\nPossible causes:")
    print("  - PostgreSQL service not running")
    print("  - Wrong credentials (user/password)")
    print("  - Database doesn't exist")
    print("  - Firewall blocking connection")
    sys.exit(1)
except UnicodeDecodeError as e:
    print(f"\n✗ UnicodeDecodeError: {e}")
    print("\nThis is a Windows-specific psycopg2 issue.")
    print("Trying workaround...")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Unexpected error: {type(e).__name__}: {e}")
    sys.exit(1)
