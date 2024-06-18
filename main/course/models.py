import uuid

from main import db

class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_name = db.Column(db.String(125))
    url = db.Column(db.String(125))
    no_of_topics = db.Column(db.Integer)
    # no_of_questions = db.Column(db.Integer, default=0)
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', backref='courses', lazy=True)

class Performance(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    score = db.Column(db.Integer, default=0)
    average = db.Column(db.Integer, default=0)
    progress = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='performances', lazy=True)
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='performances', lazy=True)