from src.cn.data_base_connection import get_database_connection

class PokemonModel:
    @staticmethod
    def get_pokemon_by_id(pokemon_id):
        try:
            connection = get_database_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM pokemons WHERE id = %s;", (pokemon_id,))
            pokemon_data = cursor.fetchone()

            return pokemon_data

        except Exception as e:
            print(f"Error al obtener el Pokémon de la base de datos: {e}")
            raise

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def add_pokemon(name, description):
        try:
            connection = get_database_connection()
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
