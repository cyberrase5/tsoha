'''functions mostly concerning users'''
import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from db import db


def login(username, password):
    '''login, creates session stuff'''
    sql = "SELECT id, username, password, isteacher FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is None:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["isteacher"] = user.isteacher
        session["csrf_token"] = secrets.token_hex(16)
        return True

    return False


def register(firstname, lastname, password, username, isteacher):
    '''register, checks password etc.'''
    sql = "SELECT 1 FROM users WHERE username=:username" # check if username is already in use
    result = db.session.execute(sql, {"username":username})
    if result.fetchone():
        return False

    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (firstname, lastname, password, username, isteacher) "\
        "VALUES (:firstname, :lastname, :password, :username, :isteacher)"
    db.session.execute(sql, {"firstname":firstname, "lastname":lastname,
                             "password":hash_value, "username":username, "isteacher":isteacher})
    db.session.commit()
    return True


def logout():
    '''deletes session stuff'''
    del session["user_id"]
    del session["username"]
    del session["isteacher"]
    del session["csrf_token"]


def is_enrolled(course_id, user_id):
    '''returns true if entry is found in participants'''
    sql = "SELECT 1 FROM participants WHERE course_id=:course_id AND user_id=:user_id"
    result = db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    if result.fetchone():
        return True

    return False


def is_course_teacher(course_id, teacher_id):
    '''returns true if is this course's teacher'''
    sql = "SELECT 1 FROM courses WHERE id=:course_id AND teacher_id=:teacher_id"
    result = db.session.execute(sql, {"course_id":course_id, "teacher_id":teacher_id})
    if result.fetchone():
        return True

    return False


def leave_course(course_id, user_id):
    '''leaves course, deletes entry from participants'''
    sql = "DELETE FROM participants WHERE course_id=:course_id AND user_id=:user_id"
    db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    db.session.commit()


    #aux functions

def user_id():
    '''returns user id from session'''
    return session.get("user_id", 0)

def username():
    '''returns username from session'''
    return session.get("username", 0)

def isteacher():
    '''returns true if teacher from session'''
    return session.get("isteacher", 0)

def teacher_password():
    '''returns hashed correct passphrase'''
    return "pbkdf2:sha256:260000$ahsuNWMlcq4gtzY2"\
        "$69036caf21529f0707f74dacd7f4cb335c6c415fadabdfc9232e4541757ea28a"
    # generated with generate_password_hash("secret_teacher_password")
    # if secret key changes, this needs to be recalculated

def authenticate_teacherness(proof):
    '''compares given phrase to hashed correct phrase'''
    return check_password_hash(teacher_password(), proof)
