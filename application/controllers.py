from flask import render_template, current_app as app, request, redirect

from application.models import Student, db


@app.route('/', methods=['GET'])
def index_get():
    students = []
    students = Student.query.all()
    print(students)
    return render_template("index.html", students=students)


@app.route('/articles', methods=['GET'])
def articles_get():
    return render_template("articles.html")


@app.route('/student/create', methods=['GET'])
def create_students_get():
    return render_template("create_student.html")


@app.route('/student/create', methods=['POST'])
def create_students_post():
    print(request.form)
    form = request.form
    student = Student(roll_number=form["roll"], first_name=form["f_name"], last_name=form["l_name"])
    db.session.add(student)
    db.session.commit()
    return redirect("/")
