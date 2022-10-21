'''database config '''
from os import getenv
from flask_sqlalchemy import SQLAlchemy

from app import app

db_uri = getenv("DATABASE_URL")  # or other relevant config var
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
