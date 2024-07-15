from flask import url_for
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
    # wallet_balance = db.Column(db.Integer, default=0)
    full_name = db.Column(db.String(50))
    groups = db.relationship('Group', secondary=Groups, lazy='subquery',
        backref=db.backref('users', lazy=True))
    user_plan = db.Column(db.String(50))
    is_premium_user = db.Column(db.Boolean, default=False)
    referrer_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    
    referred_users = db.relationship('User', backref=db.backref('referrer', remote_side=[id]), lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    
    def refer_user(self, referred_user):
        print("referid", self.id, referred_user.id)
        referral = Referral(referrer_id=self.id, referred_id=referred_user.id)
        db.session.add(referral)
        db.session.commit()
    
    def earn_benefit(self):
        # Logic for earning benefits
        pass

    @property
    def referral_link(self):
        referralL = url_for('auth.create_user', referrer=self.username, _external=True)
        return referralL
    
    @property
    def referral_count(self):
        return len(self.referred_users)



class Referral(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    referrer_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    benefit_received = db.Column(db.Boolean, default=False)
    date_referred = db.Column(db.DateTime, default=datetime.utcnow)

    referrer = db.relationship('User', foreign_keys=[referrer_id], backref='referrals_made')
    referred = db.relationship('User', foreign_keys=[referred_id], backref='referred_by')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
