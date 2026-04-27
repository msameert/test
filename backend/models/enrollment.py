from db import db

class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)

    semester_id = db.Column(db.Integer,db.ForeignKey("semesters.id"),nullable=False)

    status = db.Column(db.String(50), default="active")

    student = db.relationship("Student", backref="enrollments")
    semester = db.relationship("Semester", backref="enrollments")