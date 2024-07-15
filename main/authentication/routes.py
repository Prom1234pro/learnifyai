from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages, url_for
    )

from main.utils import user_required

# from main.utils import load_active_sessions, save_active_sessions, SESSION_TIMEOUT
from .models import db, User, Group
from flask_mail import Message
import string, secrets
from main import bcrypt, mail

a_route_bp = Blueprint('auth', __name__)

def generate_verification_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


@a_route_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()

    if user:
        user.email_verified = True
        user.verification_token = None
        db.session.commit()
        flash('Your email has been verified successfully!', 'success')
    else:

        flash('Invalid or expired verification token. Please try again.', 'danger')

    return redirect("/login-user")

@a_route_bp.route('register', methods=['GET', 'POST'])
def create_user():
    messages = get_flashed_messages(with_categories=True)
    if request.method == 'POST':
        data = request.form
        referrer = data.get('referrer')
        if not data:
            flash('You did not provide any data', "warning")
            return redirect('/register')
        
        username = data.get('username')
        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', "warning")
            return redirect('/register')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists', "warning")
            flash('If you are the owner, please log in', "success")
            return redirect('/register')
        
        verification_token = generate_verification_token()  # Ensure this function generates a token for the email
        new_user = User(username=username, email=email, full_name=fullname, password=hashed_password, verification_token=verification_token)
        db.session.add(new_user)
        db.session.commit()
        
        if referrer:
            referrer_user = User.query.filter_by(username=referrer).first()
            if referrer_user:
                new_user.referrer_id = referrer_user.id
                referrer_user.refer_user(new_user)
                referrer_user.earn_benefit()
                print("Number of referred users:", referrer_user.referral_count)
        
        try:
            verification_link = url_for('auth.verify_email', token=verification_token, _external=True)
            msg = Message(subject='Verify Your Email Address', sender='your_email@example.com', recipients=[email])
            msg.body = f"Please click the following link to verify your email address: {verification_link}"
            mail.send(msg)
            flash('A verification email has been sent to you', "success")

        except Exception as e:
            print(f"Error sending verification email: {e}")
            flash('Server timeout. Please try again later.', "danger")
            return redirect('/register')
        
        return redirect('/onboarding')
    
    return render_template('account/signup.html', messages=messages, page="signup")

@a_route_bp.route('/onboarding')
def onboarding():
    return render_template('pages/ob.html')

@a_route_bp.route('/login-user', methods=['GET','POST'])
def login_user_():
    messages = get_flashed_messages(with_categories=True)
    user = session.get('user')
    # if user:
    #     return redirect(f'/groups/{user.id}')

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
        if not user.email_verified:
            flash('Email not yet verified', "warning")
            return redirect('/login-user')
        
        is_valid = bcrypt.check_password_hash(user.password, password)
        if not is_valid:
            flash('Invalid email or password', "warning")
            return redirect('/login-user')
        session["user"] = user
        user.is_logged_in = True
        db.session.commit()

        flash('login successful', "success")
        return redirect(f'/groups/{user.id}')

    return render_template('account/signup.html', messages=messages, page="login")

@a_route_bp.route('/logout')
def logout():
    user = session.get('user')
    user.is_logged_in = False
    db.session.commit()
    session.pop('user', None)
    session.modified = True
    session.clear()
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
    
@a_route_bp.route('/generate-referral-link')
def generate_referral_link():
    user = session["user"]
    referral_link = url_for('auth.create_user', referrer=user.username, _external=True)
    return render_template('pages/referral_link.html', referral_link=referral_link)

@a_route_bp.route('/user/update/<user_id>', methods=['PUT'])
@user_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.is_admin = data.get('is_admin', user.is_admin)
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  # Make sure to hash the password in real implementation
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200
