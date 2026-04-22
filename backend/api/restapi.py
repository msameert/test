from flask import Blueprint, request, jsonify
from datetime import datetime
from db import db
from backend.models.user import User
from backend.models.student import Student



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
