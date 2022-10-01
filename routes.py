from dataclasses import asdict
from app import app
from flask import render_template, request, redirect
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana (todennäköisesti")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        username=request.form["username"]
        password = request.form["password"]
        role=int(request.form["type"])
        pos = "opiskelija"
        bool = False
        if role == 1:
            pos = "opettaja"
            bool = True

        if users.register(firstname, lastname, password, username, bool):
            return render_template("reg.html", fname=firstname, lname=lastname, uname=username, role=pos)
        else:
            return render_template("error.html", message="Rekisteröityminen epäonnistui, käyttäjänimi todennäköisesti jo käytössä")

@app.route("/logout")
def logout():
    return redirect("/")

@app.route("/error")
def error():
    return render_template("error.html")

