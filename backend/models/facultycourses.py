from db import db

class FacultyCourse(db.Model):
    __tablename__ = "faculty_courses"

    id = db.Column(db.Integer, primary_key=True)

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    semester_id = db.Column(
        db.Integer,
        db.ForeignKey("semesters.id"),
        nullable=False
    )

    faculty = db.relationship("Faculty", backref="faculty_courses")
    course = db.relationship("Course", backref="faculty_courses")
    semester = db.relationship("Semester", backref="faculty_courses")