from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages, url_for
    )
import uuid
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from .topic import create_topic
# from main.utils import load_active_sessions, save_active_sessions, SESSION_TIMEOUT
from .models import db, Quiz, Option
from main.cluster.models import Group
from main.authentication.models import User
from main import bcrypt

ad_route_bp = Blueprint('admin', __name__)


@ad_route_bp.route('/admin/createadminuser', methods=['POST'])
def create_admin_user():
    data = request.get_json()
    
    # Check if user already exists in database
    existing_user = User.query.filter_by(email=data['email']).first()
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
    
    if existing_user:
        return jsonify({'message': 'User with that email already exists'}), 400
    
    # Create new user
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT token
    access_token = create_access_token(identity=new_user.id, additional_claims={'is_admin': True})
    return jsonify({'access_token': access_token}), 200

@ad_route_bp.route("/admin/login-admin", methods=["POST"])
def login_admin():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).one_or_none()
    if user is None:
        return jsonify({'error':'Not found'}), 404
    is_valid = bcrypt.check_password_hash(user.password, password)
    if not is_valid:
        return jsonify({'error':'Invalid password'}), 400

    access_token = create_access_token(identity=user.id, additional_claims={'is_admin': True})
    return jsonify({'access_token': access_token}), 200

@ad_route_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()  # Require JWT token for access
def admin_dashboard():
    current_user_id = get_jwt_identity()  # Get current user's ID from JWT token
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403  # Forbidden
    # Logic to fetch admin dashboard data...
    return jsonify({'message': 'Admin Dashboard Data'}), 200

@ad_route_bp.route('/admin/create-quiz/obj', methods=['POST'])
# @jwt_required()  # Require JWT token for access
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
            topic_id = create_topic(summaries, name=topic['topic_name'], course_id=course_id)
            for quiz_data in quizzes:
                quiz = Quiz(topic_id=topic_id,
                            hint=quiz_data['hint'],
                            question_text=quiz_data['question_text'],
                            course_id=course_id)

                if 'options' in quiz_data and isinstance(quiz_data['options'], list):
                    options_data = quiz_data['options']
                    for option_data in options_data:
                        option = Option(option_text=option_data['option_text'], is_correct=option_data['is_correct'], quiz=quiz)
                        quiz.options.append(option)

                db.session.add(quiz)

            db.session.commit()

            return jsonify({'message': 'Quizzes created successfully'}), 201

        except Exception as e:
            return jsonify({'error': f'unknown error{e}'}), 401

    return jsonify({'error': 'Method not allowed'}), 405

@ad_route_bp.route('/admin/create-quiz/gamma', methods=['POST'])
# @jwt_required()  # Require JWT token for access
def create_quiz_gamma():
    if request.method == 'POST':
        current_user_id = get_jwt_identity()  # Get current user's ID from JWT token
        current_user = User.query.get(current_user_id)
        if not current_user.is_admin:
            return jsonify({'message': 'Unauthorized'}), 403
        data = request.json 

        if 'quizzes' not in data or not isinstance(data['quizzes'], list):
            return jsonify({'error': 'No quizzes data provided or invalid format'}), 400

        try:
            quizzes = data['quizzes']
            course_id = data['course_id']
            topic = data['topic']
            topic_id = create_topic(name=topic['topic_name'], summary=topic["summary"], course_id=course_id)
            
            for quiz_data in quizzes:
                # Create a new Quiz object
                quiz = Quiz(topic_id=topic_id,
                            answer=quiz_data['answer'],
                            type_=quiz_data['type_'],
                            hint=quiz_data['hint'],
                            question_text=quiz_data['question_text'],
                            course_id=course_id)
                db.session.add(quiz)

            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'Quizzes created successfully'}), 201

        except Exception as e:
            return jsonify({'error': f'unknown error{e}'}), 401

    return jsonify({'error': 'Method not allowed'}), 405


@ad_route_bp.route('/admin/create-group-key/<string:user_id>', methods=['POST'])
@jwt_required()  # Require JWT token for access
def generate_group_key(user_id):
    if request.method == 'POST':
        current_user_id = get_jwt_identity()  # Get current user's ID from JWT token
        current_user = User.query.get(current_user_id)
        if not current_user.is_admin:
            return jsonify({'message': 'Unauthorized'}), 403
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
