from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash



def login(username, password):
    sql = "SELECT id, username, password, isteacher FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user==None:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["isteacher"] = user.isteacher
        return True
    
    return False
        
    
    

def register(firstname, lastname, password, username, isteacher):
    sql = "SELECT 1 FROM users WHERE username=:username" # check if username is already in use
    result = db.session.execute(sql, {"username":username})
    if result.fetchone():
        return False

    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (firstname, lastname, password, username, isteacher) VALUES (:firstname, :lastname, :password, :username, :isteacher)"
    db.session.execute(sql, {"firstname":firstname, "lastname":lastname, "password":hash_value, "username":username, "isteacher":isteacher})
    db.session.commit()
    return True


def logout():
    del session["user_id"]
    del session["username"]
    del session["isteacher"]

def create_course(name, description):
    print()


    #aux functions

def user_id():
    return session.get("user_id",0)

def username():
    return session.get("username",0)

def isteacher():
    return session.get("isteacher",0)

