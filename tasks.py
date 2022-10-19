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

def QA_tasks(id, week, user_id): # type 0
    sql = "SELECT T.id, T.question, T.correctanswer, T.maxpoints, T.max_tries, S.tries, S.points  "\
        "FROM tasks T, submissions S WHERE T.course_id=:id AND T.week=:week AND T.type=0 AND S.task_id=T.id AND S.user_id=:uid"
    result = db.session.execute(sql, {"id":id, "week":week, "uid":user_id})
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
    list = courses.participants_ids(course_id)

    for id in list:
        sql = "INSERT INTO submissions (course_id, user_id, task_id, tries, points) VALUES (:cid, :uid, :tid, 0, 0)"
        db.session.execute(sql, {"cid":course_id, "uid":id[0], "tid":task_id})

    db.session.commit()

def correct_answer(id):
    sql = "SELECT correctanswer FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def add_submission_try(task_id, user_id):
    sql = "UPDATE submissions SET tries=tries+1 WHERE task_id=:task_id AND user_id=:user_id"
    db.session.execute(sql, {"task_id":task_id, "user_id":user_id})
    db.session.commit()

def update_points(task_id, user_id, points):
    sql = "UPDATE submissions SET points=:points WHERE task_id=:task_id AND user_id=:user_id"
    db.session.execute(sql, {"points":points, "task_id":task_id, "user_id":user_id})
    db.session.commit()

def MC_tasks(course_id, week, user_id): # type 1
    sql = "SELECT T.id, C.id, T.question, T.maxpoints, T.max_tries, C.choice, S.tries, S.points, T.week FROM tasks T, choices C, submissions S "\
        "WHERE T.course_id=:id AND T.id=C.task_id AND T.week=:week AND S.task_id=T.id AND S.user_id=:user_id AND T.type=1 ORDER BY C.id"
    result = db.session.execute(sql, {"id":course_id, "week":week, "user_id":user_id})
    return result.fetchall()

def choice_text(id):
    sql = "SELECT choice FROM choices WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]