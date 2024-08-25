import json
from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )
from sqlalchemy.sql import func

from main.authentication.models import User
from main.utils import user_required

from .models import Quiz, QuizQuestion, Topic, db
from main.course.models import Course, Performance
from datetime import timedelta
# from ... import bcrypt 

SESSION_TIMEOUT = timedelta(seconds=10)
qroute_bp = Blueprint('practice', __name__)
    
ACTIVE_SESSIONS_FILE = 'active_sessions.json'

@qroute_bp.route('/practice/<string:user_id>/<string:course_id>')
@user_required
def quiz(user_id, course_id):
    messages = get_flashed_messages(with_categories=True)
    topics = request.args.get('topics').split(",")
    mode = request.args.get('mode')
    time = int(request.args.get('time', 10))  # Default to 10 seconds
    num_questions = int(request.args.get('num_questions')) 
    order = request.args.get('order', 'orderly') 
    # course = Course.query.get_or_404(course_id)
    quizzes = Quiz.query.join(Topic).filter(
        Quiz.topic_id == Topic.id,
        Topic.id.in_(topics),
        Topic.course_id == course_id
    )
    if order == 'shuffled':
        quizzes = quizzes.order_by(func.random())
    
    if num_questions > 0:
        quizzes = quizzes.limit(num_questions)

    performance = Performance.query.filter_by(user_id=user_id, course_id=course_id).first()
    quizzes = quizzes.all()
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

    return render_template('pages/quiz_answers.html', time=time, performance_id=performance.id, course_id=course_id, user_id=user_id, messages=messages, mode=mode, quizzes=quizzes_json, enum = enumerate, len=len, topics=topics)

@qroute_bp.route('/exam/<string:user_id>/<string:course_id>')
@user_required
def exam(user_id, course_id):
    messages = get_flashed_messages(with_categories=True)
    topics = request.args.get('topics')
    mode = request.args.get('mode')
    hours = request.args.get('hours')
    minutes = request.args.get('minutes')

    course = Course.query.get_or_404(course_id)
    return render_template('pages/quiz.html', course_id=course_id, user_id=user_id, messages=messages, quizzes=course.quizzes, enum = enumerate,  mode=mode, topics=topics, hours=hours, minutes=minutes)

@qroute_bp.route('/quiz/setstudymode/<string:user_id>/<string:course_id>')
@user_required
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


@qroute_bp.route('/course-lessons/<string:course_id>')
@user_required
def course_lessons(course_id):
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    # course = Course.query.get_or_404(course_id)
    return render_template("pages/study.html", course="course", user=user)


@qroute_bp.route('/course-quiz/<string:course_id>')
@user_required
def course_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    # Get query parameters
    years = request.args.get('years')
    questions_limit = request.args.get('questions', type=int, default=10)

    # Parse years if provided
    year_list = years.split(',') if years else []

    # Filter quizzes by course

    # Filter questions by course and year
    quiz_questions_query = QuizQuestion.query.filter_by(course_id=course_id)
    
    if year_list:
        quiz_questions_query = quiz_questions_query.filter(QuizQuestion.year.in_(year_list))
    
    if questions_limit > 0:
        quiz_questions_query = quiz_questions_query.limit(questions_limit)
    
    quiz_questions = quiz_questions_query.all()

    return render_template(
        'pages/quiz_test.html',
        course=course,
        user=user,
        quizzes=[],
        quiz_questions=quiz_questions,
        enumerate=enumerate,
        len=len,
        questions_limit=questions_limit,
        years=years
    )

@qroute_bp.route('/theory-quiz/<string:course_id>')
@user_required
def theory_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    return render_template('pages/theory-quiz.html', course=course, user=user, enumerate=enumerate, len=len)

@qroute_bp.route('/gamma-quiz/<string:course_id>')
@user_required
def gamma_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    return render_template('pages/gamma-quiz.html', course=course, user=user, enumerate=enumerate, len=len)

@qroute_bp.route('/submit-quiz/<string:course_id>', methods=['POST'])
@user_required
def submit_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    user = User.query.get_or_404(session.get('user_id'))
    user_answers = []
    years = request.args.get('years')
    questions_limit = request.args.get('questions', type=int, default=10)

    # Parse years if provided
    year_list = years.split(',') if years else []

    # Filter quizzes by course

    # Filter questions by course and year
    quiz_questions_query = QuizQuestion.query.filter_by(course_id=course_id)
    
    if year_list:
        quiz_questions_query = quiz_questions_query.filter(QuizQuestion.year.in_(year_list))
    
    if questions_limit > 0:
        quiz_questions_query = quiz_questions_query.limit(questions_limit)
    
    quiz_questions = quiz_questions_query.all()
    score = 0
    for index, quiz in enumerate(quiz_questions):
        answer = request.form.get(f'question{index}')
        user_answers.append(answer)
        if quiz.answer == answer:
            score += 1
    
    performance = Performance.query.filter_by(course_id=course_id, user_id=user.id).first()

    if performance.user_id != user.id:
        flash('Unauthorized action', 'danger')
        return redirect('/courses')
    
    if score is not None:
        new_score_value = float(score)
        performance.add_score(new_score_value, len(course.quizzes))  # Adds a new score and manages the score count

        # if average is not None:
        #     performance.average = int(average)
        # if progress is not None:
        #     performance.progress = int(progress)
        
        db.session.commit()
    
    return render_template('pages/quiz_answers.html', enumerate=enumerate, len=len, user=user, course=course, quizzes=quiz_questions, user_answers=user_answers)
