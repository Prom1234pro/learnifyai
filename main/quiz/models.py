import uuid

from main import db


class Topic(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50))
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='topics', lazy=True)

class Summary(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text)
    keynote = db.Column(db.Text)
    topic_id = db.Column(db.String(36), db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', backref='summaries', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_id = db.Column(db.String(36), db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', backref='quizzes', lazy=True)
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

