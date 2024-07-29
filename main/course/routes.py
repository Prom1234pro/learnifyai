from flask import (Blueprint, abort, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages, url_for, abort
    )
from datetime import datetime, timedelta

from main.utils import user_required
from .models import Performance, Score, db, Course
from main.authentication.models import User
from main.cluster.models import Group

    
croute_bp = Blueprint('course', __name__)

@croute_bp.route('/courses')
@user_required
def courses():
    user = session.get('user')
    # if user is None:
    #     return redirect("/logout")
    return redirect(f"/courses/{user.id}")

@croute_bp.route('/courses/<string:user_id>')
@user_required
def get_all_user_courses(user_id):
    user = User.query.get(user_id)
    messages = get_flashed_messages(with_categories=True)

    if not user:
        abort(404)

    # Collect all courses from the user's groups
    courses = []
    for group in user.groups:
        courses.extend(group.courses)

    # Convert the course objects to dictionaries
    # courses_data = [{
    #     "id": course.id,
    #     "course_name": course.course_name,
    #     "url": course.url,
    #     "no_of_topics": course.no_of_topics,
    #     "group_id": course.group_id
    # } for course in courses]    
    return render_template('pages/course.html', messages=messages, user=user, courses=courses, enum=enumerate)

@croute_bp.route('/cluster-courses/<string:group_id>')
@user_required
def get_all_user_group_courses(group_id):
    group = Group.query.get(group_id)
    messages = get_flashed_messages(with_categories=True)

    user_id = session.get('user_id')
    user = User.query.get(user_id)
      
    return render_template('pages/courses.html', messages=messages, group=group, user=user)


@croute_bp.route('/courses/<string:id>/<string:group_id>')
@user_required
def course_(id, group_id):
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(id)
    courses = group.courses
    messages = get_flashed_messages(with_categories=True)
    # user_activity(id)
    return render_template('pages/course.html', messages=messages, user=user, group_id=group_id, courses=courses, enum=enumerate)
    # return render_template('pages/course.html', messages=messages, user=user, enum=enumerate)


@croute_bp.route('/user/create-course/<string:group_id>', methods=['POST'])
@user_required
def create_course(group_id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.get_or_404(user_id)
        # Extract data from the request body
        data = request.get_json()
        course_name = data.get('course_name')
        url = data.get('url')
        _for = data.get('_for')
        description = data.get('description', '')  # Default to an empty string if not provided
        progress = data.get('progress', 0)  # Default to 0 if not provided
        
        group = Group.query.get_or_404(group_id)
        new_course = Course(
            course_name=course_name,
            url=url,
            _for=_for,
            description=description,
            progress=progress,
            group_id=group_id
        )
        
        db.session.add(new_course)
        
        # Create a Performance object for the user and the new course
        for user in group.users:
            new_performance = Performance(user_id=user.id, course_id=new_course.id, score=0)
            db.session.add(new_performance)
        
        # Commit both the new course and performance to the database
        db.session.commit()
        
        flash('Course created successfully', 'success')
        
        return jsonify({"message": "success", "course_id": new_course.id})

    return abort(404)


@croute_bp.route('/performances', methods=['GET'])
@user_required
def show_performances():
    user_id = session.get("user_id")
    user = User.query.get_or_404(user_id)
    performances = Performance.query.filter_by(user_id=user.id).all()
    
    # Render the performance.html template and pass the performances data
    return render_template('pages/performances.html', user=user, performances=performances)


@croute_bp.route('/updateperformance/<string:id>/<score>', methods=['POST'])
@user_required
def update_performance(id, score):
    user = User.query.get_or_404(session["user"].id)
    performance = Performance.query.get_or_404(id)

    if performance.user_id != user.id:
        flash('Unauthorized action', 'danger')
        return redirect('/courses')
    
    if request.method == 'POST':
        data = request.get_json()
        
        if score is not None:
            new_score_value = float(score)
            performance.add_score(new_score_value)  # Adds a new score and manages the score count

        # if average is not None:
        #     performance.average = int(average)
        # if progress is not None:
        #     performance.progress = int(progress)
        
        db.session.commit()
        
        flash('Performance updated successfully', 'success')
        return redirect(f'/courses/{user.id}/{performance.course_id}')
    
    return abort(404)    


@croute_bp.route('/deleteperformance/<string:id>', methods=['POST'])
@user_required
def delete_performance(id):
    print(id)
    performance = Performance.query.get(id)
    if not performance:
        flash('Performance not found.', 'warning')
        return redirect(url_for('course.show_performances'))  # Redirect to an appropriate page

    # Delete all associated scores
    scores = Score.query.filter_by(performance_id=id).all()
    for score in scores:
        db.session.delete(score)

    db.session.commit()

    return redirect(url_for('course.show_performances'))


@croute_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    # Calculate the date for one week ago
    one_week_ago = datetime.utcnow() - timedelta(weeks=1)

    # Query to get the top performers within the last week
    top_performers = db.session.query(
        User.username,
        db.func.sum(Performance.score).label('total_score')
    ).join(Performance).filter(
        Performance.timestamp >= one_week_ago
    ).group_by(User.id).order_by(
        db.desc('total_score')
    ).limit(10).all()

    # Format the results
    leaderboard = [{"username": user.username, "total_score": score} for user, score in top_performers]

    return jsonify(leaderboard), 200