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
        return render_template("misc_error.html")
    return redirect("/")


@app.route('/student/<sid>/delete', methods=['GET'])
def delete_students_get(sid):
    print("Delete method called with sid : ", sid)
    Student.query.filter(Student.student_id == sid).delete()
    Enrollments.query.filter(Enrollments.estudent_id == sid).delete()
    db.session.commit()
    return redirect("/")


@app.route('/student/<sid>/update', methods=['GET'])
def update_students_get(sid):
    student = Student.query.filter(Student.student_id == sid).first()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id == sid).all()
    courses = [i.ecourse_id for i in enrollments]
    print("Update method called with sid : ", sid)
    return render_template("update_student.html", student=student, courses=courses)


@app.route('/student/<sid>/update', methods=['POST'])
def update_students_post(sid):
    form = request.form
    Student.query.filter(Student.student_id == sid) \
        .update({"first_name": request.form["f_name"],
                 "last_name": request.form["l_name"]})
    db.session.commit()
    Enrollments.query.filter(Enrollments.estudent_id == sid).delete()
    course_list = form.getlist("courses")
    for course in course_list:
        enrollment = Enrollments(estudent_id=sid, ecourse_id=course_dict[course])
        db.session.add(enrollment)
        db.session.commit()
    print(form)

    return redirect("/")
