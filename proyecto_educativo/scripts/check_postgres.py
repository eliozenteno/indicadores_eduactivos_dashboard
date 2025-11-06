"""
Simple helper to test PostgreSQL connection and check for the table
`indicadores_educativos`.

Usage (after installing psycopg2-binary if needed):
    python scripts/check_postgres.py

This script attempts to connect with the credentials below. Edit them if needed.
"""
import sys

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception as e:
    print("ERROR: psycopg2 is not installed or failed to import.")
    print("Install it with: pip install psycopg2-binary")
    print("Import error:", e)
    sys.exit(1)

# --- Edit these credentials if your DB uses different values ---
DB = {
    'dbname': 'dashboard_colegio',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432,
}
# ---------------------------------------------------------------

SQL_CHECK_TABLE = """
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = %s
LIMIT 1;
"""

SQL_SAMPLE = "SELECT * FROM indicadores_educativos LIMIT 5;"


def main():
    print("Trying to connect to PostgreSQL with:", DB)
    try:
        conn = psycopg2.connect(**DB)
    except Exception as e:
        print("Connection failed:", e)
        sys.exit(2)

    print("Connected to PostgreSQL OK")
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(SQL_CHECK_TABLE, ("indicadores_educativos",))
        found = cur.fetchone()
        if not found:
            print("Table 'indicadores_educativos' NOT found in the database.")
            print("Check the schema name or table name (case-sensitive on some setups).")
            # optionally list tables in public schema
            print('\nListing tables in public schema:')
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;")
            for r in cur.fetchall():
                print('-', r['table_name'])
            conn.close()
            sys.exit(3)

        print("Found table:", found)
        print("Trying to fetch up to 5 rows from 'indicadores_educativos'...")
        try:
            cur.execute(SQL_SAMPLE)
            rows = cur.fetchall()
            if not rows:
                print("Table exists but returned 0 rows.")
            else:
                print(f"Fetched {len(rows)} rows (sample):")
                for r in rows:
                    print(r)
        except Exception as e:
            print("Query failed (maybe table columns or permissions):", e)
            print("If the table is in a different schema, try schema.table_name or adjust search_path.")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
