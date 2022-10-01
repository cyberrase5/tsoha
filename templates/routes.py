from app import app
from flask import render_template, request, redirect
import users

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Ei onni")
