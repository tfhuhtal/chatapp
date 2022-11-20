'''module for site routes'''

from app import app
from flask import render_template, request, redirect
import users, rooms

@app.route("/")
def index():
    '''home page'''

    list = rooms.get_rooms()
    return render_template("index.html", rooms=list)


@app.route("/login", methods=["GET", "POST"])
def login():
    '''login page'''

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password!")


@app.route("/logout")
def logout():
    '''logout page'''

    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    '''register page'''

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords did not match!")

        if users.register(username, password1):
            return redirect("/")

        else:
            return render_template("error.html", message="Failed to register!")

 
@app.route("/create", methods=["GET", "POST"])
def create():
    '''create room page'''

    if request.method == "GET":
        return render_template("create.html")

    if request.method == "POST":
        room_name = request.form["room_name"]

        if users.add_room(room_name):
            return redirect("/")
        
        else:
            return render_template("error.html", message="Failed to create room!")


@app.route("/join", methods=["GET", "POST"])
def join():
    '''joins new room if possible'''

    if request.method == "GET":
        return render_template("join.html")
    
    if request.method == "POST":
        room_name = request.form["room_name"]
        if users.join_room(room_name):
            return redirect("/")
        else:
            return render_template("error.html", message="Failed to join room!")