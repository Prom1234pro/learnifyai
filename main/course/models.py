import uuid
from datetime import datetime

from main import db

class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_name = db.Column(db.String(125))
    url = db.Column(db.String(125))
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', backref='courses', lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def no_of_topics(self):
        return len(self.topics)
    
    @property
    def no_of_questions(self):
        return len(self.quizzes)
    
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
        return float(len(self.scores) / 5) * 100
    
  
    def add_score(self, new_score_value):
        # Create a new score
        new_score = Score(score=new_score_value, performance_id=self.id)
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
    performance_id = db.Column(db.String(36), db.ForeignKey('performance.id'), nullable=False)
    performance = db.relationship('Performance', backref='scores', lazy=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    