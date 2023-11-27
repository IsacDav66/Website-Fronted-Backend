# src/controllers/baseController.py
from flask import Blueprint, redirect, render_template, session
from datetime import datetime, timedelta
from src.cn.data_base_connection import get_database_connection
class PokemonID:
    def __init__(self, app, prefix):
        self.app = app
        self.prefix = prefix
        self.blueprint = Blueprint(self.prefix, __name__)

       
       

  
    def get_pokemon_by_id(self, pokemon_id):
        # Conéctate a la base de datos y realiza una consulta SQL
        connection = get_database_connection(self.app)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM pokemons WHERE id = %s;", (pokemon_id,))
        pokemon_data = cursor.fetchone()

        cursor.close()
        connection.close()

        return pokemon_data

        
    def add_pokemon(self, name, description):
        try:
            connection = get_database_connection(self.app)
            cursor = connection.cursor()

            # Insertar el nuevo Pokémon en la base de datos
            cursor.execute("INSERT INTO pokemons (pokemon, description) VALUES (%s, %s) RETURNING id", (name, description))
            new_pokemon_id = cursor.fetchone()[0]

            connection.commit()
            return new_pokemon_id
        except Exception as e:
            print(f"Error al agregar el Pokémon a la base de datos: {e}")
            raise
        finally:
            cursor.close()
            connection.close()

            
            
    def get_app(self):
        return self.app

