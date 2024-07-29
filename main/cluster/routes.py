from flask import (Blueprint, abort, redirect, 
    render_template, request,
    jsonify, flash, get_flashed_messages, session
    )
import uuid
from werkzeug.utils import secure_filename
import os
from flask import current_app

from main.course.models import Performance, Course
from main.utils import admin_required, user_required
from .models import db, Group
from ..authentication.models import User
from datetime import datetime, timedelta
# from ... import bcrypt 
# from ... import mail
from .utils import is_auth
from itertools import cycle
SESSION_TIMEOUT = timedelta(hours=6)
groute_bp = Blueprint('group', __name__)

ACTIVE_SESSIONS_FILE = 'active_sessions.json'

 
@groute_bp.route('/dashboard/<string:id>')
@user_required
def dashboard(id):
    messages = get_flashed_messages(with_categories=True)
    public_groups = Group.query.filter_by(is_public=True, activated=True).all()
    user = User.query.get_or_404(id)
    courses = []
    for group in user.groups:
        courses.extend(group.courses)
    user_groups = user.activated_groups
    colors = ['primary', 'success', 'danger', 'info', 'warning']
    index = 0
    for course in courses:
        if index > 4:
            index = 0
        course.color = colors[index]
        index += 1
    courses_dict = [course.to_dict() for course in courses]
    
    
    # user_activity(id)
    return render_template('pages/dashboard.html', messages=messages, user=user, user_groups=user_groups, public_groups=public_groups, courses=courses_dict)


  
@groute_bp.route('/clusters/<string:id>')
@user_required
def group(id):
    messages = get_flashed_messages(with_categories=True)
    public_groups = Group.query.filter_by(is_public=True, activated=True).all()
    print(public_groups)
    for pu in public_groups:
        print(pu, "ertawere")
    user = User.query.get_or_404(id)
    user_groups = user.activated_groups
    
    return render_template('pages/clusters.html', messages=messages, user=user, user_groups=user_groups, public_groups=public_groups)

    
@groute_bp.route('/admin/create-group', methods=['POST'])
@admin_required
def create_group():
    if request.method == 'POST':
        data = request.form
        if not data:
            return jsonify({'error': 'No data provided'})

        user_id = session["user_id"]
        no_of_users = data.get('max-occupancy')
        group_name = data.get('group-name')
        school = data.get('school')
        group_pin = data.get('group-pin')
        group_key = str(uuid.uuid4())
        motto = data.get('motto')
        description = data.get('description')
        
        # Ensure required fields are provided
        if not group_name or not no_of_users or not group_pin:
            return jsonify({'error': 'Required fields are missing'}), 400

        # Create the group object
        group = Group(
            name=group_name,
            school=school,
            max_no_users=int(no_of_users),
            group_admin_id=user_id,
            cluster_handle = str(uuid.uuid4()),
            group_key=group_key,
            pass_key=group_pin,
            motto=motto,
            description=description,
            is_public=True,
            activated=True
        )

        user = User.query.get(user_id)
        if 'group-image' in request.files:
            file = request.files['group-image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                group.image_filename = filename

        group.created_by = user.id
        group.owned_by = user.id
        group.current_no_users = 0

        db.session.add(group)
        db.session.commit()

        flash(f'{group.name} has been created successfully', "success")
        return jsonify({'message': f'{group.name} cluster has been created'}), 200
    
    return abort(404)


@groute_bp.route('/user/add-to-group', methods=['POST'])
@user_required
def add_user_to_group():
    if request.method == 'POST':
        # Check if Content-Type is JSON
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            data = request.form
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract data from request
        group_id = data.get('group_id')
        user_id = session.get('user_id')
        pass_key = data.get('group_pin') or "1234"
        
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
            flash('An unknown error occurred', "warning")
            flash('You were logged out', "warning")
            return redirect('/login-user')

        if user in group.users:
            return jsonify({"error": "User already in group"}), 200

        group.users.append(user)
        group.current_no_users += 1

        # Create a new Performance object for the user
        for course in group.courses:
            new_performance = Performance(user_id=user.id, course_id=course.id, score=0, average=0)
            db.session.add(new_performance)
        
        # Commit all changes to the database
        db.session.commit()

        flash('Joined group successfully and performance created', "info")
        if request.content_type == 'application/json':

            return jsonify({"success": f"{user.username} added to {group.name}"})
        else:
            return redirect(request.referrer or '/clusters/'+user_id)
    
    return abort(404)


@groute_bp.route('/join-cluster/<cluster_id>', methods=['GET','POST'])
@user_required
def join_cluster(cluster_id):
    if request.method == 'POST':
        pass
    return render_template("pages/join-cluster.html")