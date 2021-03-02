from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = relationship("World")

    def __repr__(self):
        return '<User %r>' % self.username

class World(db.Model):
    __tablename__ = 'Worlds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'))

class Location_character(db.Model):
    __tablename__ = 'Location_character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'))
    description = db.Column(text(400))
    world_id = Column(Integer, ForeignKey('world.id'))
    location = db.Column(Boolean, nullable = False)

class Notes(db.Model):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(text(400))
    creator_id = Column(Integer, ForeignKey('user.id'))
    location/character_id = Column(Integer, ForeignKey('location_character.id'))

class User_Worlds(db.Model):
    __tablename__ = 'User_worlds'
    id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    world_id = Column(Integer, ForeignKey('world.id'))
