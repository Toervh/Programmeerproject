from flask import Flask, session, redirect, url_for, render_template, request, flash, jsonify
from flask_login import LoginManager, UserMixin, logout_user, login_user, current_user
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Login manager
login = LoginManager(app)

# Database Configuration
app.config['UPLOAD_FOLDER'] = '/doc/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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

class World(db.Model):
    __tablename__ = 'worlds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(500))
    creator_name = db.Column(db.String(80))

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)
    text = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    location_id = db.Column(db.Integer)
    character_id = db.Column(db.Integer)

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100))
    world_id = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(80))
    world_id = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    str = db.Column(db.Integer)
    con = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    int = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    cha = db.Column(db.Integer)
    player_character = db.Column(db.Boolean)
    player_id = db.Column(db.Integer, nullable=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
def index():
    if not session.get("user_name"):
        return redirect("/login")

    username = session.get("user_name")

    worlds = World.query.filter_by(creator_name=username).all()
    # if not worlds:
    #     return render_template("index.html")
    for world in worlds:
        print(world)
    return render_template("index.html", worlds=worlds)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        user = User(username=username, password=password, email=email)
        db.session.add(user)

        try:
            db.session.commit()
        except:
            flash('Username already in use.')
            return redirect('/register')

        return render_template("registered.html")



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session.get("name"):
            return redirect("/index.html", message="You are already logged in.")
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Incorrect username or password. Please try again.')
            return redirect("/login")
        if user.password == password:
            session["logged_in"] = True
            session["user_name"] = username
            session["id"] = user.id
            db.session.commit()
            login_user(user)
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect("/login")

        return redirect("/")

@app.route('/profile/<user_id>', methods=["GET"])
def profile(user_id):

    user = User.query.filter_by(id=user_id).first()
    all_notes = Notes.query.filter_by(creator_id=user.id).all()

    return render_template("profile.html", user=user, notes=all_notes)

@app.route('/new_world', methods=["POST", "GET"])
def new_world():
    if request.method == "GET":
        if not session.get("user_name"):
            return redirect("/login")

        return render_template("new_world.html")

    if request.method == "POST":
        if not session.get("user_name"):
            return redirect("/login")

        world_name = request.form.get("world_name")
        world_description = request.form.get("description")

        ##TODO file upload
        # file = request.files['file']
        # file = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if len(world_description) > 500:
            flash('Max amount of words exceeded.')
            return redirect('/new_world')
        else:
            world = World(name=world_name, description=world_description, creator_name=session["user_name"])
            world_id = world.id
            flash("world created")
            db.session.add(world)
            db.session.commit()
        return redirect("/")


@app.route('/new_character/<world_id>', methods=["POST", "GET"])
def new_character(world_id):
    if request.method == "GET":
        if not session.get("user_name"):
            return redirect("/login")
        return render_template("new_character.html")

    if request.method == "POST":
        if not session.get("user_name"):
            return redirect("/login")

        pc = request.form.get("PC")
        character_name = request.form.get("character_name")
        print(f"form get character name: {character_name}")
        print(f"form get PC: {pc}")

        if request.form.get("PC") == "PC":
            user_id = session["id"]
            character = Characters(character_name=request.form.get("character_name"), world_id=world_id,
                                   description=request.form.get("description"),
                                   str=request.form.get("str"), con=request.form.get("con"),
                                   dex=request.form.get("dex"),
                                   int=request.form.get("int"), wis=request.form.get("wis"),
                                   cha=request.form.get("cha"), player_character=True, creator_id=user_id)
        else:
            character = Characters(character_name=request.form.get("character_name"), world_id=world_id, description=request.form.get("description"),
                                   str=request.form.get("str"), con=request.form.get("con"), dex=request.form.get("dex"),
                                   int=request.form.get("int"), wis=request.form.get("wis"), cha=request.form.get("cha"))
        db.session.add(character)
        db.session.commit()

        return redirect('/')


@app.route('/new_location/<world_id>', methods=["POST", "GET"])
def new_location(world_id):
    if request.method == "GET":
        if not session.get("user_name"):
            return redirect("/login")
        return render_template("new_location.html")

    if request.method == "POST":
        if not session.get("user_name"):
            return redirect("/login")

        location = Locations(location_name=request.form.get("location_name"), world_id=world_id, description=request.form.get("description"))
        db.session.add(location)
        db.session.commit()

        return redirect('/')

#         ##TODO file upload
#         # file = request.files['file']
#         # file = secure_filename(file.filename)
#         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))



@app.route('/world/<world_id>')
def world(world_id):
    if not session.get("user_name"):
        return redirect("/login")

    world = World.query.filter_by(id=world_id).first()
    locations = Locations.query.filter_by(world_id=world_id).all()
    characters = Characters.query.filter_by(world_id=world_id).all()

    return render_template("/world.html", world=world, locations=locations, characters=characters)

@app.route('/location/<location_id>')
def location(location_id):
    if not session.get("user_name"):
        return redirect("/login")

    location = Locations.query.filter_by(id=location_id).first()
    notes = Notes.query.filter_by(location_id=location_id).all()
    world = World.query.filter_by(id=location.world_id).first()



    return render_template("location.html", location=location, notes=notes, world=world)


@app.route('/character/<character_id>')
def character(character_id):
    if not session.get("user_name"):
        return redirect("/login")

    character = Characters.query.filter_by(id=character_id).first()
    owner = None
    if character.player_character:
        owner = User.query.filter_by(user_id=character.player_id)

    notes = Notes.query.filter_by(character_id=character_id).all()
    world = World.query.filter_by(id=character.world_id)

    print(f"Name: {character.character_name}")
    print(f"description: {character.description}")
    print(character.player_character)
    print(f"player id: {character.player_id}")
    print(character.creation_date)


    return render_template("character.html", character=character, notes=notes, owner=owner, world=world)


@app.route('/create_note', methods=["POST"])
def create_note():

    note_text = request.json
    print(note_text)
    print(note_text[0])
    print(note_text[1])
    print(note_text[2])
    print(note_text[3])
    user_id = session["id"]

    if note_text[1] == 'location':
        note = Notes(world_id=note_text[2], creator_id=user_id, text=note_text[0], location_id=note_text[3])

    if note_text[1] == 'character':
        note = Notes(world_id=note_text[2], creator_id=user_id, text=note_text[0], character_id=note_text[3])

    if not note:
        return json.dumps(False)

    else:

        db.session.add(note)
        db.session.commit()

    return jsonify(note_text)

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session["user_name"] = None
    logout_user()
    return redirect("/")

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)