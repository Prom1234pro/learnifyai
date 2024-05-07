from flask import (Blueprint, redirect, 
    render_template, request, g,
    jsonify, session, flash, get_flashed_messages
    )
import uuid
import json
from .models import db, Course
from datetime import datetime, timedelta
from . import bcrypt 
import requests

SESSION_TIMEOUT = timedelta(seconds=10)
croute_bp = Blueprint('course', __name__)

@croute_bp.route('/user/create-course/<string:group_id>', methods=['POST'])
def create_course(group_id):
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

        return jsonify({'message': 'Course created successfully'}), 201

    return jsonify({'error': 'Method not allowed'}), 405