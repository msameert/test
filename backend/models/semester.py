from db import db

class Semester(db.Model):
    __tablename__ = "semesters"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False )
    name = db.Column(db.String(50), nullable=False)  # Spring 2025
    year = db.Column(db.Integer, nullable=False)    # 2025
    semester_number = db.Column(db.Integer, nullable=False)   # 1-8
    semester_type = db.Column(db.String(20), nullable=False)  # Fall, Summer, Spring

    department_id = db.Column(db.Integer,db.ForeignKey("departments.id"),nullable=True)