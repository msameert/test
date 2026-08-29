# 🚀 Flask + Supabase + Gunicorn + Docker + Alembic + Vercel

A Flask-based Learning Management System (LMS) built with **Python, Flask, SQLAlchemy, PostgreSQL/Supabase, Alembic, Gunicorn, Docker, and Vercel**.

The project includes database migrations, role-based authentication, separate dashboards for administrators and students, containerized local development, and Vercel deployment.

## 🌐 Live Demo

**Production:** https://lms-system-dev.vercel.app/

---

# 🏗️ Architecture

```text
                   ┌─────────────────────┐
                   │       Browser       │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │     Flask App       │
                   │  Authentication     │
                   │  Role Management    │
                   │  Routes / Views     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │     SQLAlchemy      │
                   │      ORM Layer      │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │      Alembic        │
                   │  Database Migration │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Supabase PostgreSQL  │
                   └─────────────────────┘
```

For local/containerized execution:

```text
Docker
  │
  ▼
Gunicorn
  │
  ▼
Flask Application
  │
  ▼
Supabase PostgreSQL
```

---

# 🛠️ Technology Stack

| Technology          | Purpose                         |
| ------------------- | ------------------------------- |
| **Python**          | Backend programming language    |
| **Flask**           | Web application framework       |
| **SQLAlchemy**      | ORM and database interaction    |
| **PostgreSQL**      | Relational database             |
| **Supabase**        | Hosted PostgreSQL database      |
| **Alembic**         | Database schema migrations      |
| **Gunicorn**        | Production WSGI server          |
| **Docker**          | Application containerization    |
| **Vercel**          | Deployment and hosting          |
| **Jinja2**          | Server-side HTML templating     |
| **python-dotenv**   | Environment variable management |
| **psycopg2-binary** | PostgreSQL database driver      |

---

# 📁 Project Setup

Create the Flask project and install the required dependencies:

```bash
pip install flask sqlalchemy psycopg2-binary python-dotenv alembic gunicorn
```

A virtual environment is recommended:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

---

# 🗄️ Supabase PostgreSQL Setup

A PostgreSQL database was created using **Supabase**.

The PostgreSQL connection string was added to a `.env` file:

```env
DATABASE_URL=postgresql://username:password@host:5432/postgres
```

> **Important:** Never commit `.env` or database credentials to Git.

Add the following to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# 🔌 SQLAlchemy Database Connection

The application loads the database URL from the environment:

```python
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

conn = engine.connect()
```

This allows the application to connect to the Supabase PostgreSQL database without hardcoding credentials.

---

# 🐳 Docker Setup

The application was containerized using Docker.

## Dockerfile

```dockerfile
FROM python:3.13.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

The application runs Gunicorn on port `5000`.

## Build the Docker Image

```bash
docker build -t testapp .
```

## Run the Container

```bash
docker run -p 5000:5000 testapp
```

The application can then be accessed at:

```text
http://localhost:5000
```

### Docker Port Mapping

The format is:

```text
HOST_PORT:CONTAINER_PORT
```

Therefore:

```bash
docker run -p 5000:5000 testapp
```

maps the host's port `5000` to the container's port `5000`.

> `0.0.0.0` is the address Gunicorn binds to inside the container. Use `localhost` in your browser.

---

# 🔄 Database Migrations with Alembic

Alembic is used to manage database schema changes and migrations.

Install Alembic:

```bash
pip install alembic
```

Initialize Alembic:

```bash
alembic init migrations
```

This creates the migration directory and configuration files.

---

# ⚙️ Alembic Configuration

The SQLAlchemy model metadata is connected to Alembic's migration system.

Example:

```python
from backend.models.user import Base

target_metadata = Base.metadata
```

This allows Alembic to detect changes in SQLAlchemy models when generating migrations.

---

# ⚠️ Alembic Environment Variable Issue

A database connection string containing `%` characters can cause an interpolation error in Alembic configuration.

The issue was resolved by escaping `%` characters:

```python
DATABASE_URL.replace("%", "%%")
```

This prevents Alembic's configuration parser from incorrectly interpreting `%` characters.

---

# 📝 Creating Migrations

After creating or modifying SQLAlchemy models, generate a migration:

```bash
alembic revision --autogenerate -m "Creating User Model"
```

Review the generated migration before applying it to the database.

Apply migrations:

```bash
alembic upgrade head
```

The migration flow is:

```text
SQLAlchemy Models
       │
       ▼
Alembic Autogenerate
       │
       ▼
Migration File
       │
       ▼
alembic upgrade head
       │
       ▼
Supabase PostgreSQL
```

---

# 🔐 Role-Based Authentication

The application implements role-based authentication.

User information is stored in the Flask session after successful login:

```python
session["user_id"] = user.id
session["username"] = user.username
session["role"] = user.role
```

The user's role determines which dashboard they can access.

### Supported Roles

* **Admin**
* **Student**

---

# 👨‍💼 Admin Dashboard

Administrators are redirected to:

```text
/admin/dashboard
```

Routes verify that the logged-in user has the required role:

```python
if session.get("role") != "admin":
    return redirect(url_for("home"))
```

---

# 🎓 Student Dashboard

Students are redirected to:

```text
/student/dashboard
```

The route verifies the user's role before granting access.

---

# ⚠️ Role-Based Redirect Loop

During development, an `ERR_TOO_MANY_REDIRECTS` error occurred.

### Cause

The application was redirecting users back to the same dashboard route:

```python
return redirect(url_for("dashboard"))
```

This resulted in a loop:

```text
/dashboard
    ↓
/dashboard
    ↓
/dashboard
    ↓
...
```

### Solution

Users are now redirected directly to their role-specific dashboards:

```text
Admin   → /admin/dashboard
Student → /student/dashboard
```

This prevents the redirect loop and keeps dashboard routing explicit.

---

# ☁️ Vercel Deployment

The Flask application was deployed to Vercel.

The production environment uses the following dependencies:

```text
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
```

These dependencies should be listed in `requirements.txt`.

---

# ⚠️ Vercel Build Error: requirements.txt Encoding

During deployment, Vercel initially returned:

```text
Failed to parse requirements.txt
Unexpected '�'
```

### Cause

The `requirements.txt` file had been saved using **UTF-16 LE encoding**, which introduced characters that Vercel's dependency parser could not interpret correctly.

### Solution

The file was converted to **UTF-8** using VS Code:

```text
VS Code
   ↓
Bottom-right encoding indicator
   ↓
UTF-16 LE
   ↓
Save with Encoding
   ↓
UTF-8
```

After converting the file to UTF-8, the Vercel deployment completed successfully.

---

# 🧪 Troubleshooting Summary

| Issue                              | Cause                                        | Solution                                         |
| ---------------------------------- | -------------------------------------------- | ------------------------------------------------ |
| Supabase hostname resolution error | Incorrect database connection string         | Verify the Supabase PostgreSQL connection string |
| Docker app inaccessible            | Incorrect port mapping                       | Use `docker run -p 5000:5000 testapp`            |
| `0.0.0.0` not opening in browser   | `0.0.0.0` is a bind address                  | Open `http://localhost:5000`                     |
| Alembic `%` interpolation error    | `%` interpreted by config parser             | Escape `%` as `%%`                               |
| Alembic metadata error             | SQLAlchemy metadata not connected to Alembic | Set `target_metadata = Base.metadata`            |
| Redirect loop                      | Dashboard redirects to itself                | Redirect directly to role-specific dashboards    |
| Vercel `Unexpected �` error        | `requirements.txt` encoded as UTF-16 LE      | Save the file as UTF-8                           |

---

# 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and activate the virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`:

```env
DATABASE_URL=your_supabase_postgresql_connection_string
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

Using Flask:

```bash
flask run
```

Or using Gunicorn:

```bash
gunicorn -b 0.0.0.0:5000 app:app
```

### 7. Open the application

```text
http://localhost:5000
```

---

# 📌 Current Status

The project currently includes:

* ✅ Flask backend
* ✅ Supabase PostgreSQL database
* ✅ SQLAlchemy ORM
* ✅ Alembic database migrations
* ✅ Role-based authentication
* ✅ Admin dashboard
* ✅ Student dashboard
* ✅ Session-based user authentication
* ✅ Gunicorn production server
* ✅ Docker containerization
* ✅ Vercel deployment
* ✅ Production database connectivity

---

# 🌐 Production

The application is currently deployed at:

**https://lms-system-dev.vercel.app/**

---

# 📄 License

This project is currently intended for educational and development purposes.












