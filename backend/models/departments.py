from db import db

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)

    students = db.relationship("Student", backref="department")
    courses = db.relationship("Course", backref="department")
    semesters = db.relationship("Semester", backref="department")