from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash



def login(username, password):
    print()

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
    print()
