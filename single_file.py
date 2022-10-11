import os.path

import sqlalchemy
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False, )
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False, )


@app.route('/', methods=['GET'])
def index_get():
    students = Student.query.all()
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
        course_dict = {"course_1": 1, "course_2": 2, "course_3": 3, "course_4": 4}
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
    Student.query.filter(Student.student_id == sid).delete()
    Enrollments.query.filter(Enrollments.estudent_id == sid).delete()
    db.session.commit()
    return redirect("/")


@app.route('/student/<sid>/update', methods=['GET'])
def update_students_get(sid):
    student = Student.query.filter(Student.student_id == sid).first()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id == sid).all()
    courses = [i.ecourse_id for i in enrollments]
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
    course_dict = {"course_1": 1, "course_2": 2, "course_3": 3, "course_4": 4}
    for course in course_list:
        enrollment = Enrollments(estudent_id=sid, ecourse_id=course_dict[course])
        db.session.add(enrollment)
        db.session.commit()
    return redirect("/")


@app.route('/student/<sid>', methods=['GET'])
def students_details_get(sid):
    student = Student.query.filter(Student.student_id == sid).first()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id == sid).all()
    course_ids = [i.ecourse_id for i in enrollments]
    course_list = []
    for index, cid in enumerate(course_ids):
        course = Course.query.filter(Course.course_id == cid).first()
        course_list.append([index + 1, course.course_code, course.course_name, course.course_description])
    return render_template("student_details.html", student=student, courses=course_list)


if __name__ == "__main__":
    app.run()
