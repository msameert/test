from db import db

class SemesterCourse(db.Model):
    __tablename__ = "semester_courses"

    id = db.Column(db.Integer, primary_key=True)

    semester_id = db.Column(db.Integer,db.ForeignKey("semesters.id"),nullable=False)

    course_id = db.Column(db.Integer,db.ForeignKey("courses.id"),nullable=False)

    semester = db.relationship("Semester", backref="semester_courses")
    course = db.relationship("Course", backref="semester_courses")