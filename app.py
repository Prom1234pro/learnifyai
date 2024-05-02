from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/groups')
def group():
    return render_template('group.html')

@app.route('/practice')
def quiz():
    return render_template('quiz.html')

@app.route('/courses')
def course():
    return render_template('course.html')

if __name__ == '__main__':
    app.run(debug=True)