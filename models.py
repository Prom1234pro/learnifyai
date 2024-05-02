from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

Groups = db.Table('groups',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    Groups = db.relationship('Group', secondary=Groups, lazy='subquery',
        backref=db.backref('users', lazy=True))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_of_users = db.Column(db.Integer)
    group_admin = db.Column(db.Integer)
    users = db.relationship('User', secondary=Groups, lazy='subquery',
        backref=db.backref('groups', lazy=True))
    course = db.relationship('Course', backref='group', lazy=True)
    group_key = db.Column(db.String(120))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_of_users = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    quiz = db.relationship('Quiz', backref='course', lazy=True)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_of_users = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     group = db.relationship('Group', backref='', lazy=True)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"

# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('.id'), nullable=False)
#     no_of_users = db.Column(db.Integer)