from flask import Flask,render_template, redirect, session, url_for, request
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

from flask_sqlalchemy import SQLAlchemy
from db import db
from backend.models.user import User

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'secret123')

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)



@app.route("/")
def home () :
  if "username" in session :
    return redirect(url_for("dashboard"))
  return render_template("signin.html")
  
# Login
@app.route("/login", methods=["POST"])
def login() :
             # Collect info from DB 
      username = request.form['username']
      password = request.form['password']
      user = User.query.filter_by(username=username).first()
      if user and user.check_password(password):
          session['username'] = username 
          return redirect(url_for("dashboard"))
      else :
          return render_template("signin.html")
      

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
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for("home"))

@app.route("/test")
def test() :
  return render_template("home.html", message="Supabase connected successfully")


if __name__ == "__main__" :
  app.run(debug=True)

