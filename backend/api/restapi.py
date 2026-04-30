from flask import Blueprint, request, jsonify
from datetime import datetime
from db import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.faculty import Faculty
from backend.models.departments import Department



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
  course_name = request.form["course_name"]
  department = request.form["department"]
  designation = request.form["designation"]
  
  new_user = User(username=username, role="faculty")
  new_user.set_password(password)

  db.session.add(new_user)
  db.session.flush()

  new_faculty = Faculty(name=name,email=email,course_name=course_name,
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

