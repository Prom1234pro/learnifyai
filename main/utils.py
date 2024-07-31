from functools import wraps
from flask import flash, redirect, url_for, abort, session

from main.authentication.models import Profile, User


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login_user_'))
        
        user = User.query.get(user_id)
        if not user:
            flash('You need to log in to access this page.', 'warning')
            return redirect(url_for('auth.login_user_'))  # Redirect to the login page
        return f(*args, **kwargs)
    return decorated_function

def onboarding_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('onboarding_id')
        if not user_id:
            return redirect(url_for('auth.create_user'))  # Redirect to the login page
        
        user = User.query.get(user_id)
        if not user:
            flash('You need to log in to access this page.', 'warning')
            return redirect(url_for('auth.create_user'))  # Redirect to the login page
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return abort(404)
        
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return abort(404)
        
        return f(*args, **kwargs)
    return decorated_function

def premium_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user').is_premium_user:
            flash('This page is only accessible to premium users.', 'warning')
            return redirect(url_for('upgrade_to_premium'))  # Redirect to upgrade page
        return f(*args, **kwargs)
    return decorated_function