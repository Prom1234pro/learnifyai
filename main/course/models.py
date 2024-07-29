import uuid
from datetime import datetime
from flask import session
from itertools import cycle

def color_generator():
    colors = ['primary', 'success', 'danger', 'info', 'warning']
    while True:
        for color in colors:
            yield color

color_gen = color_generator()

from main import db

class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_name = db.Column(db.String(125))
    _for = db.Column(db.String(125)) #post utme
    description = db.Column(db.String(125))
    progress = db.Column(db.Integer, default=0)
    url = db.Column(db.String(125))
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', backref='courses', lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    has_summary = db.Column(db.Boolean, default=False)
    
    
    # @property
    # def color(self):
    #     return next(color_gen)

    def to_dict(self):
        return {
            'id': self.id,
            'course_name': self.course_name,
            '_for': self._for,
            'description': self.description,
            'progress': self.progress,
            'url': self.url,
            'has_summary': self.has_summary,
            'group_id': self.group_id,
            'date_created': self.date_created.isoformat(),
            'date_updated': self.date_updated.isoformat(),
            'group_name': self.group.name,
            'color': self.color,
            'no_of_topics': self.no_of_topics,  # Assuming this is a property or attribute
            'performance': {
                'progress': self.performance.progress  # Assuming performance is related and has a progress attribute
            }
        }
    
    @property
    def no_of_topics(self):
        return len(self.topics)
    
    @property
    def no_of_questions(self):
        return len(self.quizzes)
    
    @property
    def performance(self):
        user_id = session.get('user_id')
        return Performance.query.filter_by(course_id=self.id, user_id=user_id).first()


    
class Performance(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    score = db.Column(db.Integer, default=0)
    average = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='performances', lazy=True)
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='performances', lazy=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def progress(self):
        return int(float(len(self.scores) / 5) * 100)
    
  
    def add_score(self, new_score_value, total):
        # Create a new score
        new_score = Score(score=new_score_value, total_questions=total, performance_id=self.id)
        db.session.add(new_score)
        db.session.commit()

        # Check the number of scores and remove the oldest if more than 4
        scores = Score.query.filter_by(performance_id=self.id).order_by(Score.timestamp).all()
        if len(scores) > 4:
            db.session.delete(scores[0])
            db.session.commit()

class Score(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer)
    performance_id = db.Column(db.String(36), db.ForeignKey('performance.id'), nullable=False)
    performance = db.relationship('Performance', backref='scores', lazy=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def percentage(self):
        if self.total_questions is not None:
            return round((self.score / self.total_questions) * 100, 2)
        else:
            return 0