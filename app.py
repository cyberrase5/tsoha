from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("createMulCho.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/createCourse")
def createCourse():
    return render_template("createCourse.html")

@app.route("/createC", methods=["POST"])
def createC():
    name=request.form["name"]
    sql = "INSERT INTO courses (coursename, teacher_id, taskcount) VALUES (:name, 4, 0)"
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return render_template("createC.html", name=name)

@app.route("/course/<int:id>")
def course(id):
    sql = "SELECT coursename FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    coursename = result.fetchone()[0]
    sql = "SELECT U.firstname FROM courses C, users U WHERE C.id=:id AND U.id=C.teacher_id"
    result = db.session.execute(sql, {"id":id})
    firstname = result.fetchone()[0]
    sql = "SELECT U.lastname FROM courses C, users U WHERE C.id=:id AND U.id=C.teacher_id"
    result = db.session.execute(sql, {"id":id})
    lastname = result.fetchone()[0]
    return render_template("course.html", coursename=coursename, fname=firstname, lname=lastname)