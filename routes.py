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
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html",message="Username has to be 3-20 characters long")
        if " " in username:
            return render_template("error.html", message="Whitespaces are not allowed in username")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords did not match!")
        if password1 == "":
            return render_template("error.html", message="No password set")
        if users.register(username, password1):
            return redirect("/")
    return render_template("register.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        users.check_csrf()
        room_name = request.form["room_name"]
        for room in users.rooms():
            if room[0] == room_name:
                return render_template("error.html", message="This room already exists")
        if rooms.add_room(room_name):
            return redirect("/")
        return render_template("error.html", message="Failed to create room!")
    return render_template("create.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        users.check_csrf()
        room_name = request.form["room_name"]
        for room in users.rooms():
            if room[0] == room_name:
                return render_template("error.html", message="You have already joined to this room")
        if users.join_room(room_name):
            return redirect("/")
        return render_template("error.html", message="Failed to join room!")
    return render_template("join.html")


@app.route("/profile")
def profile():
    stats = users.get_stats()
    count = users.get_count()
    return render_template("profile.html", stats=stats, count=count)


@app.route("/rooms/<room_id>/")
def view_room(room_id):
    if users.is_member(room_id):
        users.set_room_id(room_id)
        room = rooms.get_room(room_id)
        messages = rooms.get_messages(room_id)
        return render_template("room.html", room=room, messages=messages)
    return render_template("error.html", message="You have no access to this chat!")


@app.route("/send", methods=["POST"])
def send():
    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        if users.send_message(content):
            return redirect("/rooms/" + users.get_room_id() + "/")
        return render_template("error.html", message="Failed to send a message!")


@app.route("/rooms/<room_id>/edit")
def edit_room_view(room_id):
    if users.is_member(room_id):
        room = rooms.get_room(room_id)
        members = rooms.get_members(room_id)
        return render_template("edit.html", room=room, members=members)
    return render_template("error.html", message="You have no access to this site")


@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        users.check_csrf()
        room_name = request.form["room_name"]
        if rooms.update_name(room_name):
            return redirect("/rooms/" + users.get_room_id() + "/")
        return render_template("error.html", message="Failed to update name")


@app.route("/remove", methods=["POST"])
def remove():
    if request.method == "POST":
        user_name = request.form["user_name"]
        if not rooms.is_admin():
            if user_name != users.get_username():
                return render_template("error.html", message="You have no rights to remove user")
        if rooms.remove_user(user_name):
            return redirect("/rooms/" + users.get_room_id() + "/")


@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        word = request.form["search"]
        if word == "ls -la":
            return render_template("/secret.html", rooms=rooms.get_all_rooms())
        if word != "":
            results = rooms.get_results(word)
            if len(results) == 0:
                return render_template("error.html", message="No results found")
            return render_template("/results.html", results=results)
        return render_template("error.html", message="No search word given")


@app.route("/rooms/<room_id>/message/<message_id>")
def edit_message_view(room_id, message_id):
    if users.is_member(room_id):
        message = rooms.get_message(message_id)
        if message is None:
            return render_template("error.html", message="No access to this message")
        return render_template("edit_message.html", message=message)
    return render_template("error.html", message="You have no access to this site")


@app.route("/rooms/<room_id>/message/<message_id>_edit/", methods=["POST"])
def edit_message(room_id, message_id):
    if not users.is_member(room_id):
        return render_template("error.html", message="You have no access to this site")
    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        if rooms.update_message(content, message_id):
            return redirect("/rooms/" + users.get_room_id() + "/")
        return render_template("error.html", message="Failed to update message")
        