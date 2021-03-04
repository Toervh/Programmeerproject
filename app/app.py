import os
from flask import Flask, session, redirect, url_for, render_template, request
#TODO
#ask how to import flask session
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
#TODO
#setup flask session

# TODO
# Setup for Email server.
# app.config["MAIL_DEFAULT_SENDER"] = "toervanholstein@gmail.com"
# app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_SERVER"] = smtp.gmail.com
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
# mail = Mail(app)

#TODO
#find out what link to use to connect database and to view it.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite////tmp/test.db'

#TODO
#is this the right way to initialize SQLAlchemy?
db = SQLAlchemy(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    #TODO
    #Find out how to check input and created users.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        #TODO
        #insert into database
        # db.execute("INSERT INTO users(username, password, email) VALUES (:username, :password, :email)",
        #            {"username": username, "password": password, "email": email})
        # db.commit()
        #TODO
        #Implement mailing the user that the registration was succesfull.
        # message = Message("Thank you for registering!", recipients=[email])
        # mail.send(message)
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
        # res = db.execute("SELECT id, password FROM users WHERE username LIKE :username",
        #                  {"username": username}).fetchone()
        # user_id = res.id
        # if not res:
        #     return render_template("error.html", message="Login unsuccesfull. Please try again.")
        # else:
        session["logged_in"] = True
        # session["user_id"] = user_id
        session["user_name"] = username
        session["logged_in"] = True
        return render_template("index.html")

# @app.route('/world/<world_id>')
# def world(world_id):
#     if not session.get(logged_in):
#         redirect(url_for('login'))
#     else:
#         res = db.execute("SELECT * FROM worlds WHERE id = :world_id",
#                         {"world_id": world_id}).fetchone()

@app.route('/logout')
def logout():
    # session["logged_in"] = False
    # session["user_id"] = None
    return "TODO"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)