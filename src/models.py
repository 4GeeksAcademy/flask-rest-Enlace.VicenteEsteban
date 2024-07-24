from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(120), unique=False,nullable=False)
    last_name=db.Column(db.String(120), unique=False,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return f"<User{self.first_name}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name":self.first_name,
            "last_name":self.last_name
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height =db.Column(db.String(120),unique=False,nullable=True)
    mass =db.Column(db.String(120),unique=False,nullable=True)
    hair_color =db.Column(db.String(120),unique=False,nullable=True)
    skin_color =db.Column(db.String(120),unique=False,nullable=True)
    eye_color =db.Column(db.String(120),unique=False,nullable=True)
    birth_year =db.Column(db.String(120),unique=False,nullable=True)
    gender =db.Column(db.String(120),unique=False,nullable=True)
    name =db.Column(db.String(120),unique=False,nullable=True)
    homeworld =db.Column(db.String(120),unique=False,nullable=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color":self.eye_color,
            "birth_year":self.birth_year,
            "gender":self.gender,
            "name":self.name,
            "homeworld":self.homeworld,

            # do not serialize the password, its a security breach
        }
    

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    diameter=db.Column(db.String(120),unique=False,nullable=False)
    rotation_period=db.Column(db.String(120),unique=False,nullable=False)
    orbital_period=db.Column(db.String(120),unique=False,nullable=False)
    gravity=db.Column(db.String(120),unique=False,nullable=False)
    population=db.Column(db.String(120),unique=False,nullable=False)
    climate=db.Column(db.String(120),unique=False,nullable=False)
    terrain=db.Column(db.String(120),unique=False,nullable=False)
    surface_water=db.Column(db.String(120),unique=False,nullable=False)
    name=db.Column(db.String(120),unique=False,nullable=False)
   
    

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "gravity":self.gravity,
            "population":self.population,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
             
            # do not serialize the password, its a security breach
        }
    

class Favorites_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'))
    user=db.relationship(User, backref="favorites_planets")
    planet=db.relationship(Planet)
    def __repr__(self):
        return f"{self.user.first_name} likes {self.planet.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "planet_id":self.planet_id,
            "user_id":self.user_id,
            "user":self.user.first_name,
            "planet":self.planet.name
            
            # do not serialize the password, its a security breach
        }


class Favorites_people(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'),nullable=True)
    user=db.relationship(User, backref="favorites_people")
    people=db.relationship(People)
    def __repr__(self):
        return f"{self.user.first_name} likes {self.people.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "people_id":self.people_id,
            "user_id":self.user_id,
            "user":self.user.first_name,
            "people":self.people.name
            # do not serialize the password, its a security breach
        }