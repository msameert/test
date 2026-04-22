from flask import Flask,render_template, redirect, session, url_for, request
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

from flask_sqlalchemy import SQLAlchemy
from db import db
from backend.models.user import User
from backend.models.student import Student


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

    return redirect(url_for("home"))

@app.route("/test")
def test() :
  return render_template("home.html", message="Supabase connected successfully")

@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return "Unauthorized", 403
    return render_template("dashboard.html")

@app.route("/student/dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return "Unauthorized", 403
    
    student = Student.query.filter_by(user_id=session["user_id"]).first()

    return render_template("studentdashboard.html", firstname=student.firstname)

if __name__ == "__main__" :
  app.run(debug=True)

