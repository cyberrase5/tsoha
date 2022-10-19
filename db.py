'''database connection'''
from os import getenv
from flask_sqlalchemy import SQLAlchemy

from app import app

DB_URI = getenv("DATABASE_URL")  # or other relevant config var
if DB_URI.startswith("postgres://"):
    DB_URI = DB_URI.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
