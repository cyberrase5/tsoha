from db import db
from flask import session

import users

def course(id):
    sql = "SELECT coursename, description FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def join_course(course_id, user_id):
    if users.is_enrolled(course_id, user_id):
        return

    sql = "INSERT INTO participants (course_id, user_id) VALUES (:c_id, :u_id)"
    db.session.execute(sql, {"c_id":course_id, "u_id":user_id})
    db.session.commit()

def create_course(name, description):
    sql = "SELECT 1 FROM courses WHERE coursename=:name"
    result = db.session.execute(sql, {"name":name})
    if result.fetchone():
        return False

    sql = "INSERT INTO courses (coursename, teacher_id, description) VALUES (:name, :id, :text) RETURNING id"
    result = db.session.execute(sql, {"name":name, "id":users.user_id(), "text":description})
    db.session.commit()
    join_course(result.fetchone()[0], users.user_id())

    return True


def list_courses(flag): # flag 0 = my courses, 1 = all courses
    id = users.user_id()
    if (flag == 0):
        sql = "SELECT C.id, C.coursename FROM courses C, participants P WHERE C.id=P.course_id AND P.user_id=:id"
        result = db.session.execute(sql, {"id":id})
        print()
    if (flag == 1):
        result = db.session.execute("SELECT id, coursename FROM courses")

    return result.fetchall()

def week_texts(week):
    print()


def week_taskts(week):
    print()

def course_name(course_id):
    sql = "SELECT coursename FROM courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()[0]