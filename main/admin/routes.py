import json
import os.path
import uuid
from flask import Blueprint, render_template, request, jsonify, send_file, url_for, abort, session
import requests
from main.authentication.models import User, db
from main.course.models import Course
from main.utils import admin_required, user_required, validate_format
from flask_mail import Message
from main import bcrypt, mail

from main.quiz.topic import create_topic
# from main.utils import load_active_sessions, save_active_sessions, SESSION_TIMEOUT
from main.quiz.models import Quiz, Option, QuizQuestion
from main.cluster.models import Group
import string, secrets

admin_bp = Blueprint('admin', __name__)

def generate_verification_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_verification_email(user):
    token = generate_verification_token()  # Implement this method in your User model
    user.verification_token=token
    msg = Message('Verify Your Account', sender='promiseimadonmwinyi@example.com', recipients=[user.email])
    link = url_for('auth.verify_email', token=token, _external=True)
    msg.body = f'Please click the link to verify your account: {link}'
    mail.send(msg)

@admin_bp.route('/ailearnify/create-admin', methods=['POST'])
@admin_required
def create_admin():
    if request.method == "POST":
        data = request.get_json()
        password = data.get('password')
        username = data.get('username')
        email = data.get('email')

        if not password or not username or not email:
            return jsonify({"error": "Invalid body"}), 400

        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            is_admin=True,
            email_verified=False
        )
        send_verification_email(new_user)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": "Success"}), 201

    return abort(404)


@admin_bp.route('/admin-login-to-system', methods=['POST'])
def admin_login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and is an admin
        if user and user.is_admin:
            # Check if user is verified
            if not user.email_verified:
                return jsonify({"error": "Email not verified"}), 403
            
            # Check if the password is correct
            if bcrypt.check_password_hash(user.password, password):
                session["user_id"] = user.id
                user.is_logged_in = True
                db.session.commit()
                return jsonify({"success": "Logged in successfully"}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return "hi me"

@admin_bp.route('/make_admin/<user_id>', methods=['POST'])
@admin_required
def make_admin(user_id):
    if request.method == 'POST':
        user = User.query.get_or_404(user_id)
        user.is_admin = True
        db.session.commit()
        return jsonify({"success":"user made an admin"})
    return abort(404)

@admin_bp.route('/admin/groups')
@admin_required
def group():
    all_groups =Group.query.all()
    all_groups_data = [{'id': group.id, 'name': group.name, 'image_filename': group.image_filename} for group in all_groups]
    return jsonify({'all_groups': all_groups_data}), 200

@admin_bp.route('/ailearnify/update/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    if request.method == "PUT":
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.is_admin = data.get('is_admin', user.is_admin)
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  # Make sure to hash the password in real implementation
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    return abort(404)

@admin_bp.route('/admin/get-all-users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    users_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'email_verified': user.email_verified,
            'is_logged_in': user.is_logged_in,
            'is_premium_user': user.is_premium_user,
            'user_plan': user.user_plan,
            # Add any other fields you want to include
        }
        users_list.append(user_data)
    return jsonify(users_list), 200

@admin_bp.route('/upgrade-to-premium/<username>', methods=['GET', 'POST'])
@admin_required
def upgrade_to_premium(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        data = request.get_json()
        user_plan = data.get('user_plan')
        if user.is_premium_user and user.user_plan == user_plan:
            return jsonify({"message": "user already a premium user"})
        
        user.is_premium_user = True
        user.user_plan = user_plan
        db.session.commit()
        
        return jsonify({"message": "success"})
    
    return abort(404)


@admin_bp.route('/admin/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    if request.method == "DELETE":
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return abort(404)

@admin_bp.route('/group/<group_id>/courses', methods=['GET'])
@admin_required
def get_courses_by_group(group_id):
    if request.method == 'GET':
        courses = Course.query.filter_by(group_id=group_id).all()
        
        if not courses:
            return jsonify({"error": "No courses found for the specified group ID"}), 404
        
        courses_list = [{
            "id": course.id,
            "course_name": course.course_name,
            "url": course.url,
            "no_of_topics": course.no_of_topics,
            "group_id": course.group_id
        } for course in courses]
        
        return jsonify(courses_list), 200

    return abort(404)



@admin_bp.route('/admin/create-quiz/obj', methods=['POST'])
@admin_required
def create_quiz_obj():
    if request.method == 'POST':
        # current_user_id = get_jwt_identity()  # Get current user's ID from JWT token
        # current_user = User.query.get(current_user_id)
        # if not current_user.is_admin:
        #     return jsonify({'message': 'Unauthorized'})
        data = request.json  # Get JSON data from the request body

        if 'quizzes' not in data or not isinstance(data['quizzes'], list):
            return jsonify({'error': 'No quizzes data provided or invalid format'}), 400

        try:
            quizzes = data['quizzes']
            course_id = data['course_id']
            topic = data['topic']
            summaries = data['summaries']
            topic_id = topic['topic_id']
            if topic['topic_id']:
                topic_id = topic['topic_id']
            else:
                topic_id = create_topic(summaries, name=topic['topic_name'], course_id=course_id)
            for quiz_data in quizzes:
                quiz = Quiz(topic_id=topic_id,
                            hint="No hint",
                            instructions=quiz_data['instructions'],
                            question_text=quiz_data['question_text'],
                            course_id=course_id)

                if 'options' in quiz_data and isinstance(quiz_data['options'], list):
                    options_data = quiz_data['options']
                    for option_data in options_data:
                        option = Option(option_text=option_data['option_text'], is_correct=option_data['is_correct'], quiz=quiz)
                        quiz.options.append(option)
                        if option_data['is_correct']:
                            quiz.answer = option_data['option_text']

                db.session.add(quiz)

            db.session.commit()

            return jsonify({'message': 'Quizzes created successfully', 'topic_id':topic_id}), 201

        except Exception as e:
            return jsonify({'error': f'unknown error{e}'}), 401

    return abort(404)


def create_quiz_obj_(path):
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return jsonify({'error': 'JSON file not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Error decoding JSON file'}), 400
    
    if 'quizzes' not in data or not isinstance(data['quizzes'], list):
        return jsonify({'error': 'No quizzes data provided or invalid format'}), 400
    
    course_id = data.get('course_id')
    year = data.get('year')
    
    # Validate required fields
    if not course_id:
        return jsonify({'error': 'Course ID is required'}), 400
    
    quizzes = data['quizzes']
    
    for quiz_data in quizzes:
        try:
            quiz = QuizQuestion(
                topic_name=quiz_data.get('topic_name'),
                year=year,
                type_=quiz_data.get('type_', 'obj'),
                question_text=quiz_data.get('question_text', ''),
                answer=quiz_data.get('answer', ''),
                hint=quiz_data.get('hint', 'No hint'),
                instructions=quiz_data.get('instructions', 'No instructions'),
                img=quiz_data.get('img'),
                course_id=course_id
            )
            db.session.add(quiz)
            db.session.commit()
            
            if 'options' in quiz_data and isinstance(quiz_data['options'], list):
                options_data = quiz_data['options']
                for option_data in options_data:
                    option = Option(
                        option_text=option_data['option_text'],
                        is_correct=option_data['is_correct'],
                        option_type='quiz_question',
                        quiz_id=None,
                        quiz_question_id=quiz.id,
                    )
                    db.session.add(option)
                    if option.is_correct:
                        quiz.answer = option.option_text
                    
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error processing quiz: {e}'}), 400
    
    try:
        db.session.commit()
        return jsonify({'message': 'Quizzes created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error committing to database: {e}'}), 500

    return abort(404)

@admin_bp.route('/admin/delete-quizzes/<course_id>', methods=['DELETE'])
@admin_required
def delete_quizzes_by_course(course_id):
    try:
        # Find all quizzes related to the course
        quizzes = Quiz.query.filter_by(course_id=course_id).all()
        if not quizzes:
            return jsonify({'message': 'No quizzes found for the provided course ID'}), 404

        # Delete all quizzes related to the course
        for quiz in quizzes:
            db.session.delete(quiz)
        
        db.session.commit()
        return jsonify({'message': 'All quizzes deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {e}'}), 500

@admin_bp.route('/admin/delete-quiz-questions/<course_id>', methods=['DELETE'])
@admin_required
def delete_quiz_questions_by_course(course_id):
    try:
        # Find all quiz questions related to the course
        quiz_questions = QuizQuestion.query.filter_by(course_id=course_id).all()
        if not quiz_questions:
            return jsonify({'message': 'No quiz questions found for the provided course ID'}), 404

        # Delete all quiz questions related to the course
        for quiz_question in quiz_questions:
            db.session.delete(quiz_question)
        
        db.session.commit()
        return jsonify({'message': 'All quiz questions deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {e}'}), 500


@admin_bp.route('/admin/create-quiz/gamma', methods=['POST'])
@admin_required
def create_quiz_gamma():
    if request.method == 'POST':
        data = request.json 

        if 'quizzes' not in data or not isinstance(data['quizzes'], list):
            return jsonify({'error': 'No quizzes data provided or invalid format'}), 400

        try:
            quizzes = data['quizzes']
            course_id = data['course_id']
            topic = data['topic']
            if topic['topic_id']:
                topic_id = topic['topic_id']
            else:
                topic_id = create_topic(name=topic['topic_name'], summary=topic["summary"], course_id=course_id)
            
            for quiz_data in quizzes:
                # Create a new Quiz object
                quiz = Quiz(topic_id=topic_id,
                            answer=quiz_data['answer'],
                            type_=quiz_data['type_'],
                            hint=quiz_data['hint'],
                            instructions=quiz_data['instructions'],
                            question_text=quiz_data['question_text'],
                            course_id=course_id)
                db.session.add(quiz)

            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'Quizzes created successfully', 'topic_id':topic_id}), 201

        except Exception as e:
            return jsonify({'error': f'unknown error{e}'}), 401

    return abort(404)


@admin_bp.route('/admin/create/<string:user_id>', methods=['POST'])
@admin_required
def generate_group_key(user_id):
    if request.method == 'POST':
        data = request.form
        if not data:
            return jsonify({"error": "No data provided"})
        
        no_of_users = data.get('max-occupancy')
        # group_admin_id = data.get('group_admin_id')
        user = User.query.get_or_404(user_id)
        if not user.is_admin:
            return jsonify({"error": "you must be an admin"})
        group = Group(
            name = data.get('group-name'),
            school = data.get('school'),
            max_no_users=no_of_users,
            group_admin_id=user_id,
            group_key=str(uuid.uuid4()),
        )
        db.session.add(group)
        db.session.commit()
        return jsonify({"id":group.group_key})
    else:
        return abort(404)

@admin_bp.route('/download/<filename>', methods=['GET'])
@admin_required
def download_file(filename):
    try:
        path = f'../instance/{filename}'
        return send_file(path, as_attachment=True)
    except Exception as e:
        return str(e)
    

def read_text(text):
    lines = text.splitlines()
    
    course_id = None
    topic_name = None
    instructions = None
    year = None
    quizzes = []
    
    current_question = {}
    current_options = []

    def add_question():
        if "question_text" in current_question and current_options:
            current_question["topic_name"] = topic_name
            current_question["options"] = current_options.copy()
            quizzes.append(current_question.copy())
            current_question.clear()
            current_options.clear()

    for line in lines:
        line = line.strip()
        
        if line.startswith("Course ID:"):
            course_id = line.split(":", 1)[1].strip()
        
        elif line.startswith("Topic Name:"):
            topic_name = line.split(":", 1)[1].strip()
        
        elif line.startswith("Current Instruction:"):
            instructions = line.split(":", 1)[1].strip()
        
        elif line.startswith("Year:"):
            year = line.split(":", 1)[1].strip()
        
        elif line and not line.startswith(("Course ID:", "Topic Name:", "Topic ID:", "Year:", "Instruction:")):
            if line.endswith("?"):
                add_question()
                current_question["question_text"] = line
                current_question["instructions"] = instructions  
            else:
                option_parts = line.rsplit(",", 1)
                option_text = option_parts[0].strip()
                is_correct = option_parts[1].strip().lower() == "true" if len(option_parts) > 1 else False
                current_options.append({
                    "option_text": option_text,
                    "is_correct": is_correct
                })

    add_question()

    return {
        "course_id": course_id,
        "year": year,
        "quizzes": quizzes
    }



@admin_bp.route('/convert-text-to-json', methods=['POST'])
@admin_required
def convert_text_to_json():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data from the request body
        text = data.get('text')    # Extract the text from the data
        user_id = session.get('user_id')
        user = User.query.get_or_404(user_id)
        try:
            is_valid, message = validate_format(text)
            if not is_valid:
                return jsonify({'error': message}), 400
            
            json_data = read_text(text)  # Convert text to JSON
            directory = user.username
            json_file_path = os.path.join(directory, 'temp_data.json')
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4, separators=(',', ': '))
 
            create_quiz_obj_(json_file_path)
            
            return jsonify(json_data), 201
        except Exception as e:
            return jsonify({'error': f'Error processing text: {e}'}), 400

    return jsonify({'error': 'Invalid request method'}), 405


@admin_bp.route('/preview-json', methods=['POST'])
@admin_required
def preview_json():
    if request.method == 'POST':
        data = request.get_json()  # Extract JSON data from the request body
        text = data.get('text')    # Retrieve the text field from the data
        user_id = session.get('user_id')
        user = User.query.get_or_404(user_id)
        try:
            # Validate the format of the provided text
            is_valid, message = validate_format(text)
            if not is_valid:
                return jsonify({'error': message}), 400
            
            # Convert the validated text to JSON
            json_data = read_text(text)
            html_content = render_template('pages/preview.html', user=user, data=json_data, enumerate=enumerate)
            
            # Return the HTML content as a JSON response
            return jsonify({'html': html_content}), 200
        
        except Exception as e:
            # Return an error message if an exception occurs
            return jsonify({'error': f'Error processing text: {e}'}), 400
