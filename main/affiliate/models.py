from main import db
import uuid
from sqlalchemy.types import Enum
import enum


class ReferralStatus(enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    REJECTED = "Rejected"

class CommissionStatus(enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"


class Affiliate(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    affiliate_token = db.Column(db.String(255), unique=True, nullable=False)
    commission_rate = db.Column(db.Float, nullable=False)
    total_referrals = db.Column(db.Integer, default=0, nullable=False)
    total_earnings = db.Column(db.Float, default=0.0, nullable=False)

    user = db.relationship('User', backref='affiliate', lazy=True)



class Referrals(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    affiliate_id = db.Column(db.String(36), db.ForeignKey('affiliate.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    referral_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    status = db.Column(Enum(ReferralStatus), default=ReferralStatus.PENDING, nullable=False)

    affiliate = db.relationship('Affiliate', backref='referrals', lazy=True)
    user = db.relationship('User', backref='referrals', lazy=True)

class Commission(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    affiliate_id = db.Column(db.String(36), db.ForeignKey('affiliate.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    status = db.Column(Enum(CommissionStatus), default=CommissionStatus.PENDING, nullable=False)

    affiliate = db.relationship('Affiliate', backref='commissions', lazy=True)
