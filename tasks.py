from db import db
from flask import session

import users, courses

def create_text(course_id, week, content):
    sql = "INSERT INTO texts (course_id, content, week) VALUES (:cid, :content, :week)"
    db.session.execute(sql, {"cid":course_id, "content":content, "week":week})
    db.session.commit()

def week_texts(course_id, week):
    sql = "SELECT content FROM texts WHERE course_id=:course_id AND week=:week"
    result = db.session.execute(sql, {"course_id":course_id, "week":week})
    return result.fetchall()

def create_QA(id, question, answer, points, tries, week): # type 0 = question and answer task
    sql = "INSERT INTO tasks (course_id, question, correctanswer, maxpoints, max_tries, week, type) VALUES (:id, :question, :answer, :points, :tries, :week, 0)"
    db.session.execute(sql, {"id":id, "question":question, "answer":answer, "points":points, "tries":tries, "week":week})
    db.session.commit()

def create_MultipleChoice(id, question, answer, points, tries, week): # type 0 = question and answer task
    sql = "INSERT INTO tasks (course_id, question, correctanswer, maxpoints, max_tries, week, type) VALUES (:id, :question, :answer, :points, :tries, :week, 0)"
    db.session.execute(sql, {"id":id, "question":question, "answer":answer, "points":points, "tries":tries, "week":week})
    db.session.commit()

def add_choices():
    print()