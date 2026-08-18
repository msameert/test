from db import db

class Assessment (db.Model) :
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    total_marks = db.Column(db.Float, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)

    course = db.relationship("Course", backref="assessments")
    faculty = db.relationship("Faculty", backref="assessments")

