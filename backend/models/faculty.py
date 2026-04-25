from db import db

class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=True)
    course_name = db.Column(db.String(70), nullable=False)
    department = db.Column(db.String(100))
    designation = db.Column(db.String(100), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship("User", backref="faculty", uselist=False)