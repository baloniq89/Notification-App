import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.connection = self._connect()

    def _connect(self):
        try:
            connection = psycopg2.connect(
                dbname="notification",
                user="admin",
                password="admin",
                host="db",
                cursor_factory=RealDictCursor
            )
            print("Database connection established.")
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def fetch_all(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def execute(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or [])
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
