from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )
import uuid
import json
from .models import db, User, Quiz, Option, Group
from datetime import datetime, timedelta
from . import bcrypt 

SESSION_TIMEOUT = timedelta(seconds=10)
groute_bp = Blueprint('group', __name__)

ACTIVE_SESSIONS_FILE = 'active_sessions.json'


  
@groute_bp.route('/groups/<string:id>')
def group(id):
    messages = get_flashed_messages(with_categories=True)
    public_groups = Group.query.filter_by(is_public=True, activated=True).all()
    user = User.query.get_or_404(id)
    user_groups = user.activated_groups
    # if not is_auth():     
    #     return redirect(f"/logout/{id}?return_url=http://localhost:5000/groups/{id}")
    # user_activity(id)
    return render_template('group.html', messages=messages, user=user, user_groups=user_groups, public_groups=public_groups)

@groute_bp.route('/admin/create-group-key/<string:user_id>', methods=['POST'])
def generate_group_key(user_id):
    if request.method == 'POST':
        data = request.form
        if not data:
            flash('No data provided', "warning")
            return redirect('/groups/'+user_id)
        
        no_of_users = data.get('max-occupancy')
        # group_admin_id = data.get('group_admin_id')
        group = Group(
            name = data.get('group-name'),
            school = data.get('school'),
            max_no_users=no_of_users,
            group_admin_id=user_id,
            group_key=str(uuid.uuid4()),
        )
        db.session.add(group)
        db.session.commit()
        flash('Group creation was successful', "success")
        flash('Click create group and check has id', "info")
        flash(f'Your id is {group.group_key}', "info")
        flash('Copy your id if not it will be lost', 'warning')
        return redirect('/groups/'+user_id)

@groute_bp.route('/user/create-group/<string:user_id>', methods=['POST'])
def create_group(user_id):
    data = request.form
    if not data:
        return jsonify({'error': 'No data provided'})
    
    group_pin = data.get('group-pin')
    group_key = data.get('group-id')
    group = Group.query.filter_by(group_key=group_key).first()
    if not group or group.group_admin_id != user_id:
        flash('Invalid group identifier', "warning")
        return redirect('/groups/'+user_id)
    
    # if int(group.max_no_users) != int(no_of_users):
    #     return jsonify({'error': f'Valid numbers of users is {group.max_no_users}'}), 403

    group.activated = True
    group.pass_key = group_pin
    user = User.query.get(user_id)
    if not user:
        flash('You are not authorized to this page', "warning")
        return redirect('/login-user')

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
        

        # Retrieve the group and check if it exists
        group = Group.query.get(group_id)
        if not group:
            flash('This group was deleted by the creator', "warning")
            return redirect('/groups/'+user_id)

        # Check if the passkey matches the passkey associated with the group
        if str(pass_key) != str(group.pass_key):
            flash('Incorrect passkey', "warning")
            return redirect('/groups/'+user_id)

        if group.current_no_users +1 > group.max_no_users:
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
        db.session.commit()
        

        flash('Joined group successfully', "info")
        print('/groups/'+user_id)
        return redirect('/groups/'+user.id)
