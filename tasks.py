from db import db
from flask import session

import users, courses

def createText(course_id, week, content):
    sql = "INSERT INTO texts (course_id, content, week) VALUES (:cid, :content, :week)"
    db.session.execute(sql, {"cid":course_id, "content":content, "week":week})
    db.session.commit()

def week_texts(course_id, week):
    sql = "SELECT content FROM texts WHERE course_id=:course_id AND week=:week"
    result = db.session.execute(sql, {"course_id":course_id, "week":week})
    return result.fetchall()