'''routes'''
from flask import render_template, request, redirect, session, abort
import users
import tasks
import courses

from app import app

@app.route("/")
def index():
    '''index'''
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''login handler'''
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if users.login(username, password):
        return redirect("/")

    return render_template("error.html", message="Väärä käyttäjätunnus tai salasana (todennäköisesti)")


@app.route("/register", methods=["GET", "POST"])
def register():
    '''registration handler'''
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        password = request.form["password"]
        proof = request.form["teacherness"]
        role = int(request.form["type"])
        pos = "opiskelija"
        teacher = False

        if role == 1:
            pos = "opettaja"
            teacher = True
            if not users.authenticate_teacherness(proof):
                return render_template("error.html", message="Et ole oikeasti opettaja, et tiedä salasanaa")

        if users.register(firstname, lastname, password, username, teacher):
            return render_template("reg.html", fname=firstname, lname=lastname, uname=username, role=pos)

        return render_template("error.html", message="Rekisteröityminen epäonnistui, "\
            "käyttäjänimi todennäköisesti jo käytössä")

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/logout")
def logout():
    '''logout'''
    users.logout()
    return redirect("/")


@app.route("/course/<int:course_id>")
def course(course_id):
    '''course front page'''
    name = courses.course(course_id)
    enrolled = users.is_enrolled(course_id, users.user_id())
    teacher = users.is_course_teacher(course_id, users.user_id())
    task_stats = courses.course_points_stats(course_id)
    participants = courses.participants_count(course_id)

    return render_template("course.html", cid=course_id, data=name, enrolled=enrolled, isteacher=teacher,
                           taskcount=task_stats[0], points=task_stats[1], parts=participants)


@app.route("/joinCourse/<int:course_id>")
def join_course(course_id):
    '''joins course'''
    user_id = users.user_id()
    courses.join_course(course_id, user_id)
    tasks.add_submissions_old(course_id, user_id)

    return redirect("/course/" + str(course_id))


@app.route("/allCourses")
def all_courses():
    '''lists all courses'''
    course_list = courses.list_courses(1)
    return render_template("allCourses.html", course_list=course_list)


@app.route("/myCourses")
def my_courses():
    '''lists course currently enrolled by user'''
    course_list = courses.list_courses(0)
    return render_template("myCourses.html", course_list=course_list)


@app.route("/createCourse", methods=["GET", "POST"])
def create_course():
    '''course creation handler'''
    if request.method == "GET":
        return render_template("createCourse.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        name = request.form["name"]
        desc = request.form["description"]

        if courses.create_course(name, desc):
            return redirect("/")

        return render_template("error.html", message="Virhe, "\
            "samanniminen kurssi on jo olemassa, lisää esim. syksy 2022")

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/course/<int:course_id>/week/<int:week>")
def week(course_id, week):
    '''lists this week's tasks'''
    name = courses.course_name(course_id)
    teacher = users.is_course_teacher(course_id, users.user_id())
    text_list = tasks.week_texts(course_id, week)
    enrolled = users.is_enrolled(course_id, users.user_id())

    return render_template("week.html", cid=course_id, coursename=name, no=week, 
                            teacher=teacher, text_list=text_list, enrolled=enrolled)


@app.route("/course/<int:course_id>/week/<int:week>/createText", methods=["GET", "POST"])
def create_text(course_id, week):
    '''creates text for specified week'''
    if request.method == "GET":
        teacher = users.is_course_teacher(course_id, users.user_id())
        return render_template("createText.html", teacher=teacher, cid=str(course_id), no=str(week))
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        content = request.form["text"]
        tasks.create_text(course_id, week, content)
        return redirect("/course/" + str(course_id) + "/week/" + str(week))

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/course/<int:course_id>/week/<int:week>/createQA", methods=["GET", "POST"])
def create_qa_task(course_id, week):
    '''creates question and answer task for this week'''
    if request.method == "GET":
        teacher = users.is_course_teacher(course_id, users.user_id())
        return render_template("createQA.html", teacher=teacher, cid=str(course_id), no=str(week))
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        question = request.form["question"]
        answer = request.form["answer"]
        tries = request.form["tries"]
        points = request.form["points"]

        if int(points) < 1:
            return render_template("error.html", message="Tehtävästä pitää saada vähintään yksi piste")

        task_id = tasks.create_qa_task(course_id, question, answer, points, tries, week)
        tasks.add_submissions_new(course_id, task_id)
        return redirect("/course/" + str(course_id) + "/week/" + str(week))

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/course/<int:course_id>/week/<int:week>/createMultipleChoice", methods=["GET", "POST"])
def create_mc_task(course_id, week):
    '''creates multiple choice task for this week'''
    if request.method == "GET":
        teacher = users.is_course_teacher(course_id, users.user_id())
        return render_template("createMultipleChoice.html", teacher=teacher,
                               cid=str(course_id), no=str(week))
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        question = request.form["question"]
        answer = request.form["answer"]
        tries = request.form["tries"]
        points = request.form["points"]
        choices = request.form.getlist("choice")

        if int(points) < 1:
            return render_template("error.html", message="Tehtävästä pitää saada vähintään yksi piste")

        task_id = tasks.create_mc_task(course_id, question, answer, points, tries, week)
        tasks.add_choices(task_id, choices, course_id)
        tasks.add_submissions_new(course_id, task_id)

        return redirect("/course/" + str(course_id) + "/week/" + str(week))

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/course/<int:course_id>/week/<int:week>/tasks")
def task_list(course_id, week):
    '''lists tasks on week page'''
    user_id = users.user_id()
    qa_list = tasks.qa_tasks_list(course_id, week, user_id)
    mc_list = tasks.mc_tasks_list(course_id, week, user_id)
    name = courses.course_name(course_id)

    # this is a mess I know, more info in tasks_list functions

    return render_template("tasks.html", no=course_id, coursename=name, QA_list=qa_list,
                           week=week, MC_list=mc_list, i=0, len=int(len(mc_list)/4))


@app.route("/course/<int:course_id>/leave")
def leave(course_id):
    '''leaves course, deletes entries from submissions and participants'''
    user_id = users.user_id()
    tasks.delete_from_submissions(course_id, user_id)
    users.leave_course(course_id, user_id)

    return redirect("/course/" + str(course_id))


@app.route("/course/<int:course_id>/delete")
def delete(course_id):
    '''deletes course, for course teacher only'''
    if not users.is_course_teacher(course_id, users.user_id()):
        return render_template("error.html", message="Virhe, sinulla ei ole oikeuksia poistaa tätä tätä kurssia")
    courses.delete_course(course_id)

    return redirect("/allCourses")


@app.route("/course/<int:course_id>/allPoints")
def all_points(course_id):
    '''lists all participants and their points'''
    user_id = users.user_id()
    points_list = courses.all_points(course_id)
    teacher = users.is_course_teacher(course_id, user_id)
    maxpoints = courses.my_points_summary(course_id, user_id)

    return render_template("allPoints.html", cid=course_id, points_list=points_list,
                           teacher=teacher, maxpoints=maxpoints[0][1])


@app.route("/course/<int:course_id>/myPoints")
def my_points(course_id):
    '''lists current users points by task'''
    user_id = users.user_id()
    enrolled = users.is_enrolled(course_id, user_id)
    points_list = courses.my_points(course_id, user_id)
    summary = courses.my_points_summary(course_id, user_id)

    return render_template("myPoints.html", cid=course_id, points_list=points_list,
                           enrolled=enrolled, summary=summary)


@app.route("/QA", methods=["POST"])
def qa_handler():
    '''question and answer task handler'''
    if request.method == "POST":
        answer = request.form["answer"]
        task_id = request.form["task_id"]
        course_id = request.form["id"]
        week = request.form["week"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        stats = tasks.tries_and_points(task_id)
        # [0] max tries, [1] points, [2] current tries
        if stats[2] >= stats[0]:
            return render_template("error.html", message="Olet vastannut liian monta kertaa, älä yritä huijata")

        correct_answer = tasks.correct_answer(task_id)
        user_id = users.user_id()
        tasks.add_submission_try(task_id, user_id)

        if answer.lower() == correct_answer.lower():
            tasks.update_points(task_id, user_id, stats[1])
            return render_template("correct.html", points=stats[1], cid=course_id, week=week)

        return render_template("error.html", message="Väärä vastaus", id=course_id, week=week)

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/MC", methods=["POST"])
def mc_handler():
    '''multiple choice task handler'''
    if request.method == "POST":
        answer_choice_id = int(request.form["choice"])
        task_id = int(request.form["task_id"])
        course_id = request.form["course_id"]
        week = request.form["week"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        stats = tasks.tries_and_points(task_id)
        # [0] max tries, [1] points, [2] current tries

        if int(stats[2]) >= int(stats[0]):
            return render_template("error.html", message="Olet vastannut liian monta kertaa, älä yritä huijata")

        user_id = users.user_id()
        tasks.add_submission_try(task_id, user_id)
        if tasks.choice_text(answer_choice_id) == tasks.correct_answer(task_id):
            tasks.update_points(task_id, user_id, stats[1])
            return render_template("correct.html", points=stats[1], cid=course_id, week=week)

    return render_template("error.html", message="Tuntematon virhe")


@app.route("/error")
def error():
    '''error'''
    return render_template("error.html")
