from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import object_session
import uuid
from datetime import datetime, timedelta

db = SQLAlchemy()

Groups = db.Table('groups',
    db.Column('group_id', db.String(36), db.ForeignKey('group.id'), primary_key=True),
    db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_logged_in = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    last_activity_time = db.Column(db.DateTime)  
    verification_token = db.Column(db.String(60))  
    groups = db.relationship('Group', secondary=Groups, lazy='subquery',
        backref=db.backref('users', lazy=True))
    is_premium_user = db.Column(db.Boolean, default=False)
    
    def update_activity_time(self):
        self.last_activity_time = datetime.utcnow()
        db.session.commit()

    def is_inactive(self):
        if not self.last_activity_time:
            return True  # User has never been active
        # Check if the difference between current time and last activity time exceeds 24 hours
        return (datetime.utcnow() - self.last_activity_time) > timedelta(hours=24)

    @property
    def activated_groups(self):
        return object_session(self).query(Group).with_parent(self).filter(Group.activated == True).all()
    
    # def set_session_id(self, session_id):
    #     self.session_id = session_id
    #     db.session.commit()

    # def update_last_login_ip(self, ip_address):
    #     self.last_login_ip = ip_address
    #     db.session.commit()

class Group(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120))
    max_no_users = db.Column(db.Integer)
    current_no_users = db.Column(db.Integer, default=0)
    group_admin_id = db.Column(db.String(36))
    activated = db.Column(db.Boolean, default=False)
    school = db.Column(db.String(120))
    is_public = db.Column(db.Boolean, default=True)
    group_key = db.Column(db.String(120))
    pass_key = db.Column(db.String(120), default=1234)


class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_name = db.Column(db.String(125))
    url = db.Column(db.String(125))
    no_of_topics = db.Column(db.Integer)
    # no_of_questions = db.Column(db.Integer, default=0)
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', backref='courses', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = db.Column(db.String(60))
    type_ = db.Column(db.String(60), default="obj")
    question_text = db.Column(db.Text)
    answer = db.Column(db.Text)
    hint = db.Column(db.Text)
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='quizzes', lazy=True)

class Option(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    option_text = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship('Quiz', backref='options', lazy=True)

