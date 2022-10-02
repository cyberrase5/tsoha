from db import db
from flask import session

import users

def create_course(name, description):
    sql = "SELECT 1 FROM courses WHERE coursename=:name"
    result = db.session.execute(sql, {"name":name})
    if result.fetchone():
        return False

    
    sql = "INSERT INTO courses (coursename, teacher_id, taskcount) VALUES (:name, :id, 0) RETURNING id"
    result = db.session.execute(sql, {"name":name, "id":users.user_id()})
    sql = "INSERT INTO texts (course_id, content) VALUES (:id, :text)"
    db.session.execute(sql, {"id":result.fetchone()[0], "text":description})
    db.session.commit()

    return True