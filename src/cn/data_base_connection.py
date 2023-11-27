# src/database/data_base_connection.py
import os
import psycopg2
from dotenv import load_dotenv

def initialize_database(app):
    # Cargar variables de entorno desde .env
    load_dotenv()

def get_database_connection(app):
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('PG_NAME'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASS'),
            host=os.getenv('PG_HOST') or 'localhost',
            port=os.getenv('PG_PORT') or '5432'
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error en la conexión a la base de datos: {e}")
        raise
