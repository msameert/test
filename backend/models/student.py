from db import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), unique=True, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=True)
    enroll_year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, default='active')
    gender = db.Column(db.String(50), nullable=False)
    cnic = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", backref="student")
