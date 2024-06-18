from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )
import uuid
from werkzeug.utils import secure_filename
import os
from flask import current_app
import json

from main.course.models import Performance
from .models import db, Group
from ..authentication.models import User
from datetime import datetime, timedelta
# from ... import bcrypt 
# from ... import mail
from .utils import is_auth

SESSION_TIMEOUT = timedelta(hours=6)
groute_bp = Blueprint('group', __name__)

ACTIVE_SESSIONS_FILE = 'active_sessions.json'


  
@groute_bp.route('/groups/<string:id>')
def group(id):
    messages = get_flashed_messages(with_categories=True)
    public_groups = Group.query.filter_by(is_public=False, activated=True).all()
    print(public_groups)
    for pu in public_groups:
        print(pu, "ertawere")
    user = User.query.get_or_404(id)
    user_groups = user.activated_groups
    if not is_auth():     
        return redirect(f"/logout/{id}")
    # user_activity(id)
    return render_template('pages/group.html', messages=messages, user=user, user_groups=user_groups, public_groups=public_groups)


@groute_bp.route('/user/create-group-key/<string:user_id>', methods=['POST'])
def user_generate_group_key(user_id):
    if request.method == 'POST':
        data = request.form
        if not data:
            flash('No data provided', "warning")
            return redirect('/groups/'+user_id)
        
        no_of_users = data.get('max-occupancy')
        # group_admin_id = data.get('group_admin_id')
        user = User.query.get_or_404(user_id)
        # if not user.is_premium_user:
        #     flash(f'You must be a premium user to create a private group', "info")
        #     return redirect('/groups/'+user_id)
        group_key=str(uuid.uuid4())
        group = Group(
            name = data.get('group-name'),
            school = data.get('school'),
            max_no_users=no_of_users,
            group_admin_id=user_id,
            group_key=group_key,
        )
        db.session.add(group)
        db.session.commit()
        # try:
        #     msg = Message(subject='Create Group', sender='contact@tpaservices.me', recipients=[user.email])
        #     msg.body = f"Your ID - {group_key}"
        #     mail.send(msg)
        # except:
        #     return "server error"
        flash(f"{group_key}", 'info')
        flash('You group creation is not yet complete', "info")
        flash('check your email to complete creation', "info")
        return redirect('/groups/'+user_id)
    
@groute_bp.route('/user/create-group/<string:user_id>', methods=['POST'])
def create_group(user_id):
    if not is_auth():     
        return redirect(f"/logout/{user_id}")
    
    data = request.form
    if not data:
        return jsonify({'error': 'No data provided'})
    
    group_pin = data.get('group-pin')
    group_key = data.get('group-id')
    group = Group.query.filter_by(group_key=group_key).first()
    if not group or group.group_admin_id != user_id:
        flash('Invalid group identifier', "warning")
        return redirect('/groups/'+user_id)
    
    group.activated = True
    group.is_public = False
    group.pass_key = group_pin
    
    user = User.query.get(user_id)
    if not user:
        flash('You are not authorized to this page', "warning")
        return redirect('/login-user')
    
    # Handle file upload
    if 'group-image' in request.files:
        file = request.files['group-image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            group.image_filename = filename
    
    group.users.append(user)
    group.current_no_users += 1

    db.session.commit()
    flash(f'{group.name} has been created successfully', "success")
    return redirect('/groups/'+user_id)

@groute_bp.route('/user/add-to-group', methods=['POST'])
def add_user_to_group():
    if request.method == 'POST':

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract data from JSON
        group_id = data.get('group_id')
        user_id = data.get('user_id')
        pass_key = data.get('group_pin')
        course_id = data.get('course_id')  # Ensure course_id is provided in the request
        
        # Retrieve the group and check if it exists
        group = Group.query.get(group_id)
        if not group:
            flash('This group was deleted by the creator', "warning")
            return redirect('/groups/'+user_id)

        # Check if the passkey matches the passkey associated with the group
        if str(pass_key) != str(group.pass_key):
            flash('Incorrect passkey', "warning")
            return redirect('/groups/'+user_id)

        if group.current_no_users + 1 > group.max_no_users:
            flash('Group already filled', "warning")
            return redirect('/groups/'+user_id)
        
        # Retrieve the user and add them to the group
        user = User.query.get(user_id)
        if not user:
            flash('An unknown error occured', "warning")
            flash('You were logged out', "warning")
            return redirect('/login-user')

        if user in group.users:
            return redirect('/groups/'+user_id)

        group.users.append(user)
        group.current_no_users += 1

        # Create a new Performance object for the user
        for course in group.courses:
            new_performance = Performance(user_id=user.id, course_id=course.id, score=0, average=0, progress=0)
            db.session.add(new_performance)
        
        # Commit all changes to the database
        db.session.commit()

        flash('Joined group successfully and performance created', "info")
        return redirect('/groups/' + user.id)
