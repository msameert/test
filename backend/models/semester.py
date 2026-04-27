from db import db

class Semester(db.Model):
    __tablename__ = "semesters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Semester 1
    year = db.Column(db.Integer, nullable=False)

    department_id = db.Column(db.Integer,db.ForeignKey("departments.id"),nullable=False)