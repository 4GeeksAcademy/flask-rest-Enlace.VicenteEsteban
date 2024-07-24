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
from models import db, User, People, Planet, Favorites_planet, Favorites_people
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


@app.route('/user/', methods=['GET'])
def get_users():
    user_query=User.query.all()
    user_list=list(map(lambda user:user.serialize(),user_query))
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(user_list), 200
   

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    user=User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"info":"Not found"}), 404
    print(user.favorites_planets)
    print(user.favorites_people)
    output=user.serialize()
    output["favorites_planets"]=list(
        map(lambda planet:planet.serialize(),user.favorites_planets)) 
    output["favorites_people"]=list(
        map(lambda people:people.serialize(),user.favorites_people))
    
    return jsonify(output), 200

   

@app.route('/people/', methods=['GET'])
def get_people():
    people_query=People.query.all()
    people_list=list(map(lambda people:people.serialize(),people_query))

    return jsonify(people_list), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):

    one_people=People.query.filter_by(id=people_id).first()
    if one_people is None:
        return jsonify({"info":"Not found"}), 404
    print(one_people)
    return jsonify(one_people.serialize()), 200


@app.route('/planets/', methods=['GET'])
def get_planet():
    planets_query=Planet.query.all()
    planets_list=list(map(lambda planet:planet.serialize(),planets_query))
   
    return jsonify(planets_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):

    one_planet=Planet.query.get(planet_id)
    if one_planet is None:
        return jsonify({"info":"Not found"}), 404
    print(one_planet)
    return jsonify(one_planet.serialize()), 200


@app.route('/user/favorites/', methods=['GET'])
def get_favorites():

   
    favorites_query_people=Favorites_people.query.all()
    favorites_query_planet=Favorites_planet.query.all()
    favorite_list=list(map(lambda favorite:favorite.serialize(),favorites_query_people)) + list(map(lambda favorite:favorite.serialize(),favorites_query_planet))
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(favorite_list), 200




@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def favorite_planet(planet_id):
   
    request_body= request.json
    one_planet=Planet.query.filter_by(id=planet_id).first()
    if one_planet is None:
        return jsonify({"info":"Not found"}), 404
    one_user=User.query.filter_by(id=request_body["user_id"]).first()
    if one_user is None:
        return jsonify({"info":"Not found"}), 404
    planet_favorites= Favorites_planet(user_id=request_body["user_id"],planet_id=planet_id)
    db.session.add(planet_favorites)
    db.session.commit()
    response_body={
        "msg":"Personaje creado"
    }
    return jsonify(response_body), 200
    

   
@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def favorite_people(people_id):
    request_body= request.json
    people_favorites= Favorites_people(user_id=request_body["user_id"],people_id=people_id)
    db.session.add(people_favorites)
    db.session.commit()
    response_body={
        "msg":"Personaje creado"
    }
    return jsonify(response_body), 200
   
@app.route('/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_people=Favorites_people.query.filter_by(people_id=people_id).first()
    if favorite_people is None:
        return jsonify({"info":"Not found"}), 404

    db.session.delete(favorite_people)
    db.session.commit()
    return jsonify({"Info":"Favorite people deleted"}), 200

@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet=Favorites_planet.query.filter_by(planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"info":"Not found"}), 404

    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"Info":"Favorite planet deleted"}), 200


    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)