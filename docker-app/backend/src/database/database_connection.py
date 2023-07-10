import os
from contextlib import contextmanager
import psycopg2

class DatabaseConnection:
    def __init__(self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_PORT = os.getenv('DB_PORT')

    @contextmanager
    def connection_cursor(self):
        conn = psycopg2.connect(
            dbname=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
            conn.close()
