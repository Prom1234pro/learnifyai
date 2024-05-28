from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )
import uuid
import json
from ...models.models import db, Quiz, Quiz, Option, Course
from datetime import datetime, timedelta
from ... import bcrypt 

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
    topics = request.args.get('topics')
    mode = request.args.get('mode')
    course = Course.query.get_or_404(course_id)
    if not is_auth():     
        return redirect(f"/logout/{user_id}?return_url=/practice/{user_id}")
    return render_template('quiz.html', course_id=course_id, user_id=user_id, messages=messages, mode=mode, quizzes=course.quizzes, enum = enumerate, len=len, topics=topics)

@qroute_bp.route('/exam/<string:user_id>/<string:course_id>')
def exam(user_id, course_id):
    messages = get_flashed_messages(with_categories=True)
    topics = request.args.get('topics')
    mode = request.args.get('mode')
    hours = request.args.get('hours')
    minutes = request.args.get('minutes')

    course = Course.query.get_or_404(course_id)
    if not is_auth():     
        return redirect(f"/logout/{user_id}?return_url=/practice/{user_id}")
    return render_template('quiz.html', course_id=course_id, user_id=user_id, messages=messages, quizzes=course.quizzes, enum = enumerate,  mode=mode, topics=topics, hours=hours, minutes=minutes)

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



