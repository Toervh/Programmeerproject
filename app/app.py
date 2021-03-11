from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from models import *

app = Flask(__name__)


# TODO
# Setup for Email server.
# app.config["MAIL_DEFAULT_SENDER"] = "toervanholstein@gmail.com"
# app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_SERVER"] = smtp.gmail.com
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
# mail = Mail(app)

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
    # creator_id = Column(Integer, ForeignKey('user.id'))

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

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session["user_name"] = None
    return redirect("/")

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)