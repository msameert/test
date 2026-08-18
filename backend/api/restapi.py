from flask import Blueprint, request, jsonify, redirect, url_for, session
from datetime import datetime
from db import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.faculty import Faculty
from backend.models.departments import Department
from backend.models.courses import Course
from backend.models.facultycourses import FacultyCourse
from backend.models.semester import Semester
from backend.models.studentcourses import StudentCourse
from backend.models.assessment import Assessment
from backend.models.studentmarks import Studentmark


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
  department_id = request.form["department_id"]
  new_user = User(username=username, role="student")
  new_user.set_password(password)
  
  db.session.add(new_user)
  db.session.flush()

  new_student = Student(firstname=firstname, lastname= lastname,
                        email= email, enroll_year= enroll_year, cnic=cnic,gender=gender,
                        user_id=new_user.id, department_id=department_id)

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

    faculty_id = int(request.form.get("faculty_id"))
    course_ids = request.form.getlist("course_ids")
    semester_id = int(request.form.get("semester_id"))

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

@api.route("/admin/assign_student_courses", methods=["POST"])
def assign_student_courses():

    student_id = int(request.form.get("student_id"))
    course_ids = request.form.getlist("course_ids")
    semester_id = int(request.form.get("semester_id"))

    if not student_id or not course_ids or not semester_id:
        return "Please select a student and at least one course.", 400

    # Add new assignments
    for course_id in course_ids:
        sc = StudentCourse(
            student_id=student_id,
            course_id=course_id,
            semester_id=semester_id
        )
        db.session.add(sc)

    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@api.route("/assessment/get_assessment", methods=["POST"])
def get_assessment():
    assessment_title = request.form.get("title")
    total_marks = request.form.get("total_marks")
    course_id = request.form.get("course_id", type=int)

    faculty = Faculty.query.filter_by(user_id=session.get("user_id")).first()
    if not faculty:
        return "Unauthorized", 403

    faculty_id = faculty.id

    if not assessment_title or total_marks is None or course_id is None:
        return "Please enter title and total marks of assessment.", 400

    new_assessment = Assessment(
        title=assessment_title,
        total_marks=float(total_marks),
        course_id=course_id,
        faculty_id=faculty_id
    )
    db.session.add(new_assessment)
    db.session.commit()
    return {"message": "Assessment created successfully"}, 201

@api.route("/assessment/get_marks", methods=["POST"])
def get_marks():
    assessment_id = request.form.get("assessment_id", type=int)
    student_ids = request.form.getlist("student_id")
    marks_list = request.form.getlist("marks")
    
    if not assessment_id or not student_ids or not marks_list:
        return "Missing data", 400
    
    # Zip them together to pair each student with their mark
    for student_id, marks in zip(student_ids, marks_list):
        new_mark = Studentmark(
            student_id=int(student_id),
            assessment_id=assessment_id,
            obtained_marks=float(marks) if marks else 0
        )
        db.session.add(new_mark)
    
    db.session.commit()
    return {"message": "Marks assigned successfully"}, 201