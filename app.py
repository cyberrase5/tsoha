from crypt import methods
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/reg", methods=(["POST"]))
def reg():
    fname=request.form["firstname"]
    lname=request.form["lastname"]
    uname=request.form["username"]
    password = request.form["password"]
    role=int(request.form["type"])
    pos = "opiskelija"
    bool = False
    if role == 1:
        pos = "opettaja"
        bool = True
    
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (firstname, lastname, password, isteacher, username) VALUES (:firstname, :lastname, :password, :isteacher, :username)"
    db.session.execute(sql, {"firstname":fname, "lastname":lname, "password":hash_value, "isteacher":bool, "username":uname})
    db.session.commit()


    return render_template("reg.html", fname=fname, lname=lname, uname=uname, role=pos)

@app.route("/createMulCho/<int:id>")
def createMulCho(id):
    return render_template("createMulCho.html")

@app.route("/createMC", methods=(["POST"]))
def createCourse():
    return render_template("createMC.html")

#@app.route("/createCourse")
#def createCourse():
#    return render_template("createCourse.html")

@app.route("/createC", methods=(["POST"]))
def createC():
    name=request.form["name"]
    sql = "INSERT INTO courses (coursename, teacher_id, taskcount) VALUES (:name, 1, 0)"
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
    return render_template("course.html", coursename=coursename, fname=firstname, lname=lastname, id=id)


@app.route("/error")
def error():
    return render_template("error.html")