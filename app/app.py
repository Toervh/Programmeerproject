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
    # Check if the user is logged in.
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
        # Render the form for user.
        return render_template("register.html")

    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Hash the password for storage in database
        hashed_password = generate_password_hash(password)

        # Try to create user row.
        try:
            user = User(username=username, password=hashed_password, email=email)
            db.session.add(user)
            db.session.commit()

            # Log the user in.
            session["logged_in"] = True
            session["user_name"] = username
            session["id"] = user.id
            db.session.commit()
            login_user(user)

        # If unsuccessfull: flash message to user.
        except:
            flash('Username already in use.')
            return redirect('/register')


        return render_template("registered.html")



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        # Check if the user is logged in.
        if session.get("user_name"):

            # User cant visit login page when they are already logged in.
            flash('You are already logged in.')
            return redirect(url_for('index'))
        return render_template("login.html")

    if request.method == "POST":

        # Get form data.
        username = request.form.get("username")
        password = request.form.get("password")

        # Find user in database.
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Incorrect username or password. Please try again.')
            return redirect(url_for('login'))

        # Checking hashed password
        result = check_password_hash(user.password, password)

        # If password was incorrect: flash this to user.
        if result is False:
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))

        # If password was correct, log the user in and reroute them to index.
        else:
            session["logged_in"] = True
            session["user_name"] = username
            session["id"] = user.id
            db.session.commit()
            login_user(user)

            return redirect(url_for('index'))

        return redirect(url_for('index'))

@app.route('/profile/<user_id>', methods=["GET"])
def profile(user_id):
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # Check so a user can only view their own profile page. Future updates will change this.
    if int(session["id"]) is not int(user_id):
        flash('For now, you cannot visit other peoples userpage.')
        return redirect(url_for('index'))

    # Log all the users notes.
    user = User.query.filter_by(id=user_id).first()
    all_notes = Notes.query.filter_by(creator_id=user.id).all()

    return render_template("profile.html", user=user, notes=all_notes)



@app.route('/new_world', methods=["POST", "GET"])
def new_world():
    if request.method == "GET":
        # Check if the user is logged in.
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))


        return render_template("new_world.html")

    if request.method == "POST":
        # Check if the user is logged in.
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        # Get form info
        world_name = request.form.get("world_name")
        world_description = request.form.get("description")

        # Check if description isnt too long.
        if len(world_description) > 500:
            flash('Max amount of words exceeded.')
            return redirect('/new_world')

        # Proceed to create world and add it to the database.
        else:
            world = World(name=world_name, description=world_description, creator_id=session["id"])
            world_id = world.id
            db.session.add(world)
            db.session.commit()

            # Let user know world was created.
            flash("world created")


        return redirect("/")


@app.route('/new_character/<world_id>', methods=["POST", "GET"])
def new_character(world_id):
    if request.method == "GET":
        # Check if the user is logged in.
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        return render_template("new_character.html", world_id=world_id)

    if request.method == "POST":
        # Check if the user is logged in.
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        # Get information from the form.
        pc = request.form.get("PC")
        character_name = request.form.get("character_name")

        # Get user id.
        user_id = session["id"]

        # If the PC button was clicked, create a player avatar. Essentially a character but the creator is the owner of this character.
        if request.form.get("PC") == "PC":
            character = Characters(character_name=request.form.get("character_name"), world_id=world_id,
                                   description=request.form.get("description"),
                                   str=request.form.get("str"), con=request.form.get("con"),
                                   dex=request.form.get("dex"),
                                   int=request.form.get("int"), wis=request.form.get("wis"),
                                   cha=request.form.get("cha"), player_character=True, creator_id=user_id)

        # Create the character but without the Player_character set to True.
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
        # Check if the user is logged in.
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        return render_template("new_location.html")

    if request.method == "POST":
        # Check if the user is logged in.
        if not session.get("user_name"):
            flash('You are not logged in.')
            return redirect(url_for('login'))

        # Create a new location with info from the form and add it to the database.
        location = Locations(location_name=request.form.get("location_name"), world_id=world_id, description=request.form.get("description"),
                             creator_id=session["id"])
        db.session.add(location)
        db.session.commit()

        return redirect(url_for('world', world_id=world_id))



@app.route('/world/<world_id>')
def world(world_id):
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # get the world row, all locations attached and all characters.
    world = World.query.filter_by(id=world_id).first()
    locations = Locations.query.filter_by(world_id=world_id).all()
    characters = Characters.query.filter_by(world_id=world_id).all()

    # Query all users so the current user can add them.
    users = User.query.all()

    return render_template("/world.html", world=world, locations=locations, characters=characters, users=users)

@app.route('/location/<location_id>')
def location(location_id):
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # Query the location and all notes at this location.
    location = Locations.query.filter_by(id=location_id).first()
    notes = Notes.query.filter_by(location_id=location_id).all()

    # Query the world for linking within the html.
    world = World.query.filter_by(id=location.world_id).first()

    return render_template("location.html", location=location, notes=notes, world=world)



@app.route('/character/<character_id>')
def character(character_id):
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # Query the character in question.
    character = Characters.query.filter_by(id=character_id).first()

    # Setting owner to none otherwise it breaks the site.
    owner = None

    # Get the id of the owner of this character.
    if character.player_character:
        owner = User.query.filter_by(user_id=character.player_id).first()

    # Query all notes for this character.
    notes = Notes.query.filter_by(character_id=character_id).all()

    # Query the world for linking within the html.
    world = World.query.filter_by(id=character.world_id).first()

    return render_template("character.html", character=character, notes=notes, owner=owner, world=world)



@app.route('/create_note', methods=["POST"])
def create_note():
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # Get the information sent.
    note_text = request.json

    # Get user id.
    user_id = session["id"]

    # If the note in question was placed at a location add it as a location note.
    if note_text[1] == 'location':
        note = Notes(world_id=note_text[2], creator_id=user_id, text=note_text[0], location_id=note_text[3])

    # If the note in question was placed at a character; add it as a character note.
    if note_text[1] == 'character':
        note = Notes(world_id=note_text[2], creator_id=user_id, text=note_text[0], character_id=note_text[3])

    # If something went wrong, return False.
    if not note:
        return json.dumps(False)

    else:

        db.session.add(note)
        db.session.commit()

    return jsonify(note_text[0])

@app.route('/add_players', methods=["POST"])
def add_players():
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # Get the multiple form data. This becomes a list.
    players = request.form.getlist('players')
    world_id = request.form.get('world_id')

    # For every player in the list add a connection to the database.
    for player in players:
        new_player = User_world_connector(user_id=player, world_id=world_id)
        db.session.add(new_player)
        db.session.commit()

    # Query all locations and characters for linking back to the world page.
    locations = Locations.query.filter_by(world_id=world_id).all()
    characters = Characters.query.filter_by(world_id=world_id).all()
    users = User.query.all()


    return redirect(f"/world/{world_id}")


@app.route('/search/', methods=["GET", "POST"])
def search():
    # Check if the user is logged in.
    if not session.get("user_name"):
        flash('You are not logged in.')
        return redirect(url_for('login'))

    # Get the form data and format it.
    query = request.args.get('search')
    query = "%{}%".format(query)

    # Query for all results in all databases.
    location_results = Locations.query.filter(Locations.location_name.like(query))
    character_results = Characters.query.filter(Characters.character_name.like(query))
    world_results = World.query.filter(World.name.like(query))
    note_results = Notes.query.filter(Notes.text.like(query))

    return render_template("search.html", location_results=location_results, character_results=character_results,
                    world_results=world_results, note_results=note_results)


@app.route('/logout')
def logout():

    # Log the user out.
    session["logged_in"] = False
    session["user_name"] = None
    logout_user()
    return redirect("/")

