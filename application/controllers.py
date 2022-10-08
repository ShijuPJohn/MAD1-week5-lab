import sqlalchemy
from flask import render_template, current_app as app, request, redirect

from application.models import Student, db, Enrollments

course_dict = {"course_1": 1, "course_2": 2, "course_3": 3, "course_4": 4}


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
    try:
        form = request.form
        student = Student(roll_number=form["roll"], first_name=form["f_name"], last_name=form["l_name"])
        db.session.add(student)
        db.session.commit()
        students = Student.query.all()
        sid = 0
        if len(students) != 0:
            sid = students[-1].student_id
        course_list = form.getlist("courses")
        for course in course_list:
            enrollment = Enrollments(estudent_id=sid, ecourse_id=course_dict[course])
            db.session.add(enrollment)
            db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return render_template("duplicate_rollnumber.html")
    except Exception as e:
        print("Some Error Happened")
    return redirect("/")
