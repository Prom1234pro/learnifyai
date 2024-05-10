from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )
import uuid
import json
from ..models.models import db, Quiz, Quiz, Option, Course
from datetime import datetime, timedelta
from .. import bcrypt 

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
    course = Course.query.get_or_404(course_id)
    if not is_auth():     
        return redirect(f"/logout/{user_id}?return_url=/practice/{user_id}")
    return render_template('quiz.html', user_id=user_id, messages=messages, quizzes=course.quizzes, enum = enumerate, len=len)


@qroute_bp.route('/admin/create-quiz', methods=['POST'])
def create_quiz():
    # user = None
    # if "user" in session:
    #     user = session["user"]
    # else:
    #     flash('User needs authorization to perform this action', 'warning')
    #     return redirect('/login-user')
    if request.method == 'POST':
        data = request.json  # Get JSON data from the request body

        if 'quizzes' not in data or not isinstance(data['quizzes'], list):
            return jsonify({'error': 'No quizzes data provided or invalid format'}), 400

        try:
            quizzes = data['quizzes']

            for quiz_data in quizzes:
                # Create a new Quiz object
                quiz = Quiz(topic=quiz_data['topic'], question_text=quiz_data['question_text'], course_id=quiz_data['course_id'])

                # Create options for the quiz
                if 'options' in quiz_data and isinstance(quiz_data['options'], list):
                    options_data = quiz_data['options']
                    for option_data in options_data:
                        # Create a new Option object
                        option = Option(option_text=option_data['option_text'], is_correct=option_data['is_correct'], quiz=quiz)
                        # Add the option to the quiz
                        quiz.options.append(option)

                # Add the quiz to the database session
                db.session.add(quiz)

            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'Quizzes created successfully'}), 201

        except Exception as e:
            return jsonify({'error': 'unknown error'}), 401

    return jsonify({'error': 'Method not allowed'}), 405