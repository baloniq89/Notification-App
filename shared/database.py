import psycopg2
import psycopg2.extras

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="notification",
            user="admin",
            password="admin",
            host="db",
            port="5432"
        )
        self.connection.autocommit = True

    def execute(self, query, params=None):
        """Wykonuje zapytanie bez zwracania wyników."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

    def fetch_all(self, query, params=None):
        """Wykonuje zapytanie i zwraca wszystkie wyniki."""
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_and_fetchone(self, query, params=None):
        """Wykonuje zapytanie i zwraca jeden wynik."""
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query, params)
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
