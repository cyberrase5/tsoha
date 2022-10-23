'''functions concerning mostly tasks'''
from db import db

import users
import courses

def create_text(course_id, week, content):
    '''creates text for this course this week'''
    sql = "INSERT INTO texts (course_id, content, week) VALUES (:cid, :content, :week)"
    db.session.execute(sql, {"cid":course_id, "content":content, "week":week})
    db.session.commit()


def week_texts(course_id, week):
    '''gets this course's this week's texts'''
    sql = "SELECT content FROM texts WHERE course_id=:course_id AND week=:week"
    result = db.session.execute(sql, {"course_id":course_id, "week":week})
    return result.fetchall()


def create_qa_task(course_id, question, answer, points, tries, week): # type 0 = question and answer task
    '''creates question & answer task'''
    sql = "INSERT INTO tasks (course_id, question, correctanswer, maxpoints, max_tries, week, type) "\
        "VALUES (:id, :question, :answer, :points, :tries, :week, 0) RETURNING id"
    result = db.session.execute(sql, {"id":course_id, "question":question, "answer":answer, "points":points,
                                      "tries":tries, "week":week})
    db.session.commit()
    return result.fetchone()[0]


def create_mc_task(course_id, question, answer, points, tries, week): # type 1 = mc task, returns task id
    '''creates multiple choice task'''
    sql = "INSERT INTO tasks (course_id, question, correctanswer, maxpoints, max_tries, week, type) "\
        "VALUES (:id, :question, :answer, :points, :tries, :week, 1) RETURNING id"
    result = db.session.execute(sql, {"id":course_id, "question":question, "answer":answer,
                                      "points":points, "tries":tries, "week":week})
    db.session.commit()
    return result.fetchone()[0]


def add_choices(task_id, choice_list, course_id):
    '''adds multiple choice task options to choices, called when creating mc task'''
    for choice in choice_list:
        sql = "INSERT INTO choices (task_id, choice, course_id) VALUES (:task_id, :choice, :course_id)"
        db.session.execute(sql, {"task_id":task_id, "choice":choice, "course_id":course_id})

    db.session.commit()


def qa_tasks_list(course_id, week, user_id): # type 0
    '''little complicated, gets list of useful information, called in week/x/tasks'''
    # returns list of q&a tasks with additional info, such as how many times the user has tried
    # to answer, how many points they have etc.
    sql = "SELECT T.id, T.question, T.correctanswer, T.maxpoints, T.max_tries, S.tries, S.points  "\
        "FROM tasks T, submissions S WHERE T.course_id=:id AND T.week=:week "\
            "AND T.type=0 AND S.task_id=T.id AND S.user_id=:uid ORDER BY T.id"
    result = db.session.execute(sql, {"id":course_id, "week":week, "uid":user_id})
    return result.fetchall()


def delete_from_submissions(course_id, user_id):
    '''deletes entries from submissions with user_id, called when leaving a course'''
    sql = "DELETE FROM submissions WHERE course_id=:course_id AND user_id=:user_id"
    db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    db.session.commit()


def course_tasks(course_id):
    '''gets course's all tasks' ids'''
    sql = "SELECT id FROM tasks where course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()


def add_submissions_old(course_id, user_id):
    '''adds empty submissions to new task to participants when new task is created'''
    task_list = course_tasks(course_id)

    for task_id in task_list:
        sql = "INSERT INTO submissions (course_id, user_id, task_id, tries, points) "\
            "VALUES (:cid, :uid, :tid, 0, 0)"
        db.session.execute(sql, {"cid":course_id, "uid":user_id, "tid":task_id[0]})

    db.session.commit()


def add_submissions_new(course_id, task_id):
    '''adds empty submissions to existing tasks when joining a course'''
    user_list = courses.participants_ids(course_id)

    for user_id in user_list:
        sql = "INSERT INTO submissions (course_id, user_id, task_id, tries, points) "\
            "VALUES (:cid, :uid, :tid, 0, 0)"
        db.session.execute(sql, {"cid":course_id, "uid":user_id[0], "tid":task_id})

    db.session.commit()


def correct_answer(task_id):
    '''gets task's correct answer'''
    sql = "SELECT correctanswer FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":task_id})
    return result.fetchone()[0]


def add_submission_try(task_id, user_id):
    '''increment try count by one to a task in table submissions'''
    sql = "UPDATE submissions SET tries=tries+1 WHERE task_id=:task_id AND user_id=:user_id"
    db.session.execute(sql, {"task_id":task_id, "user_id":user_id})
    db.session.commit()


def update_points(task_id, user_id, points):
    '''updates points in submissions'''
    sql = "UPDATE submissions SET points=:points WHERE task_id=:task_id AND user_id=:user_id"
    db.session.execute(sql, {"points":points, "task_id":task_id, "user_id":user_id})
    db.session.commit()


def mc_tasks_list(course_id, week, user_id): # type 1
    '''little more complicated, nice way to list multiple choice tasks, more info in function'''
    # gets a SORTED BY CHOICE ID table of something like this:
    # multiple choice question1 - option1 - other stuff
    # multiple choice question1 - option2 - other stuff
    # multiple choice question1 - option3 - other stuff
    # multiple choice question1 - option4 - other stuff
    # multiple choice question2 - option1 - other stuff etc.
    # now in tasks.html you can print the list four at a time, since it's sorted
    sql = "SELECT T.id, C.id, T.question, T.maxpoints, T.max_tries, C.choice, S.tries, S.points, T.week "\
        "FROM tasks T, choices C, submissions S WHERE T.course_id=:id AND T.id=C.task_id "\
            "AND T.week=:week AND S.task_id=T.id AND S.user_id=:user_id AND T.type=1 ORDER BY C.id"
    result = db.session.execute(sql, {"id":course_id, "week":week, "user_id":user_id})
    return result.fetchall()


def choice_text(choice_id):
    '''gets choice text with this choice id'''
    sql = "SELECT choice FROM choices WHERE id=:id"
    result = db.session.execute(sql, {"id":choice_id})
    return result.fetchone()[0]


def tries_and_points(task_id):
    '''gets max tries, points, current tries for this task for this user'''
    sql = "SELECT t.max_tries, t.maxpoints, s.tries FROM tasks t, submissions s "\
        "WHERE t.id=s.task_id AND s.user_id=:uid AND t.id=:tid"
    result = db.session.execute(sql, {"uid":users.user_id(), "tid":task_id})
    return result.fetchone()
