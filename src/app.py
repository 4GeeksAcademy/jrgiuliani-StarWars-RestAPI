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
from models import db, User, Planets, FavoritePlanet, People, FavoritePeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = User.query.all()
    users_serialized=[]
    for user in all_users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({"data":users_serialized}), 200

@app.route("/user/<int:id>", methods=['GET'])
def single_user(id):
    single_user=User.query.get(id)
    if single_user is None:
        return jsonify({"msg":"El usuario con el id {} no existe".format(id)}),400
    print(single_user)
    return jsonify({"data":single_user.serialize()}),200

@app.route("/people", methods=['GET'])
def get_people():
    all_people = People.query.all()
    people_serialized =[]
    for person in all_people:
        people_serialized.append(person.serialize())
    print(people_serialized)
    return jsonify({"data":people_serialized}),200

@app.route("/people/<int:id>", methods=['GET'])
def get_character(id):
    character = People.query.get(id)
    if character is None:
        return jsonify({"msg":"El usuario con el id {} no existe".format(id)}), 400
    print(character)
    return jsonify({"data":character.serialize()}),200

@app.route("/planets", methods = ['GET'])
def get_planets():
    all_planets = Planets.query.all()
    planets_serialized = []
    for planet in all_planets:
        planets_serialized.append(planet.serialize())
    print(planets_serialized)
    return jsonify({"data":planets_serialized}),200

@app.route("/planets/<int:id>", methods = ['GET'])
def get_planet(id):
    single_planet = Planets.query.get(id)
    if single_planet is None:
        return jsonify({"msg":"El planeta con id {} no existe".format(id)}), 400
    print(single_planet)
    return jsonify({"data":single_planet.serialize()}),200

@app.route("/planet", methods=['POST'])
def new_planet():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"Debes enviar informacion en el body"}),400
    if "name" not in body:
        return jsonify({"msg":"El campo name es obligatorio"}),400
    
    new_planet = Planets()
    new_planet.name = body["name"]
   
    new_planet.population = body["population"]
    db.session.add(new_planet)
    db.session.commit()

@app.route("/user/<int:id>/favorites", methods = ["GET"])
def get_favorites(id):
    user=User.query.get(id)
    if user is None: 
        return jsonify({"msg":f"El usuario con ID {id} no existe"}),404
    '''
    favorite_planets = FavoritePlanet.query.filter_by(user_id=id).all()
    favorite_planets_serialized =[]
    for favorite_planet in favorite_planets:
        favorite_planets_serialized.append(favorite_planet.serialize())
    '''
    favorite_planets = db.session.query(FavoritePlanet, Planets).join(Planets).\
        filter(FavoritePlanet.user_id == id).all()
    favorite_planets_serialized = []
    for favorite_planet, planet in favorite_planets:
        favorite_planets_serialized.append({'favorite_planet_id': favorite_planet.id,
    "planet": planet.serialize(),
    "user_id": id})

    favorite_people = db.session.query(FavoritePeople, People).join(People).\
        filter(FavoritePeople.user_id == id).all()
    favorite_people_serialized = []
    for favorite_people, people in favorite_people:
        favorite_people_serialized.append({'favorite_people_id': favorite_people.id,
    "people": people.serialize(),
    "user_id": id})

    return jsonify({"msg":"ok","favorite_planets":favorite_planets_serialized,
                     "favorite_peole":favorite_people_serialized})

@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def new_fav_planet(planet_id):
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"Debes enviar informacion en el body"}),400
    if "planet_id" not in body:
        return jsonify({"msg":"Debes enviar el planet_id"}),400
    if "user_id" not in body:
        return jsonify({"msg":"Debes enviar el user_id"}),400
    
    new_fav_planet=FavoritePlanet()
    new_fav_planet.planet_id=body["planet_id"]
    new_fav_planet.user_id=body["user_id"]
    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify({"msg":"Nuevo planeta favorito agregado",
                    "data":new_fav_planet.serialize()}),201

@app.route("/favorite/people/<int:people_id>", methods= ['POST'])
def new_fav_people(people_id):
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"Debes enviar informacion en el body"}), 400
    if "people_id" not in body:
        return jsonify({"msg":"Debes enviar el people_id"})
    if "user_id" not in body:
        return jsonify({"msg":"Debes enviar el user_id"})
    
    new_fav_people= FavoritePeople()
    new_fav_people.people_id = body["people_id"]
    new_fav_people.user_id = body["user_id"]
    db.session.add(new_fav_people)
    db.session.commit()

    return jsonify({"msg":"Nuevo personaje favorito agrgado",
                    "data":new_fav_people.serialize()}),201


@app.route("/favorite/planet/<int:planet_id>", methods = ['DELETE'])
def delete_fav_planet(planet_id):
    fav_planet = FavoritePlanet.query.get(planet_id)
    if fav_planet is None:
        return jsonify({'msg':'Favorite not found'}),404
    db.session.delete(fav_planet)
    db.session.commit()
    
    return jsonify({"msg":"favorito eliminado"}), 204
    
@app.route("/favorite/people/<int:people_id>", methods = ['DELETE'])
def delete_fav_people(people_id):
    fav_people = FavoritePeople.query.get(people_id)
    if fav_people is None:
        return jsonify({"msg":"Favorite not found"}),404
    db.session.delete(fav_people)
    db.session.commit()

    return jsonify({"msg":"favorito eliminado"}), 204

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
