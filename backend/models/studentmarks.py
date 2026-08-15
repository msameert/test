from db import db

class Studentmark (db.Model) :
    __tablename__ = "studentmarks"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)

    obtained_marks = db.Column(db.Float, nullable=False)

    student = db.relationship("Student", backref="studentmarks")
    assessment = db.relationship("Assessment", backref="studentmarks")
