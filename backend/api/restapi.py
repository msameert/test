from flask import Blueprint, request, jsonify, redirect, url_for
from datetime import datetime
from db import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.faculty import Faculty
from backend.models.departments import Department
from backend.models.courses import Course
from backend.models.facultycourses import FacultyCourse
from backend.models.semester import Semester


api = Blueprint('api',__name__)

@api.route('/admin/create_users', methods=['POST']) 

def create_students():
  username = request.form["username"]
  password = request.form["password"]

  firstname = request.form["firstname"]
  lastname = request.form["lastname"]
  email = request.form["email"]
  enroll_year = request.form["enroll_year"]
  cnic = request.form["cnic"]
  gender = request.form["gender"]

  new_user = User(username=username, role="student")
  new_user.set_password(password)
  
  db.session.add(new_user)
  db.session.flush()

  new_student = Student(firstname=firstname, lastname= lastname,
                        email= email, enroll_year= enroll_year, cnic=cnic,gender=gender,
                        user_id=new_user.id)

  db.session.add(new_student)
  db.session.commit()
  return {"message": "Student created successfully"}, 201

@api.route('/admin/create_faculty', methods=['POST'])

def create_faculty():
  username = request.form["username"]
  password = request.form["password"]

  name = request.form["name"]
  email = request.form["email"]
  department = request.form["department"]
  designation = request.form["designation"]
  
  new_user = User(username=username, role="faculty")
  new_user.set_password(password)

  db.session.add(new_user)
  db.session.flush()

  new_faculty = Faculty(name=name,email=email,
                        department=department,designation=designation,user_id=new_user.id)
  
  db.session.add(new_faculty)
  db.session.commit()
  return {"message": "Faculty created successfully"}, 201


@api.route('/admin/create_department', methods=["POST"])
def create_department() :
  name = request.form["name"]
  code = request.form["code"]

  new_department = Department(name=name, code=code)
  db.session.add(new_department)
  db.session.commit()
  return {"message": "Department created succesfuly"}, 201

@api.route('/admin/create_course', methods=["POST"])
def create_course() :
  course_name = request.form["course_name"]
  course_code = request.form["course_code"]
  credit_hours = request.form["credit_hours"]
  department_id = request.form["department_id"]

  new_course = Course(course_name=course_name, course_code=course_code, credit_hours = credit_hours, department_id = department_id)
  db.session.add(new_course)
  db.session.commit()
  return {"message": "Course created succesfuly"}, 201

@api.route('/admin/create_semester', methods=["POST"])
def create_semester() :
  name = request.form["name"]
  code = request.form.get("code")
  year = request.form.get("year")
  number = request.form.get("number")
  type = request.form.get("type")

  new_semester = Semester(name=name, code=code, year=year, semester_number=number, semester_type=type )
  db.session.add(new_semester) 
  db.session.commit()
  return {"message": "Semester created succesfuly"}, 201

@api.route("/admin/assign_faculty_courses", methods=["POST"])
def assign_faculty_courses():

    faculty_id = request.form.getlist("faculty_id")
    course_ids = request.form.getlist("course_ids")
    semester_id = request.form.getlist("semester_id")

    if not faculty_id or not course_ids or not semester_id:
        return "Please select a faculty and at least one course.", 400

    # Add new assignments
    for course_id in course_ids:
        fc = FacultyCourse(
            faculty_id=faculty_id,
            course_id=course_id,
            semester_id=semester_id
        )
        db.session.add(fc)

    db.session.commit()

    return redirect(url_for("admin_dashboard"))