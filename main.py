# main.py
import os
from flask import Flask, jsonify, redirect, request
#Importacion del controlador y objeto
from src.controllers.pokemon import PokemonID
import sys
from src.controllers.indexController import IndexController
from src.controllers.comprasController import ComprasController
from src.controllers.contactoController import ContactoController
from src.controllers.nosotrosController import NosotrosController
from src.controllers.loginController import LoginController
from src.controllers.registroController import RegistroController
from src.controllers.comentariosController import ComentariosController
from src.cn.data_base_connection import initialize_database
from src.controllers.productosController import ProductosController
from src.models.productosModel import ProductoModel
from src.controllers.asistenteController import AsistenteController
from src.controllers.logoutController import LogOutController
#from src.controllers.carritoController import CarritoController


app = Flask(__name__, static_url_path='/static')

# Configurar la conexión a la base de datos (PostgreSQL en este caso)
initialize_database(app)

if 'FLASK_SECRET_KEY' not in os.environ:
    os.environ['FLASK_SECRET_KEY'] = os.urandom(24).hex()

# Configurar la clave secreta para las sesiones desde las variables de entorno
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Redireccionar la raíz al index
@app.route('/')
def root():
    return redirect('/index/')

# Index Controller
index_controller = IndexController(app)
app.register_blueprint(index_controller.get_blueprint(), url_prefix='/index')

# Compras Controller
compras_controller = ComprasController(app)
app.register_blueprint(compras_controller.get_blueprint(), url_prefix='/compras')

# Contacto Controller
# En el código de main.py
contacto_controller = ContactoController(app)
app.register_blueprint(contacto_controller.get_blueprint(), url_prefix='/contacto')


# Nosotros Controller
nosotros_controller = NosotrosController(app)
app.register_blueprint(nosotros_controller.get_blueprint(), url_prefix='/nosotros')

# Login Controller
login_controller = LoginController(app)
app.register_blueprint(login_controller.get_blueprint(), url_prefix='/login')

# Registro Controller
registro_controller = RegistroController(app)
app.register_blueprint(registro_controller.get_blueprint(), url_prefix='/registro')

# Comentarios Controller
comentarios_controller = ComentariosController(app)
app.register_blueprint(comentarios_controller.get_blueprint(), url_prefix='/comentarios')

productos_controller = ProductosController(app)
app.register_blueprint(productos_controller.get_blueprint(), url_prefix= '/productos')

#carrito_controller = CarritoController(app)
#app.register_blueprint(carrito_controller.get_blueprint(), url_prefix= '/productos')

asistente_controller = AsistenteController(app)
app.register_blueprint(asistente_controller.get_blueprint(), url_prefix= '/asistente')
    
logout_Controller = LogOutController(app)
app.register_blueprint(logout_Controller.get_blueprint(), url_prefix='/logout')








# Crear una instancia de Pokemon
Pokemon_inst = PokemonID(app, "prefix")

    # Definir una ruta que maneje solicitude+s con parámetros
@app.route('/pokemon/<int:pokemon_id>')
def get_pokemon_description(pokemon_id):
    # Obtener la información del Pokémon desde la base de datos
    pokemon_data = Pokemon_inst.get_pokemon_by_id(pokemon_id)

    if pokemon_data:
        # Mostrar la información del Pokémon
        pokemon_description = f"{pokemon_data[1]}, Descripcion: {pokemon_data[2]}"
    else:
        # Mostrar un mensaje si no se encuentra el Pokémon
        pokemon_description = "No se encontró la descripción del Pokémon."

    return pokemon_description

@app.route('/pokemon', methods=['POST'])
def add_pokemon():
    if request.method == 'POST':
        pokemon = request.json.get('pokemon')
        description = request.json.get('description')

        if pokemon and description:
            pokemon_id = Pokemon_inst.add_pokemon(pokemon, description)
            return jsonify({'id': pokemon_id, 'message': 'Pokémon agregado correctamente.'}), 201
        else:
            return jsonify({'error': 'Se requieren el nombre y la descripción del Pokémon.'}), 400
    # Iniciar la aplicación Flask
if __name__ == '__main__':    
    app.run(debug=True)