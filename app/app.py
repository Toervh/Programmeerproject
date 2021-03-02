from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
#from models import User, World, Location_character, Notes, User_Worlds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite////tmp/test.db'
db = SQLAlchemy(app)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/header")
def header():
    return render_template("header.html")

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == "GET":
#         return render_template("register.html")
#
#     if request.method == "POST":
#         try:
#             username = request.form.get("username")
#             password = request.form.get("password")
#
#             db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
#                        {"username": username, "password": password})
#             db.commit()
#             return render_template("index.html")
#
#
#
#
# @app.route('/login', methods=["POST", "GET"])
# def login():
#     if request.method == "GET":
#         return render_template("login.html")
#
#     if request.method == "POST":
#         try:
#             username = request.form.get("username")
#             password = request.form.get("password")
#
#             res = db.execute("SELECT id, password FROM users WHERE username LIKE :username",
#                              {"username": username}).fetchone()
#             # db_hash = res.password
#             user_id = res.id
#
#             if not res:
#                 return render_template("error.html")
#             else:
#                 session["logged_in"] = True
#                 session["user_id"] = user_id
#                 session["user_name"] = username
#                 return redirect(url_for('index'))
#         except ValueError:
#             return render_template("error.html", message="Login failed. Please try again.")
#
#
# @app.route('/logout')
# def logout():
#     session["logged_in"] = False
#     session["user_id"] = None
#     return redirect(url_for('index'))

if __name__ == '__main__':
    #db.init_app(app)
    app.run()