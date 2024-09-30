from datetime import datetime
import uuid

from main import db


# PastQuestion model
class PastQuestion(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Stores options as a JSON object
    correct_option = db.Column(db.String(255), nullable=False)  # Correct option ID or text
    optional_text = db.Column(db.Text)  # For questions that contain instructions
    year = db.Column(db.Integer, nullable=False)
    school_code = db.Column(db.Integer, nullable=False)  # Unique code per school
    school = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)