import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

class DatabaseManager:
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

    def create(self, table, data):
        with self.connection_cursor() as cursor:
            insert = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                sql.SQL(', ').join(map(sql.Placeholder, data.keys()))
            )
            cursor.execute(insert, data)
            cursor.connection.commit()

    def read(self, table, condition=None):
        with self.connection_cursor() as cursor:
            if condition:
                select = sql.SQL('SELECT * FROM {} WHERE {}').format(
                    sql.Identifier(table),
                    sql.SQL(condition)
                )
            else:
                select = sql.SQL('SELECT * FROM {}').format(
                    sql.Identifier(table)
                )
            cursor.execute(select)
            rows = cursor.fetchall()
            return rows

    def update(self, table, data, condition):
        with self.connection_cursor() as cursor:
            set_clause = ', '.join([f'{column} = %({column})s' for column in data.keys()])
            update = sql.SQL(f'UPDATE {table} SET {set_clause} WHERE {condition}')
            cursor.execute(update, data)
            cursor.connection.commit()

    def delete(self, table, condition):
        with self.connection_cursor() as cursor:
            delete = sql.SQL(f'DELETE FROM {table} WHERE {condition}')
            cursor.execute(delete)
            cursor.connection.commit()
