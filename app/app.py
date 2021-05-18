import json

from flask import Flask, session, redirect, url_for, render_template, request, flash, jsonify
from flask_login import LoginManager, UserMixin, logout_user, login_user, current_user
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Login manager
login = LoginManager(app)


# Database Configuration
app.config['UPLOAD_FOLDER'] = '/doc/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

Migrate(app, db)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_worlds = db.relationship("World", backref='creator')
    created_characters = db.relationship("Characters", backref='creator')
    created_locations = db.relationship("Locations", backref='creator')
    created_notes = db.relationship("Notes", backref='creator')

class World(db.Model):
    __tablename__ = 'worlds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(500))
    creator_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)


class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, ForeignKey('worlds.id'), nullable=False)
    creator_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    location_id = db.Column(db.Integer, ForeignKey('locations.id'))
    character_id = db.Column(db.Integer, ForeignKey('characters.id'))


class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100))
    world_id = db.Column(db.Integer, ForeignKey('worlds.id'))
    creator_id = db.Column(db.Integer, ForeignKey('users.id'))
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    notes = db.relationship("Notes", backref='location')


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(80), nullable=False)
    world_id = db.Column(db.Integer, ForeignKey('worlds.id'), nullable=False)
    creator_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    str = db.Column(db.Integer)
    con = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    int = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    cha = db.Column(db.Integer)
    player_character = db.Column(db.Boolean)
    player_id = db.Column(db.Integer, nullable=True)
    notes = db.relationship("Notes", backref='character')


class User_world_connector(db.Model):
    __tablename__ = 'user_world_connector'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    world_id = db.Column(db.Integer, ForeignKey('worlds.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    if not session.get("user_name"):
        flash('Please log in to continue to your World Page.')
        return redirect(url_for('login'))

    username = session.get("user_name")
    user_id = session.get("id")
    worlds = World.query.filter_by(creator_id=user_id).all()

    # Find all worlds that user is in as a player
    connected_worlds = User_world_connector.query.filter_by(user_id=user_id).all()
    if connected_worlds != None:
        for world in connected_worlds:
            connected_world = World.query.filter_by(id=world.world_id).first()

            # Make sure there are no duplicates
            if connected_world not in worlds:
                worlds.append(connected_world)

    return render_template("index.html", worlds=worlds)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        hashed_password = generate_password_hash(password)

        try:
            user = User(username=username, password=hashed_password, email=email)
            db.session.add(user)
            db.session.commit()
        except:
            flash('Username already in use.')
            return redirect('/register')

        session["logged_in"] = True
        session["user_name"] = username
        session["id"] = user.id
        db.session.commit()
        login_user(user)

        return render_template("registered.html")



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session.get("user_name"):
            flash('You are already logged in.')
            return redirect(url_for('index'))
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Incorrect username or password. Please try again.')
            return redirect(url_for('login'))

        # Checking hashed password
        result = check_password_hash(user.password, password)
        if result is False:
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))

        else:
            session["logged_in"] = True
            session["user_name"] = username
            session["id"] = user.id
            db.session.commit()
            login_user(user)

            return redirect(url_for('index'))

        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session["logged_in"] = False
    session["user_name"] = None
    logout_user()
    return redirect("/")


@app.route('/profile/<user_id>', methods=["GET"])
def profile(user_id):
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))


    if int(session["id"]) is not int(user_id):
        flash('For now, you cannot visit other peoples userpage.')
        return redirect(url_for('index'))

    user = User.query.filter_by(id=user_id).first()
    all_notes = Notes.query.filter_by(creator_id=user.id).all()


    return render_template("profile.html", user=user, notes=all_notes)


@app.route('/new_world', methods=["POST", "GET"])
def new_world():
    if request.method == "GET":
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        all_users = User.query.all()

        return render_template("new_world.html", users=all_users)

    if request.method == "POST":
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        world_name = request.form.get("world_name")
        world_description = request.form.get("description")


        if len(world_description) > 500:
            flash('Max amount of words exceeded.')
            return redirect('/new_world')
        else:
            world = World(name=world_name, description=world_description, creator_id=session["id"])
            world_id = world.id

            flash("world created")
            db.session.add(world)
            db.session.commit()
        return redirect("/")


@app.route('/new_character/<world_id>', methods=["POST", "GET"])
def new_character(world_id):
    if request.method == "GET":
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))
        return render_template("new_character.html", world_id=world_id)

    if request.method == "POST":
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        pc = request.form.get("PC")
        character_name = request.form.get("character_name")
        user_id = session["id"]

        if request.form.get("PC") == "PC":
            character = Characters(character_name=request.form.get("character_name"), world_id=world_id,
                                   description=request.form.get("description"),
                                   str=request.form.get("str"), con=request.form.get("con"),
                                   dex=request.form.get("dex"),
                                   int=request.form.get("int"), wis=request.form.get("wis"),
                                   cha=request.form.get("cha"), player_character=True, creator_id=user_id)
        else:
            character = Characters(character_name=request.form.get("character_name"), world_id=world_id, creator_id=user_id, description=request.form.get("description"),
                                   str=request.form.get("str"), con=request.form.get("con"), dex=request.form.get("dex"),
                                   int=request.form.get("int"), wis=request.form.get("wis"), cha=request.form.get("cha"))
        db.session.add(character)
        db.session.commit()

        return redirect(url_for('world', world_id=world_id))


@app.route('/new_location/<world_id>', methods=["POST", "GET"])
def new_location(world_id):
    if request.method == "GET":
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))
        return render_template("new_location.html")

    if request.method == "POST":
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        location = Locations(location_name=request.form.get("location_name"), world_id=world_id, description=request.form.get("description"),
                             creator_id=session["id"])
        db.session.add(location)
        db.session.commit()

        return redirect(url_for('world', world_id=world_id))



@app.route('/world/<world_id>')
def world(world_id):
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    world = World.query.filter_by(id=world_id).first()
    locations = Locations.query.filter_by(world_id=world_id).all()
    characters = Characters.query.filter_by(world_id=world_id).all()
    users = User.query.all()

    return render_template("/world.html", world=world, locations=locations, characters=characters, users=users)


@app.route('/location/<location_id>')
def location(location_id):
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    location = Locations.query.filter_by(id=location_id).first()
    notes = Notes.query.filter_by(location_id=location_id).all()
    world = World.query.filter_by(id=location.world_id).first()



    return render_template("location.html", location=location, notes=notes, world=world)


@app.route('/character/<character_id>')
def character(character_id):
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    character = Characters.query.filter_by(id=character_id).first()
    owner = None

    if character.player_character:
        owner = User.query.filter_by(user_id=character.player_id).first()

    notes = Notes.query.filter_by(character_id=character_id).all()
    world = World.query.filter_by(id=character.world_id).first()

    return render_template("character.html", character=character, notes=notes, owner=owner, world=world)



@app.route('/create_note', methods=["POST"])
def create_note():
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    note_text = request.json
    user_id = session["id"]

    if note_text[1] == 'location':
        note = Notes(world_id=note_text[2], creator_id=user_id, text=note_text[0], location_id=note_text[3])

    elif note_text[1] == 'character':
        note = Notes(world_id=note_text[2], creator_id=user_id, text=note_text[0], character_id=note_text[3])

    if not note:
        return json.dumps(False)

    else:

        db.session.add(note)
        db.session.commit()

    return jsonify(note_text[0])

@app.route('/add_players', methods=["POST"])
def add_players():
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    players = request.form.getlist('players')
    world_id = request.form.get('world_id')

    for player in players:
        new_player = User_world_connector(user_id=player, world_id=world_id)
        db.session.add(new_player)
        db.session.commit()

    locations = Locations.query.filter_by(world_id=world_id).all()
    characters = Characters.query.filter_by(world_id=world_id).all()
    users = User.query.all()


    return redirect(f"/world/{world_id}")


@app.route('/search/', methods=["GET", "POST"])
def search():
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    query = request.args.get('search')
    query = "%{}%".format(query)

    location_results = Locations.query.filter(Locations.location_name.like(query))
    character_results = Characters.query.filter(Characters.character_name.like(query))
    world_results = World.query.filter(World.name.like(query))
    note_results = Notes.query.filter(Notes.text.like(query))

    return render_template("search.html", location_results=location_results, character_results=character_results,
                    world_results=world_results, note_results=note_results)


