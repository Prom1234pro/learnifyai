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
    public_groups = Group.query.filter_by(is_public=True).all()
    user = User.query.get_or_404(id)
    user_groups = user.groups
    # if not is_auth():     
    #     return redirect(f"/logout/{id}?return_url=http://localhost:5000/groups/{id}")
    # user_activity(id)
    return render_template('group.html', user=user, user_groups=user_groups, public_groups=public_groups)

@groute_bp.route('/admin/create-group-key/<string:user_id>', methods=['POST'])
def generate_group_key(user_id):
    if request.method == 'POST':
        data = request.form
        if not data:
            return jsonify({'error': 'No data provided'})
        
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
        return jsonify({'message': 'Group created successfully', 'group_id': group.group_key, 'no_of_users': group.max_no_users}), 201

@groute_bp.route('/user/create-group/<string:user_id>', methods=['POST'])
def create_group(user_id):
    data = request.form
    if not data:
        return jsonify({'error': 'No data provided'})
    
    group_pin = data.get('group-pin')
    group_key = data.get('group-id')
    group = Group.query.filter_by(group_key=group_key).first()
    if not group or group.group_admin_id != user_id:
        return jsonify({'error': 'Invalid group key'}), 403
    
    # if int(group.max_no_users) != int(no_of_users):
    #     return jsonify({'error': f'Valid numbers of users is {group.max_no_users}'}), 403

    group.activated = True
    group.pass_key = group_pin
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    group.users.append(user)
    group.current_no_users += 1

    db.session.commit()
    return jsonify({'message': 'Group created successfully',"act":group.activated, 'group_id': group.id}), 201

@groute_bp.route('/user/add-to-group', methods=['POST'])
def add_user_to_group():
    if request.method == 'POST':

        data = request.json

        # Extract group_id and user_id from the JSON data
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract data from JSON
        group_id = data.get('group_id')
        user_id = data.get('user_id')
        pass_key = data.get('group_pin')
        

        # Retrieve the group and check if it exists
        group = Group.query.get(group_id)
        if not group:
            return jsonify({'error': 'Group not found'}), 404

        # Check if the passkey matches the passkey associated with the group
        if str(pass_key) != str(group.pass_key):
            return jsonify({'error': 'Incorrect passkey'}), 403

        if group.current_no_users +1 > group.max_no_users:
            return jsonify({'error': 'Group already filled'})
        # Retrieve the user and add them to the group
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        group.users.append(user)
        group.current_no_users += 1
        db.session.commit()

        return jsonify({'message': f'User {user_id} added to group {group_id} successfully'}), 200
