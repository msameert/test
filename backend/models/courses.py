from db import db

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    course_name = db.Column(db.String(200), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)

    department_id = db.Column(db.Integer,db.ForeignKey("departments.id"),nullable=False)