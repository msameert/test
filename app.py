from flask import Flask,render_template, redirect 
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
conn = engine.connect()

app = Flask(__name__)


@app.route("/")
def home () :
  return render_template("home.html")

@app.route("/test")
def test() :
  return render_template("home.html", message="Supabase connected successfully")


if __name__ == "__main__" :
  app.run(debug=True)

