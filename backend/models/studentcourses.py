from db import db


class StudentCourse(db.Model):
    __tablename__ = "student_courses"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)

    course_id = db.Column(db.Integer,db.ForeignKey("courses.id"),nullable=False)

    semester_id = db.Column(db.Integer,db.ForeignKey("semesters.id"),nullable=False)

    marks = db.Column(db.Float)
    grade = db.Column(db.String(5))
    status = db.Column(db.String(20), default="enrolled")

    student = db.relationship("Student", backref="student_courses")
    course = db.relationship("Course", backref="student_courses")
    semester = db.relationship("Semester", backref="student_courses")