from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = '/doc/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

Migrate(app, db)

class User(db.Model):
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
    text = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100))
    world_id = db.Column(db.Integer)
    description = db.Column(db.String(500))
    # creation_date = db.Column

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer)
    description = db.Column(db.String(500))
    # creation_date = db.Column()
    str = db.Column(db.Integer)
    con = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    int = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    cha = db.Column(db.Integer)
    player_id = db.Column(db.Integer, nullable=True)

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
            db.session.commit()
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect("/login")
        return redirect("/")




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


@app.route('/new_character', methods=["POST", "GET"])
def new_character():
    if request.method == "GET":
        if not session.get("user_name"):
            return redirect("/login")
        return render_template("new_character.html")

    if request.method == "POST":
        if not session.get("user_name"):
            return redirect("/login")

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

        return redirect('/')
#         location_name = request.form.get("location_name")
#         description = request.form.get("description")
#
#         ##TODO let this route know what world it belongs to
#         # world = World.query.filter_by(id=l)
#         ##TODO file upload
#         # file = request.files['file']
#         # file = secure_filename(file.filename)
#         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#         if len(description) > 500:
#             flash('Max amount of words exceeded.')
#             return redirect('/new_location')
#         else:
#             location = Locations(world_id=world.id, location_name=location_name, description=world_description)
#             world_id = world.id
#             flash("world created")
#             db.session.add(world)
#             db.session.commit()
#         return redirect("/")



@app.route('/world/<world_id>')
def world(world_id):
    if not session.get("user_name"):
        return redirect("/login")

    world = World.query.filter_by(id=world_id).first()
    notes = Notes.query.filter_by(world_id=world_id).all()

    return render_template("/world.html", world=world, notes=notes)

@app.route('/location/<location_id>')
def location(location_id):
    if not session.get("user_name"):
        return redirect("/login")

    location = Location.query.filter_by(id=location_id).first()
    notes = Notes.query.filter_by(location_id=location_id).all()

    return render_template("location.html", location=location, notes=notes)

@app.route('/add_note')
def add_note():

    note = Note(world_id=request.form.get("world_id"), text=request.form.get("note_text"))
    session.db.add(note)
    session.db.commit()
    if 'url' in session:
        return redirect(session['url'])
    return redirect("/")

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session["user_name"] = None
    return redirect("/")

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)