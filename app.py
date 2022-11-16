'''App'''

from os import getenv
from flask import Flask
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def index():
    '''-'''
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    '''-'''
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login(username, password):
            session["user_name"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password!")

@app.route("/logout")
def logout():
    '''-'''
    del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    '''-'''
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Password didn't match")
        if register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Failed to register")


@app.route("/chats")
def chats():
    return render_template("chats.html")



def login(username, password):
    '''login'''
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False



def register(username, password):
    '''register'''
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    '''returns users id'''
    return session.get("user_id",0)

