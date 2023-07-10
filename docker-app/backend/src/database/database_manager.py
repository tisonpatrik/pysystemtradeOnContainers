from psycopg2 import sql
from src.database.database_connection import DatabaseConnection

class DatabaseManager:
    def __init__(self, db_connection:DatabaseConnection):
        self.db_connection = db_connection

    def create(self, table, data):
        with self.db_connection.connection_cursor() as cursor:
            insert = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                sql.SQL(', ').join(map(sql.Placeholder, data.keys()))
            )
            cursor.execute(insert, data)
            cursor.connection.commit()

    def read(self, table, condition=None):
        with self.db_connection.connection_cursor() as cursor:
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
        with self.db_connection.connection_cursor() as cursor:
            set_clause = ', '.join([f'{column} = %({column})s' for column in data.keys()])
            update = sql.SQL(f'UPDATE {table} SET {set_clause} WHERE {condition}')
            cursor.execute(update, data)
            cursor.connection.commit()

    def delete(self, table, condition):
        with self.db_connection.connection_cursor() as cursor:
            delete = sql.SQL(f'DELETE FROM {table} WHERE {condition}')
            cursor.execute(delete)
            cursor.connection.commit()
