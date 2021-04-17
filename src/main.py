"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Mascota

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def GetUser():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/login', methods=['POST'])
def Login():
    # OBTENIENDO LOS DATOS
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # FILTRANDO POR EMAIL Y PASSWORD
    # FIRST() PARA ELIMINAR EL DUPLICADO DE DATOS
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401

    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route('/users', methods=['GET'])
def GetAllUsers():
    users = User.query.all()
    responseUsers = list(map(lambda user: user.serialize(), users))
    return jsonify(responseUsers), 200

@app.route('/mascota/<int:idUsuario>', methods=['GET'])
def GetMascotaByIdUser(idUsuario):
    mascotasDelUsuario = Mascota.query.filter_by(idUser=idUsuario)
    """
    RespuestaMascotas = mascotas.map((mascota)=>{
        return mascota.serialize();
    }) 
    """
    respuestaMascotas = list(map(lambda mascota: mascota.serialize(), mascotasDelUsuario))
    return jsonify(respuestaMascotas), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
