from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Query sample rows from the external table 'indicadores_educativos' using the postgres connection"

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=5, help='Number of rows to fetch')

    def handle(self, *args, **options):
        limit = options.get('limit', 5)
        self.stdout.write('Using DB connection: postgres')
        try:
            with connections['postgres'].cursor() as cursor:
                # Check that connection works
                cursor.execute("SELECT 1;")
                cursor.fetchone()
        except KeyError:
            self.stderr.write("No 'postgres' database configured in settings.DATABASES. Edit settings.py to add it.")
            return
        except OperationalError as e:
            self.stderr.write(f"OperationalError connecting to postgres: {e}")
            return

        sql_check = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = %s LIMIT 1;"
        try:
            with connections['postgres'].cursor() as cursor:
                cursor.execute(sql_check, ('indicadores_educativos',))
                found = cursor.fetchone()
                if not found:
                    self.stdout.write("Table 'indicadores_educativos' NOT found in the postgres database.")
                    self.stdout.write('Listing tables in public schema:')
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;")
                    for row in cursor.fetchall():
                        self.stdout.write(' - ' + row[0])
                    return

                self.stdout.write(f"Found table: schema={found[0]}, name={found[1]}")

                # Try to fetch sample rows
                try:
                    cursor.execute(f"SELECT * FROM indicadores_educativos LIMIT %s;", (limit,))
                    rows = cursor.fetchall()
                    if not rows:
                        self.stdout.write('Table exists but returned 0 rows')
                        return
                    # Print rows in a compact way
                    self.stdout.write(f"--- Sample {len(rows)} rows ---")
                    # Print column names if available
                    col_names = [desc[0] for desc in cursor.description]
                    self.stdout.write(' | '.join(col_names))
                    for r in rows:
                        self.stdout.write(' | '.join([str(x) for x in r]))
                except Exception as e:
                    self.stderr.write(f"Failed to fetch rows: {e}")
        except Exception as e:
            self.stderr.write(f"Unexpected error: {e}")
