from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import object_session
import uuid
from datetime import datetime, timedelta
from main import db
from main.cluster.models import Group

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

