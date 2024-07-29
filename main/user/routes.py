from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, flash, get_flashed_messages, url_for
    )
import uuid
from werkzeug.utils import secure_filename
import os
from flask import current_app, session
from main import bcrypt, mail


from main.course.models import Performance
from main.utils import user_required
from main.authentication.models import Profile, User, db
from datetime import datetime, timedelta

uroute_bp = Blueprint('user', __name__)


@uroute_bp.route('/account-settings')
@user_required
def profile_settings():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        # Update user details
        user.username = request.form.get('username')
        user.email = request.form.get('email')

        # Update profile details
        profile.full_name = request.form.get('full_name')
        profile.bio = request.form.get('bio')
        profile.university = request.form.get('university')
        profile.course = request.form.get('course')
        profile.date_of_birth = request.form.get('date_of_birth')

        # Save changes
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect("/account-settings")

    return render_template('pages/account-settings.html', user=user, profile=profile)



@uroute_bp.route('/security-settings', methods=['GET', 'POST'])
@user_required
def security_settings():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')

        # Check if the current password is correct
        if not bcrypt.check_password_hash(user.password, current_password):
            flash('Current password is incorrect', 'danger')
            return redirect('/security-settings')

        # Check if new password and confirmation match
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect('/security-settings')

        # Check password requirements
        if len(new_password) < 8 or not any(char.islower() for char in new_password) or not any(char.isdigit() for char in new_password):
            flash('New password does not meet the requirements', 'danger')
            return redirect('/security-settings')

        # Update password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash('Password updated successfully', 'success')
        return redirect('/security-settings')

    return render_template('pages/security-settings.html', user=user)

@uroute_bp.route('/account-profile')
@user_required
def account_profile():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    return render_template('pages/account-profile.html', user=user, profile=profile)
