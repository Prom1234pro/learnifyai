from datetime import datetime
from main import db


class PastQuestion(db.Model):
    __tablename__ = 'past_questions'

    id = db.Column(db.SInteger, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)
    correct_option = db.Column(db.String(100), nullable=False)
    optional_text = db.Column(db.Text)
    year = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(100), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 