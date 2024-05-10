from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages
    )
import uuid
import json
from main.utils import load_active_sessions, save_active_sessions, SESSION_TIMEOUT
from ..models.models import db, User, Quiz, Option, Group
from datetime import datetime, timedelta
from .. import bcrypt 

a_route_bp = Blueprint('auth', __name__)


@a_route_bp.route('register', methods=['GET', 'POST'])
def create_user():
    messages = get_flashed_messages(with_categories=True)

    if request.method == 'POST':
        data = request.form
        if not data:
            flash('you did not provide any data', "warning")
            return redirect('/register')
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
    

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('username already exists', "warning")
            return redirect('/register')
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('email already exists', "warning")
            flash('If you are the owner login', "success")
            return redirect('/register')
    
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account creation was successful', "success")
        flash('Note: This is a test version of the app and your account will be deleted after 24 hours', "warning")
        return redirect('/login-user')
    
    return render_template('signup.html', messages=messages, page="signup")

@a_route_bp.route('/login-user', methods=['GET','POST'])
def login_user_():
    active_sessions = load_active_sessions()
    args = request.args
    url = args.to_dict()
    messages = get_flashed_messages(with_categories=True)
    if request.method == 'POST':
        data = request.form
        if not data:
            flash('you did not provide any data', "warning")
            return redirect('/login-user')
        
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('Invalid credentials', "warning")
            return redirect('/login-user')
        
        is_valid = bcrypt.check_password_hash(user.password, password)
        if not is_valid:
            flash('Invalid email or password', "warning")
            return redirect('/login-user')
        
        if user.id in active_sessions.keys():
            print("user.id is in active sessions")
            active_sessions = load_active_sessions()
            last_activity_time = datetime.fromisoformat(active_sessions[user.id]['last_activity'])
            if datetime.utcnow() - last_activity_time > SESSION_TIMEOUT:
                del active_sessions[user.id]
                print(active_sessions)
            elif 'user' in session:
                flash('Welcome Back')
            else:
                flash('Our system discovered an unusual login request', "warning")
                flash('Your account will be suspended if this persist', "warning")
                return redirect('/login-user')
    
        active_sessions[user.id] = {'email': user.email, 'last_activity': datetime.utcnow().isoformat()}
        # db.session.commit()
        save_active_sessions(active_sessions)
        session["user"] = user
        url_query = url.get('return_url', None)
        if url_query is not None:
            flash('Welcome back! continue from where you left off', "success")
            return redirect(url_query)
    
        flash('login successful', "success")
        return redirect(f'/groups/{user.id}')
    url_query = url.get('return_url', None)
    if url_query is not None:
        return render_template('signup.html', messages=messages, page="login", return_url=url_query)

    return render_template('signup.html', messages=messages, page="login")

@a_route_bp.route('/logout/<string:id>')
def logout(id):
    args = request.args
    url = args.to_dict()
    active_sessions = load_active_sessions()
    active_sessions.pop(id, None)
    save_active_sessions(active_sessions)
    session.pop('user', None)
    session.modified = True
    session.clear()
    url_query = url.get('return_url', None)
    if url_query is not None:
        return redirect(f'/login-user?return_url={url_query}')
    return redirect('/login-user')

@a_route_bp.route('/groups/remove_user', methods=['POST'])
def remove_user_from_group():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Extract data from JSON
    user_id = data.get('user_id')
    group_id = data.get('group_id')

    # Retrieve the group and check if it exists
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    # Retrieve the user and check if it exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Remove the user from the group
    if user in group.users:
        group.users.remove(user)
        db.session.commit()
        return jsonify({'message': f'User {user_id} removed from group {group_id} successfully'}), 200
    else:
        return jsonify({'error': 'User is not in the group'}), 400
    
