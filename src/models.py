from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'Usuario con email:{}'.format(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    rotation_period = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    diameter = db.Column(db.String(50))
    climate = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.String(50))
    population = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Planet {self.id} {self.name}"
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "diameter":self.diameter,
            "climate":self.climate,
            "gravity":self.gravity,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
            "population":self.population,
        }
    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True, nullable=False)
    height = db.Column(db.String(25), nullable=False)
    mass = db.Column(db.String(25), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Character {self.id} {self.name}"
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color, 
            "eye_color":self.eye_color, 
            "birth_year":self.birth_year,
            "gender":self.gender 
        }

class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_id_relationship = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    planet_id_relationship = db.relationship(Planets)

    def __repr__(self):
        return f"Al usuario {self.user_id} le gusta el planeta {self.planet_id}"
    
    def serialize(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "planet_id":self.planet_id
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_id_relationship = db.relationship(User)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    people_id_relationship = db.relationship(People)

    def __repr__(self):
        return f"Al usuario {self.user_id} le gusta el personaje {self.people_id}"
    
    def serialize(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "people_id":self.people_id
        }