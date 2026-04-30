# 🚀 Flask + Supabase + Gunicorn + Docker + Alembic + Vercel Setup 

## 1. Project Setup
Created Flask project
Installed dependencies
   -- pip install flask sqlalchemy psycopg2-binary python-dotenv alembic gunicorn

## 2. Virtual Environment Setup
   -- python -m venv venv
   -- venv\Scripts\activate   # Windows

## 3. Supabase Database Setup
Created project in Supabase
Copied PostgreSQL connection string (session pooler URL)

Created .env file:

   -- DATABASE_URL=postgresql://username:password@host:5432/postgres

### ❌ ERROR 1: Supabase host name resolution issue
Problem
could not translate host name ...
Cause :
Incorrect Supabase URL formatting / credentials

Fix :
Verified correct Supabase connection string
Ensured proper pooler URL format

## 4. SQLAlchemy Connection Setup
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
conn = engine.connect()

## 5. Docker Setup
Dockerfile (initial)
FROM python:3.13.4-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

### ❌ ERROR 2: Port mismatch in Docker
Problem :

App not accessible using wrong port mapping

Fix :

Correct usage:

  -- docker run -p 5000:5000 testapp

### ❌ ERROR 3: Wrong URL used in browser
Problem
Trying:

http://0.0.0.0:5000

Fix :

Correct:

http://localhost:5000

## 6. Flask + Docker + Gunicorn Final Working Command
  -- docker run -p 5000:5000 testapp

## 7. Alembic Setup (Database Migrations)
Install Alembic
  -- pip install alembic
Initialize
  -- alembic init migrations

### ❌ ERROR 4: Interpolation error in DATABASE_URL
Problem
invalid interpolation syntax %
Fix

Escaped % in URL OR handled in env.py:

DATABASE_URL.replace("%", "%%")

## 8. Alembic env.py Configuration
Fixed metadata issue
from backend.models.user import Base

target_metadata = Base.metadata

## 9. Migration Generation 
  -- alembic revision --autogenerate -m "Creating User Model"

## 10. Apply Migration to Database
  -- alembic upgrade head

### Architecture for Database
  Flask App
     ↓
SQLAlchemy ORM
     ↓
Alembic Migrations
   ↓
Supabase PostgreSQL 

## 11. Role-Based Authentication 
Implemented login system 
Stored user information in session:
  --  user_id
  --  username
  --  role
### Redirect users based on role after login:
   Admin → /admin/dashboard
   Student → /student/dashboard
   ---  session["user_id"] = user.id
   ---  session["username"] = user.username
   ---  session["role"] = user.role

## Separate Dashboards by Role
Admin dashboard
  --  /admin/dashboard
Student dashboard
  --  /student/dashboard

### Each route checks role before allowing access:

if session.get("role") != "admin":
    return redirect(url_for("home"))

## ❌ Error 5 : Role Based Redirect Loop

ERR_TOO_MANY_REDIRECTS

Cause:

/dashboard → /dashboard → infinite loop

Wrong:

  --  return redirect(url_for("dashboard"))

Fix:
Redirect directly to role dashboards:

admin → /admin/dashboard
student → /student/dashboard

## 12. Deployment on Vercel

Created a clean requirements.txt with required dependencies:

Flask
Flask-SQLAlchemy
SQLAlchemy
Jinja2
Werkzeug
psycopg2-binary
python-dotenv
requests
PyJWT
gunicorn
alembic

## Error 6 : Issue encountered

Vercel build failed with:

Failed to parse requirements.txt
Unexpected '�'
Cause

The file was saved in UTF-16 LE encoding with hidden BOM characters.

Fix

Converted file encoding to UTF-8 in VS Code:

Bottom right → UTF-16 LE → Save with Encoding → UTF-8

After conversion, redeployed successfully.

## Live URL :

### https://lms-system-dev.vercel.app/












