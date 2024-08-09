from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages, url_for
    )
import jwt
from main import app
from main.utils import onboarding_required, user_required

# from main.utils import load_active_sessions, save_active_sessions, SESSION_TIMEOUT
from .models import Profile, db, User, Group
from flask_mail import Message
import string, secrets
from main import bcrypt, mail
from datetime import datetime, timezone

a_route_bp = Blueprint('auth', __name__)

def generate_reset_token(email):
    # Generate a secure token
    token = jwt.encode({'email': email}, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def send_email(subject, body, to):
    msg = Message(subject, sender='promiseimadonmwinyi@example.com', recipients=[to], body=body)
    mail.send(msg)

def generate_verification_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


@a_route_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()

    current_time = datetime.now(timezone.utc).isoformat()  # Ensure the timestamp is in UTC
    if user:
        user.email_verified = True
        user.verification_token = None
        db.session.commit()
        flash({
                'time': current_time,  # ISO format timestamp
                'title': 'Email Verification',
                'text': 'Your email verification was successful',
                'category': 'primary'
            })
    else:
        flash({
                'time': current_time,  # ISO format timestamp
                'title': 'Email Verification',
                'text': 'Invalid or expired verification token. Please try again.',
                'category': 'warning'
            })
        return  render_template('account/verify-email-error.html')
    return redirect(f'/verify-email-successful?email={user.email}')

@a_route_bp.route('/request-activation-link', methods=['GET', 'POST'])
def request_activation_link():
    return render_template('account/request-activation-link.html')


@a_route_bp.route('register', methods=['GET', 'POST'])
def create_user():
    messages = get_flashed_messages(with_categories=True)
    if request.method == 'POST':
        current_time = datetime.now(timezone.utc).isoformat()  # Ensure the timestamp is in UTC
        data = request.form
        referrer = data.get('referrer')
        if not data:
            flash({
                'time': current_time,  # ISO format timestamp
                'title': 'No data provided',
                'text': 'You did not provide any data',
                'category': 'warning'
            })
            return redirect('/register')
        
        username = data.get('username')
        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash({
                'time': current_time,
                'title': 'Username taken.',
                'text': 'Please try a different username.',
                'category': 'danger'
            })
            return redirect('/register')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash({
                'time': current_time,
                'title': 'Email already exists',
                'text': 'If you are the owner, please log in',
                'category': 'warning'
            })
            return redirect('/register')
        
        verification_token = generate_verification_token()
        
        if referrer:
            referrer_user = User.query.filter_by(username=referrer).first()
            if referrer_user:
                new_user.referrer_id = referrer_user.id
                referrer_user.refer_user(new_user)
                referrer_user.earn_benefit()
        
        try:
            verification_link = url_for('auth.verify_email', token=verification_token, _external=True)
            msg = Message(subject='Verify Your Email Address', sender='promiseimadonmwinyi@example.com', recipients=[email])
            msg.body = f"Please click the following link to verify your email address: {verification_link}"
            mail.send(msg)
            new_user = User(username=username, email=email, full_name=fullname, password=hashed_password, verification_token=verification_token)
            
            db.session.add(new_user)
            db.session.commit()
            profile = Profile(
            user_id=new_user.id)
            db.session.add(profile)
            db.session.commit()
            session["onboarding_id"] = new_user.id
            flash({
                'time': current_time,
                'title': 'Email Verification',
                'text': f'An email verification was sent to {new_user.email}.',
                'category': 'primary'
            })
            return redirect(f'/onboarding')

        except Exception as e:
            flash({
                'time': current_time,
                'title': 'Server timeout',
                'text': f'Please try again later.{e}',
                'category': 'danger'
            })
            return redirect('/register')
    
    return render_template('account/auth-signup.html', messages=messages, page="signup")

@a_route_bp.route('/resend-email/<email>')
def resend_email(email):
    current_time = datetime.now(timezone.utc).isoformat()  # Ensure the timestamp is in UTC
    try:
        print(email)
        verification_token = generate_verification_token()
        user = User.query.filter_by(email=email.strip()).first()
        verification_link = url_for('auth.verify_email', token=verification_token, _external=True)
        msg = Message(subject='Verify Your Email Address', sender='promiseimadonmwinyi@example.com', recipients=[email])
        msg.body = f"Please click the following link to verify your email address: {verification_link}"
        mail.send(msg)
        flash({
                'time': current_time,
                'title': 'Verification Email Sent',
                'text': f'An email verification was sent to {user.email}.',
                'category': 'danger'
            })
        user.verification_token = verification_token
        db.session.commit()
        return redirect(f'/verification-email-sent?email={email}')

    except Exception as e:
        print(f"Error sending verification email: {e}")
        flash('Server timeout. Please try again later.', "danger")
        flash({
                'time': current_time,
                'title': 'Server timeout',
                'text': 'Please try again later.',
                'category': 'danger'
            })
        return redirect('/register')

@a_route_bp.route('/verify-email-successful')
def verify_email_successful():
    email = request.args.get("email")
    return render_template('account/verify-email-successful.html', email=email)

@a_route_bp.route('/onboarding', methods=['GET', 'POST'])
@onboarding_required
def onboarding():
    if request.method == 'POST':
        user = User.query.get(session.get('onboarding_id'))
        profile = Profile.query.filter_by(user_id=user.id).first()
        full_name = request.form.get('full_name')
        date_of_birth = request.form.get('date_of_birth')
        university = request.form.get('university')
        course = request.form.get('course')
        bio = request.form.get('bio')
        profile.full_name=full_name
        profile.user_id=user.id
        profile.date_of_birth=date_of_birth
        profile.university=university
        profile.course=course
        profile.bio=bio
        db.session.commit()
        
        return redirect(f'/verification-email-sent?email={user.email}')
    
    user = User.query.get(session.get('onboarding_id'))
    return render_template('account/onboarding.html', user=user)


@a_route_bp.route('/verification-email-sent')
def verification_email_sent():
    email = request.args.get("email")
    return render_template('account/verification-email-sent.html', email=email)

@a_route_bp.route('/login-user', methods=['GET','POST'])
def login_user_():
    messages = get_flashed_messages(with_categories=True)
    user_id = session.get("user_id") or ""
    user = User.query.get(user_id)
    if user:
        return redirect(f'/dashboard/{user.id}')

    if request.method == 'POST':
        current_time = datetime.now(timezone.utc).isoformat()  # Ensure the timestamp is in UTC
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
            flash({
                'time': current_time,
                'title': 'Email not yet verified',
                'text': 'Check you email for activation link',
                'category': 'warning'
            })
            return redirect('/login-user')
        
        is_valid = bcrypt.check_password_hash(user.password, password)
        if not is_valid:
            flash({
                'time': current_time,
                'title': 'Credential Error',
                'text': 'Invalid email or password',
                'category': 'warning'
            })
            return redirect('/login-user')
        session["user_id"] = user.id
        
        user.is_logged_in = True
        db.session.commit()
        print("redirect success ===============")
        return redirect(f'/dashboard/{user.id}')

    return render_template('account/auth-login.html', messages=messages, page="login")

@a_route_bp.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        current_time = datetime.now(timezone.utc).isoformat()  # Ensure the timestamp is in UTC
        
        if user:
            # Generate a password reset token
            token = generate_reset_token(user.email)
            
            # Create a reset URL
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            # Prepare email content
            subject = "Password Reset Request"
            body = f"Click the following link to reset your password: {reset_url}"
            
            # Send email
            send_email(subject, body, email)
            
            flash(
                {
                'time': current_time,
                'title': 'Email Sent',
                'text': "If an account with that email exists, you will receive a password reset link.",
                'category': 'info'
                })
            return redirect(url_for('auth.forgot_password'))
        else:
            flash(
                {
                'time': current_time,
                'title': 'Email Not Sent',
                'text': "No account found with that email address.",
                'category': 'info'
                })
            return redirect(url_for('auth.forgot_password'))
    
    messages = get_flashed_messages(with_categories=True)
    return render_template('account/auth-forgot-password.html', messages=messages, page="forgot_password")

@a_route_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        password = request.form.get('password')
        password_confirm = request.form.get('confirm-password')
        current_time = datetime.now(timezone.utc).isoformat()  # Ensure the timestamp is in UTC
        
        if password == password_confirm:
            try:
                # Decode token and get email
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                email = data['email']
                
                # Find user and update password
                print(email)
                user = User.query.filter_by(email=email).first()
                if user:
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    user.password = hashed_password  # You should hash the password before saving
                    db.session.commit()
                    flash({
                    'time': current_time,
                    'title': 'Password Updated',
                    'text': "Your password has been updated.",
                    'category': 'info'
                    })
                
                    return redirect(url_for('auth.login_user_'))
            except Exception as e:
                flash({
                    'time': current_time,
                    'title': 'Link Expired',
                    'text': "The reset link is invalid or has expired.",
                    'category': 'danger'
                    })
                return redirect(url_for('auth.forgot_password'))

        else:
            flash({
                    'time': current_time,
                    'title': 'Input Error',
                    'text': "Passwords don't match.",
                    'category': 'info'
                    })
            return redirect(url_for('auth.reset_password', token=token))
        
    messages = get_flashed_messages(with_categories=True)
    return render_template('account/auth-reset-password.html', messages=messages, token=token)


@a_route_bp.route('verification-email')
def verification_email():
    messages = get_flashed_messages(with_categories=True)
    return render_template('account/verification-email-sent.html', messages=messages, page="login")

@a_route_bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    user.is_logged_in = False
    db.session.commit()
    session.pop('user_id', None)
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


@app.route('/affiliate-register')
def affiliate_register():
    

    messages = get_flashed_messages(with_categories=True)
    return render_template('account/affiliate-multi-step.html', messages=messages) 