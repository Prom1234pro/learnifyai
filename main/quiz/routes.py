import json
from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )

from .models import Quiz, Topic, db
from main.course.models import Course
from datetime import timedelta
# from ... import bcrypt 

SESSION_TIMEOUT = timedelta(seconds=10)
qroute_bp = Blueprint('practice', __name__)

def is_auth():
    if 'user' in session:
        return True
    else:
        return False
    
ACTIVE_SESSIONS_FILE = 'active_sessions.json'

@qroute_bp.route('/practice/<string:user_id>/<string:course_id>')
def quiz(user_id, course_id):
    messages = get_flashed_messages(with_categories=True)
    topics = request.args.get('topics').split(",")
    # print(topics)
    mode = request.args.get('mode')
    # course = Course.query.get_or_404(course_id)
    quizzes = Quiz.query.join(Topic).filter(
        Quiz.topic_id == Topic.id,
        Topic.id.in_(topics),
        Topic.course_id == course_id
    ).all()
    # print(quizzes)
    quizzes_data = [
        {
            "question_text": quiz.question_text,
            "type_": quiz.type_,
            "hint": quiz.hint,
            "subject": quiz.topic.course.course_name,
            "topic": quiz.topic.name,
            "options": [
                {"option_text": option.option_text, "is_correct": option.is_correct}
                for option in quiz.options
            ]
        }
        for quiz in quizzes
    ]
    quizzes_json = json.dumps(quizzes_data)

    if not is_auth():     
        return redirect(f"/logout/{user_id}")
    return render_template('pages/quiz.html', course_id=course_id, user_id=user_id, messages=messages, mode=mode, quizzes=quizzes_json, enum = enumerate, len=len, topics=topics)

@qroute_bp.route('/exam/<string:user_id>/<string:course_id>')
def exam(user_id, course_id):
    messages = get_flashed_messages(with_categories=True)
    topics = request.args.get('topics')
    mode = request.args.get('mode')
    hours = request.args.get('hours')
    minutes = request.args.get('minutes')

    course = Course.query.get_or_404(course_id)
    if not is_auth():     
        return redirect(f"/logout/{user_id}")
    return render_template('pages/quiz.html', course_id=course_id, user_id=user_id, messages=messages, quizzes=course.quizzes, enum = enumerate,  mode=mode, topics=topics, hours=hours, minutes=minutes)

@qroute_bp.route('/quiz/setstudymode/<string:user_id>/<string:course_id>')
def set_studymode(user_id, course_id):
    mode = request.args.get('mode')
    topics = request.args.get('topics')
    hours = request.args.get('hours')
    minutes = request.args.get('minutes')
    
    course = Course.query.get_or_404(course_id)
    group_id = course.group_id
    if mode == "practice":
        return redirect(f'/practice/{user_id}/{course_id}?mode={mode}&topics={topics}')
    
    if not hours or int(hours) < 0 or minutes== None or int(minutes) < 0:
        flash("Set a valid time", 'danger')
        return redirect(f'/courses/{user_id}/{group_id}')
    return redirect(f'/exam/{user_id}/{course_id}?mode={mode}&topics={topics}&hours={hours}&minutes={minutes}')



