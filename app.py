from flask import Flask,render_template, redirect, session, url_for, request
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

from flask_sqlalchemy import SQLAlchemy
from db import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.faculty import Faculty
from backend.models.departments import Department
from backend.models.courses import Course
from backend.models.semester import Semester
from backend.models.facultycourses import FacultyCourse
from backend.models.studentcourses import StudentCourse
from backend.models.assessment import Assessment
from backend.models.studentmarks import Studentmark


load_dotenv()

app = Flask(__name__)

from backend.api.restapi import api
app.register_blueprint(api, url_prefix='/api')

app.secret_key = os.getenv('SECRET_KEY', 'secret123')

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)



@app.route("/")
def home () :
  return render_template("signin.html")
  
# Login
@app.route("/login", methods=["POST"])
def login() :
             # Collect info from DB 
      username = request.form['username']
      password = request.form['password']
      user = User.query.filter_by(username=username).first()

      if user and user.check_password(password):

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))

        elif user.role == "student":
            return redirect(url_for("student_dashboard"))
        
        elif user.role == "faculty":
            return redirect(url_for("faculty_dashboard"))
      

# Register
@app.route("/register", methods=["POST"])
def register() :
            # Add a new user in DB
      username = request.form['username']  
      password = request.form['password']
      user = User.query.filter_by(username=username).first()
      if user :
          return render_template("signin.html")     # If user already present then return to homepage
      else :
          new_user = User(username = username)
          new_user.set_password(password)
          db.session.add(new_user)
          db.session.commit()
          session['username'] = username
          return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
      
@app.route("/dashboard")
def dashboard():

    role = session.get("role")

    if role == "admin":
        return redirect(url_for("admin_dashboard"))

    elif role == "student":
        return redirect(url_for("student_dashboard"))
    
    elif role == "faculty":
            return redirect(url_for("faculty_dashboard"))

    return redirect(url_for("home"))

@app.route("/test")
def test() :
  return render_template("home.html", message="Supabase connected successfully")

@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return "Unauthorized", 403

    faculties = Faculty.query.all()
    courses = Course.query.all()
    semesters = Semester.query.all()
    students = Student.query.all()

    return render_template("dashboard.html", faculties=faculties, courses=courses, semesters=semesters, students=students)

@app.route("/student/dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return "Unauthorized", 403
    
    student = Student.query.filter_by(user_id=session["user_id"]).first()

    student_courses = StudentCourse.query.filter_by(student_id=student.id).all()

    department = Department.query.filter_by(id=student.department_id).first()

    course = Course.query.all()

    return render_template("studentdashboard.html", firstname=student.firstname, student_courses=student_courses, department=department, course=course)

@app.route("/faculty/dashboard")
def faculty_dashboard():
    if session.get("role") != "faculty":
        return "Unauthorized", 403
    
    faculty = Faculty.query.filter_by(user_id=session["user_id"]).first()

    faculty_courses = FacultyCourse.query.filter_by(faculty_id=faculty.id).all()

    course_students = {}

    for fc in faculty_courses:
        enrollments = StudentCourse.query.filter_by(
            course_id=fc.course_id,
            semester_id=fc.semester_id
        ).all()
        course_students[fc.id] = enrollments

    return render_template("facultydashboard.html", name=faculty.name, faculty_courses=faculty_courses, course_students=course_students)

@app.route("/assessment")
def assessment():
    if session.get("role") != "faculty":
        return "Unautorized", 403

    faculty = Faculty.query.filter_by(user_id=session["user_id"]).first()

    faculty_courses = FacultyCourse.query.filter_by(faculty_id=faculty.id).all()

    course_students = {}
    assessments_by_course = {}

    for fc in faculty_courses:
        enrollments = StudentCourse.query.filter_by(
            course_id=fc.course_id,
            semester_id=fc.semester_id
        ).all()
        course_students[fc.id] = enrollments

    assessments = Assessment.query.filter_by(faculty_id=faculty.id).all()
    for assessment in assessments:
        assessments_by_course.setdefault(assessment.course_id, []).append(assessment)

    return render_template(
        "assessment.html",
        name=faculty.name,
        faculty_courses=faculty_courses,
        course_students=course_students,
        assessments=assessments_by_course
    )

@app.route("/assessment/<int:assessment_id>")
def assessment_details(assessment_id):

    assessment = Assessment.query.get(assessment_id)
    
    if not assessment:
        return "Assessment not found", 404
    
    # Get the faculty course to determine semester
    faculty_course = FacultyCourse.query.get(assessment.course_id)
    
    # Get all students enrolled in this course and semester
    enrolled_students = StudentCourse.query.filter_by(
        course_id=assessment.course_id,
        semester_id=faculty_course.semester_id if faculty_course else None
    ).all()
    
    # Get marks for this assessment
    marks_dict = {}
    marks = Studentmark.query.filter_by(assessment_id=assessment_id).all()
    for mark in marks:
        marks_dict[mark.student_id] = mark.obtained_marks

    faculty = Faculty.query.filter_by(user_id=session["user_id"]).first()

    return render_template("assessmentdetails.html", assessment=assessment, enrolled_students=enrolled_students, marks_dict=marks_dict, name=faculty.name)

@app.route("/result/<int:course_id>")
def student_result(course_id):

    student = Student.query.filter_by(user_id=session["user_id"]).first()

    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return "Course not found", 404

    assessments = Assessment.query.filter_by(course_id=course_id).order_by(Assessment.id).all()
    marks_by_assessment = {
        mark.assessment_id: mark
        for mark in Studentmark.query.filter_by(student_id=student.id).all()    # this creates dictionary
    }


    return render_template(
        "studentresult.html", assessments=assessments, marks_by_assessment=marks_by_assessment)


if __name__ == "__main__" :
  app.run(debug=True)
