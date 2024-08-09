from datetime import datetime
import uuid

from main import db


class Topic(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50))
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('topics', cascade='all, delete-orphan'), lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    
class Summary(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text)
    keynote = db.Column(db.Text)
    topic_id = db.Column(db.String(36), db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', backref=db.backref('summaries', cascade='all, delete-orphan'), lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
class Quiz(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_id = db.Column(db.String(36), db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', backref='quizzes', lazy=True)
    year = db.Column(db.String(60))
    type_ = db.Column(db.String(60), default="obj")
    question_text = db.Column(db.Text)
    answer = db.Column(db.Text)
    hint = db.Column(db.Text)
    instructions = db.Column(db.Text)
    img = db.Column(db.String(120), nullable=True)
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('quizzes', cascade='all, delete-orphan'), lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    options = db.relationship('Option', primaryjoin="and_(Option.quiz_id == Quiz.id, Option.option_type == 'quiz')", backref='quiz', lazy=True)

class QuizQuestion(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_name = db.Column(db.String(60))
    year = db.Column(db.String(60))
    type_ = db.Column(db.String(60), default="obj")
    question_text = db.Column(db.Text)
    answer = db.Column(db.Text)
    hint = db.Column(db.Text)
    instructions = db.Column(db.Text)
    img = db.Column(db.String(120), nullable=True)
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('quiz_questions', cascade='all, delete-orphan'), lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    options = db.relationship('Option', primaryjoin="and_(Option.quiz_question_id == QuizQuestion.id, Option.option_type == 'quiz_question')", backref='quiz_question', lazy=True)

class Option(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    option_text = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    option_type = db.Column(db.String(20))  # 'quiz' or 'quiz_question'
    quiz_id = db.Column(db.String(36), db.ForeignKey('quiz.id'), nullable=True)
    quiz_question_id = db.Column(db.String(36), db.ForeignKey('quiz_question.id'), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional: Add a method to enforce constraints or validate `option_type`
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.option_type == 'quiz' and not self.quiz_id:
            raise ValueError("Quiz ID must be provided for quiz options")
        if self.option_type == 'quiz_question' and not self.quiz_question_id:
            raise ValueError("QuizQuestion ID must be provided for quiz question options")

