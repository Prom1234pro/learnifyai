from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages
    )
from ...models.models import db, Course, Group, User
import requests

def is_auth():
    if 'user' in session:
        return True
    else:
        return False
    
croute_bp = Blueprint('course', __name__)

@croute_bp.route('/courses/<string:course_id>')
def courses(course_id):
    user = session.get('user')
    course = Course.query.get_or_404(course_id)
    if user is None:
        return redirect("/logout")
    return redirect(f"/courses/{user.id}/{course.group.id}")

@croute_bp.route('/courses/<string:id>/<string:group_id>')
def course_(id, group_id):
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(id)
    courses = group.courses
    messages = get_flashed_messages(with_categories=True)
    if not is_auth():
        return redirect(f"/logout/{id}?return_url=http://localhost:5000/courses/{id}/{group_id}")
    # user_activity(id)
    return render_template('course.html', messages=messages, user=user, group_id=group_id, courses=courses, enum=enumerate)


@croute_bp.route('/user/create-course/<string:group_id>', methods=['POST'])
def create_course(group_id):
    user = None
    if "user" in session:
        user = session["user"]
        print("user-id",user.id)
        user = User.query.get_or_404(user.id)
        print(user)
        # if not user.is_premium_user:
        #     flash(f'You must be an admin to upload material', "info")
        #     return redirect(f'/courses/{user.id}/{group_id}')
    else:
        flash('User needs authorization to perform this action', 'warning')
        return redirect('/login-user')
    if request.method == 'POST':
        # Extract data from the request body
        data = request.form
        course_name = data.get('course-name')
        url = data.get('url')
        no_of_topics = data.get('number-of-topics')
        # group_id = data.get('group_id')  # Assuming you pass group_id in the request

        try:
            response = requests.head(url)
            response.raise_for_status()  # Raise an exception for non-successful status codes
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Error checking URL: ' + str(e)}), 400
        
        # Create a new Course object
        new_course = Course(course_name=course_name, no_of_topics=no_of_topics, group_id=group_id)

        # Add the new course to the database session
        db.session.add(new_course)
        db.session.commit()

        flash('course created successfully', 'success')
        return redirect(f'/courses/{user.id}/{group_id}')

    return jsonify({'error': 'Method not allowed'}), 405