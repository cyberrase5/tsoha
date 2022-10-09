from asyncio import tasks
from ctypes import pointer
from app import app
from flask import render_template, request, redirect
import users, courses, tasks

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana (todennäköisesti)")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        username=request.form["username"]
        password = request.form["password"]
        proof = request.form["teacherness"]
        role=int(request.form["type"])
        pos = "opiskelija"
        bool = False
        if role == 1:
            pos = "opettaja"
            bool = True
            if users.authenticate_teacherness(proof) == False:
                return render_template("error.html", message="Et ole oikeasti opettaja, et tiedä salasanaa")

        if users.register(firstname, lastname, password, username, bool):
            return render_template("reg.html", fname=firstname, lname=lastname, uname=username, role=pos)
        else:
            return render_template("error.html", message="Rekisteröityminen epäonnistui, käyttäjänimi todennäköisesti jo käytössä")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/course/<int:id>")
def course(id):
    name = courses.course(id)
    enrolled = users.is_enrolled(id, users.user_id())
    teacher = users.is_course_teacher(id, users.user_id())
    task_stats = courses.course_points_stats(id)
    participants = courses.participants_count(id)
    return render_template("course.html", id=id, data=name, enrolled=enrolled, isteacher=teacher, taskcount=task_stats[0], points=task_stats[1], parts=participants)

@app.route("/joinCourse/<int:id>")
def joinCourse(id):
    user_id=users.user_id()
    courses.join_course(id, user_id)
    tasks.add_submissions_old(id, user_id)
    return redirect("/course/" + str(id))

@app.route("/allCourses")
def allCourses():
    list = courses.list_courses(1)
    return render_template("allCourses.html", list=list)

@app.route("/myCourses")
def myCourses():
    list = courses.list_courses(0)
    return render_template("myCourses.html", list=list)


@app.route("/createCourse", methods=["GET", "POST"])
def createCourse():
    if request.method == "GET":
        return render_template("createCourse.html")
    if request.method == "POST":
        name=request.form["name"]
        desc=request.form["description"]
        if courses.create_course(name, desc):
            return redirect("/")
        else:
            return render_template("error.html", message="Virhe, samanniminen kurssi on jo olemassa, lisää esim. syksy 2022")

@app.route("/course/<int:id>/week/<int:week>")
def week(id, week):
    name = courses.course_name(id)
    teacher = users.is_course_teacher(id, users.user_id())
    list = tasks.week_texts(id, week)
    return render_template("week.html", id=id, coursename=name, no=week, teacher=teacher, list=list)

@app.route("/course/<int:id>/week/<int:week>/createText", methods=["GET", "POST"])
def createText(id, week):
    if request.method == "GET":
        return render_template("createText.html", teacher=users.is_course_teacher(id, users.user_id()), id=str(id), no=str(week))
    if request.method == "POST":
        content=request.form["text"]
        tasks.create_text(id, week, content)
        return redirect("/course/" + str(id) + "/week/" + str(week))

@app.route("/course/<int:id>/week/<int:week>/createQA", methods=["GET", "POST"])
def createQA(id, week):
    if request.method == "GET":
        return render_template("createQA.html", teacher=users.is_course_teacher(id, users.user_id()), id=str(id), no=str(week))
    if request.method == "POST":
        question=request.form["question"]
        answer=request.form["answer"]
        tries=request.form["tries"]
        points=request.form["points"]
        if int(points) < 1:
            return render_template("error.html", message="Tehtävästä pitää saada vähintään yksi piste")

        task_id = tasks.create_QA(id, question, answer, points, tries, week)
        tasks.add_submissions_new(id, task_id)
        return redirect("/course/" + str(id) + "/week/" + str(week))

@app.route("/course/<int:id>/week/<int:week>/createMultipleChoice", methods=["GET", "POST"])
def createMultipleChoice(id, week):
    if request.method == "GET":
        return render_template("createMultipleChoice.html", teacher=users.is_course_teacher(id, users.user_id()), id=str(id), no=str(week))
    if request.method == "POST":
        question=request.form["question"]
        answer=request.form["answer"]
        tries=request.form["tries"]
        points=request.form["points"]
        list=request.form.getlist("choice")

        if int(points) < 1:
            return render_template("error.html", message="Tehtävästä pitää saada vähintään yksi piste")

        task_id = tasks.create_MultipleChoice(id, question, answer, points, tries, week)
        tasks.add_choices(task_id, list, id)
        tasks.add_submissions_new(id, task_id)
        return redirect("/course/" + str(id) + "/week/" + str(week))


@app.route("/course/<int:id>/week/<int:week>/tasks")
def taskList(id, week):
    user_id=users.user_id()
    QA_list = tasks.QA_tasks(id, week, user_id)
    MC_list = tasks.MC_tasks(id, week, user_id)
    name = courses.course_name(id)
    return render_template("tasks.html", no=id, coursename=name, QA_list=QA_list, week=week, MC_list=MC_list, i=0, len=int(len(MC_list)/4))

@app.route("/course/<int:id>/leave")
def leave(id):
    user_id=users.user_id()
    tasks.delete_from_submissions(id, user_id)
    users.leave_course(id, user_id)

    return redirect("/course/" + str(id))
        

@app.route("/course/<int:id>/delete")
def delete(id):
    courses.delete_course(id)
    return redirect("/allCourses")

@app.route("/course/<int:id>/allPoints")
def allPoints(id):
    user_id = users.user_id()
    list = courses.all_points(id)
    teacher=users.is_course_teacher(id, user_id)
    maxpoints = courses.my_points_summary(id, user_id)
    return render_template("allPoints.html", id=id, list=list, teacher=teacher, maxpoints=maxpoints[0][1])


@app.route("/course/<int:id>/myPoints")
def myPoints(id):
    user_id=users.user_id()
    enrolled=users.is_enrolled(id, user_id)
    list = courses.my_points(id, user_id)
    summary = courses.my_points_summary(id, user_id)
    return render_template("myPoints.html", id=id, list=list, enrolled=enrolled, summary=summary)


@app.route("/QA", methods=["POST"])
def QA():
    if request.method == "POST":
        answer=request.form["answer"]
        task_id=request.form["task_id"]
        tries=request.form["tries"]
        maxtries=request.form["maxtries"]
        maxpoints=request.form["maxpoints"]
        id=request.form["id"]
        week=request.form["week"]
        if tries >= maxtries:
            return render_template("error.html", message="Olet vastannut liian monta kertaa, älä yritä huijata")

        correct_answer=tasks.correct_answer(task_id)
        user_id=users.user_id()
        tasks.add_submission_try(task_id, user_id)
        if answer == correct_answer:
            tasks.update_points(task_id, user_id, maxpoints)
            return render_template("correct.html", points=maxpoints, id=id, week=week)
        else:
            return render_template("error.html", message="Väärä vastaus", id=id, week=week)

@app.route("/MC", methods=["POST"])
def MC():
    if request.method == "POST":
        answer_choice_id=int(request.form["choice"])
        task_id=int(request.form["task_id"])
        tries=request.form["tries"]
        maxtries=request.form["maxtries"]
        maxpoints=request.form["maxpoints"]
        id=request.form["course_id"]
        week=request.form["week"]

        if tries >= maxtries:
            return render_template("error.html", message="Olet vastannut liian monta kertaa, älä yritä huijata")

        user_id=users.user_id()
        tasks.add_submission_try(task_id, user_id)
        if tasks.choice_text(answer_choice_id) == tasks.correct_answer(task_id):
            tasks.update_points(task_id, user_id, maxpoints)
            return render_template("correct.html", points=maxpoints, id=id, week=week)
        else:
            return render_template("error.html", message="Väärä vastaus", id=id, week=week)


@app.route("/error")
def error():
    return render_template("error.html")

