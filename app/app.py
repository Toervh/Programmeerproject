from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from models import *

app = Flask(__name__)



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
    description = db.Column(db.text(500))
    creator_name = db.Column(Integer)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")


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
        db.session.commit()

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
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect("/login")
        return redirect("/")

@app.route('/create_new', methods=["POST", "GET"])
def create_new():
    if request.method == "GET":
        return render_template("create_new.html")

    if request.method == "POST":
        world_name = request.form.get("name")
        world_description = request.form.get("description")
        if len(world_description) > 500:
            flash('Max amount of words exceeded.')
            return redirect('/create_new')
        else:
            world = World(name=world_name, description=world_description, creator_name=session["user_name"])

@app.route('/worlds')
def worlds():
    list_worlds = []
    for worlds in World:
        if worlds.creator_name == session["user_name"]:
            list_worlds.append(world)
    return render_template('worlds', worlds=list_worlds)

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session["user_name"] = None
    return redirect("/")

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)