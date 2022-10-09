from unittest import result
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
    sql = "INSERT INTO tasks (course_id, question, correctanswer, maxpoints, max_tries, week, type) VALUES (:id, :question, :answer, :points, :tries, :week, 0) RETURNING id"
    result = db.session.execute(sql, {"id":id, "question":question, "answer":answer, "points":points, "tries":tries, "week":week})
    db.session.commit()
    return result.fetchone()[0]

def create_MultipleChoice(id, question, answer, points, tries, week): # type 1 = multiple choice task, returns task id
    sql = "INSERT INTO tasks (course_id, question, correctanswer, maxpoints, max_tries, week, type) VALUES (:id, :question, :answer, :points, :tries, :week, 1) RETURNING id"
    result = db.session.execute(sql, {"id":id, "question":question, "answer":answer, "points":points, "tries":tries, "week":week})
    db.session.commit()
    return result.fetchone()[0]

def add_choices(task_id, list, course_id):
    for choice in list:
        sql = "INSERT INTO choices (task_id, choice, course_id) VALUES (:task_id, :choice, :course_id)"
        db.session.execute(sql, {"task_id":task_id, "choice":choice, "course_id":course_id})

    db.session.commit()

def QA_tasks(id, week): # type 0
    sql = "SELECT question, correctanswer, maxpoints, max_tries FROM tasks WHERE course_id=:id AND week=:week AND type=0"
    result = db.session.execute(sql, {"id":id, "week":week})
    return result.fetchall()

def delete_from_submissions(course_id, user_id):
    sql = "DELETE FROM submissions WHERE course_id=:course_id AND user_id=:user_id"
    db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    db.session.commit()

def course_tasks(course_id):
    sql = "SELECT id FROM tasks where course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()

def add_submissions_old(course_id, user_id):
    list = course_tasks(course_id)

    for id in list:
        sql = "INSERT INTO submissions (course_id, user_id, task_id, tries, points) VALUES (:cid, :uid, :tid, 0, 0)"
        db.session.execute(sql, {"cid":course_id, "uid":user_id, "tid":id[0]})

    db.session.commit()

def add_submissions_new(course_id, task_id):
    list = courses.participants_IDs(course_id)

    for id in list:
        sql = "INSERT INTO submissions (course_id, user_id, task_id, tries, points) VALUES (:cid, :uid, :tid, 0, 0)"
        db.session.execute(sql, {"cid":course_id, "uid":id[0], "tid":task_id})

    db.session.commit()