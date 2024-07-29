from datetime import datetime
import uuid

from main import db


class Group(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120))
    cluster_handle = db.Column(db.String(120), unique=True, nullable=False)
    max_no_users = db.Column(db.Integer)
    current_no_users = db.Column(db.Integer, default=0)
    group_admin_id = db.Column(db.String(36))
    activated = db.Column(db.Boolean, default=False)
    school = db.Column(db.String(120))
    is_public = db.Column(db.Boolean, default=True)
    group_key = db.Column(db.String(120))
    pass_key = db.Column(db.String(120), default=1234)
    image_filename = db.Column(db.String(120), nullable=True)
    motto = db.Column(db.String(120))
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    owned_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(120))
    creator = db.relationship("User", foreign_keys=[created_by])
    owner = db.relationship("User", foreign_keys=[owned_by])
    school = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    