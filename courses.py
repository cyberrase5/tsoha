'''functions conserning mostly courses'''
from db import db

import users

def course(course_id):
    '''gets course name and descriptions for front page'''
    sql = "SELECT coursename, description FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id":course_id})
    return result.fetchone()


def join_course(course_id, user_id):
    '''joins course, updates participants'''
    if users.is_enrolled(course_id, user_id):
        return

    sql = "INSERT INTO participants (course_id, user_id) VALUES (:c_id, :u_id)"
    db.session.execute(sql, {"c_id":course_id, "u_id":user_id})
    db.session.commit()


def create_course(name, description):
    '''creates course (unique name check)'''
    sql = "SELECT 1 FROM courses WHERE coursename=:name"
    result = db.session.execute(sql, {"name":name})
    if result.fetchone():
        return False

    sql = "INSERT INTO courses (coursename, teacher_id, description) "\
        "VALUES (:name, :id, :text) RETURNING id"
    user_id = users.user_id()
    result = db.session.execute(sql, {"name":name, "id":user_id, "text":description})
    db.session.commit()
    join_course(result.fetchone()[0], users.user_id())
    return True


def list_courses(flag): # flag 0 = my courses, 1 = all courses
    '''gets list of courses, arg 0 = my courses, 1 = all courses'''
    user_id = users.user_id()
    if flag == 0:
        sql = "SELECT C.id, C.coursename FROM courses C, participants P "\
            "WHERE C.id=P.course_id AND P.user_id=:id"
        result = db.session.execute(sql, {"id":user_id})
        print()
    if flag == 1:
        result = db.session.execute("SELECT id, coursename FROM courses")

    return result.fetchall()


def course_name(course_id):
    '''gets course name'''
    sql = "SELECT coursename FROM courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()[0]


def participants_count(course_id):
    '''gets participant count - teacher'''
    sql = "SELECT COUNT(*)-1 FROM participants WHERE course_id=:id"
    result = db.session.execute(sql, {"id":course_id})
    return result.fetchone()[0]


def course_points_stats(course_id):
    '''gets amount of tasks and sum of their points'''
    sql = "SELECT COUNT(*), COALESCE(SUM(maxpoints), 0) FROM tasks WHERE course_id=:id"
    result = db.session.execute(sql, {"id":course_id})
    return result.fetchone()


def delete_course(course_id):
    '''deletes course, removes from courses and where CASCADE is specified'''
    sql = "DELETE FROM courses WHERE id=:id"
    db.session.execute(sql, {"id":course_id})
    db.session.commit()


def participants_ids(course_id):
    '''gets course's participants' ids'''
    sql = "SELECT user_id FROM participants WHERE course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()


def all_points(course_id):
    '''gets participants' names and points'''
    sql = "SELECT U.firstname, U.lastname, SUM(S.points) FROM users U, submissions S "\
        "WHERE S.course_id=:id AND U.id=S.user_id GROUP BY U.lastname, U.firstname;"
    result = db.session.execute(sql, {"id":course_id})
    return result.fetchall()


def my_points(course_id, user_id):
    '''gets list of user's this course's tasks and points of them'''
    sql = "SELECT T.question, S.points, T.maxpoints FROM tasks T, submissions S "\
        "WHERE T.course_id=:cid AND S.user_id=:uid AND T.id=S.task_id;"
    result = db.session.execute(sql, {"cid":course_id, "uid":user_id})
    return result.fetchall()


def my_points_summary(course_id, user_id):
    '''gets user's sum of points and max points for this course'''
    sql = "SELECT SUM(S.points), SUM(T.maxpoints) FROM tasks T, submissions S "\
        "WHERE T.course_id=:cid AND S.user_id=:uid AND T.id=S.task_id"
    result = db.session.execute(sql, {"cid":course_id, "uid":user_id})
    return result.fetchall()
