from flask import render_template, request, redirect
from app import app
import users
import rooms


@app.route("/")
def index():
    room_list = rooms.get_rooms()
    return render_template("index.html", rooms=room_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Wrong username or password!")
    return render_template("login.html")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords did not match!")
        if users.register(username, password1):
            return redirect("/")
        return render_template("error.html", message="Failed to register!")
    return render_template("register.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        room_name = request.form["room_name"]
        if users.add_room(room_name):
            return redirect("/")
        return render_template("error.html", message="Failed to create room!")
    return render_template("create.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        room_name = request.form["room_name"]
        if users.join_room(room_name):
            return redirect("/")
        return render_template("error.html", message="Failed to join room!")
    return render_template("join.html")


@app.route("/rooms/<room_id>/", methods=["GET", "POST"])
def view_room(room_id):
    if users.is_member(room_id):
        users.set_room_id(room_id)
        room = rooms.get_room(room_id)
        messages = rooms.get_messages(room_id)
        members = rooms.get_members(room_id)
        return render_template("room.html", room=room, messages=messages, members=members)
    return render_template("error.html", message="You have no access to this chat!")


@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if users.send_message(content):
        return redirect("/rooms/" + users.get_room_id() + "/")
    return render_template("error.html", message="Failed to send a message!")
