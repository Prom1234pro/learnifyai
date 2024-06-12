from flask import (Blueprint, redirect, 
    render_template, request,
    jsonify, session, flash, get_flashed_messages
    )

from main.routes.course.create_demo import create_quiz
from main.utils import image_to_text, read_files, scanned_pdf_to_text
from ...models.models import Performance, db, Course, Group, User
from PIL import Image
import os
from groq import Groq

def chat(prompt, course_id):
    client = Groq(
    api_key="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"
)

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt + f'\n5. Change the course_id in the above format to {course_id}'
            },
            ],
        temperature=1,
        max_tokens=3020,
        top_p=1,
        stream=True,
        stop=None,
    )
    res = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
         res += str(chunk.choices[0].delta.content)
    return res


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
        print("user-id", user.id)
        user = User.query.get_or_404(user.id)
        print(user)
        # if not user.is_premium_user:
        #     flash(f'You must be an admin to upload material', "info")
        #     return redirect(f'/courses/{user.id}/{group_id}')
    else:
        flash('User needs authentication to perform this action', 'warning')
        return redirect('/login-user')
        
    if request.method == 'POST':
        # Extract data from the request body
        data = request.form
        course_name = data.get('course-name')
        url = data.get('url')
        no_of_topics = data.get('number-of-topics')
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        allowed_extensions = {'png', 'jpg', 'jpeg', 'pdf'}
        file_extension = os.path.splitext(file.filename)[1].lower()[1:]
        if file_extension not in allowed_extensions:
            return jsonify({'error': 'Invalid file extension'}), 400
        # try:
        #     response = requests.head(url)
        #     response.raise_for_status()  # Raise an exception for non-successful status codes
        # except requests.exceptions.RequestException as e:
        #     return jsonify({'error': 'Error checking URL: ' + str(e)}), 400
        
        if file_extension == "pdf":
            res = scanned_pdf_to_text_route(file)
        else:
            res = image_to_texd_route(file)
        text = res
        with open("prompt.txt") as f:
            fil = f.read()
            text += fil
        
        # Create a new Course object
        group = Group.query.get_or_404(group_id)
        new_course = Course(course_name=course_name, no_of_topics=no_of_topics, url=url, group_id=group_id)
        
        # Add the new course to the database session
        db.session.add(new_course)
        db.session.flush()  # Flush to get the course ID before committing
        print(text)
        resp = chat(text, new_course.id)
        print(resp)
        # Create a Performance object for the user and the new course
        for user in group.users:
            new_performance = Performance(user_id=user.id, course_id=new_course.id, score=0, average=0, progress=0)
            db.session.add(new_performance)
        # Commit both the new course and performance to the database
        db.session.commit()
        
        flash('Course created successfully', 'success')
        
        flash('Generating your questions and summaries from your material', 'success')

        create_quiz(resp)
        return redirect(f'/courses/{user.id}/{group_id}')

    return jsonify({'error': 'Method not allowed'}), 405

@croute_bp.route('/performances', methods=['GET'])
def show_performances():
    user = None
    if "user" in session:
        user = session["user"]
        print("user-id", user.id)
        user = User.query.get_or_404(user.id)
        print(user)
        # if not user.is_premium_user:
        #     flash(f'You must be an admin to upload material', "info")
        #     return redirect(f'/courses/{user.id}/{group_id}')
    else:
        flash('User needs authentication to perform this action', 'warning')
        return redirect('/login-user')
    # Query the database for performances by user ID
    performances = Performance.query.filter_by(user_id=user.id).all()
    
    # Render the performance.html template and pass the performances data
    return render_template('performance.html', user=user, performances=performances)


@croute_bp.route('/updateperformance/<string:id>', methods=['POST'])
def update_performance(id):
    user = None
    if "user" in session:
        user = session["user"]
        print("user-id", user.id)
        user = User.query.get_or_404(user.id)
        print(user)
        # if not user.is_premium_user:
        #     flash(f'You must be an admin to upload material', "info")
        #     return redirect(f'/courses/{user.id}/{group_id}')
    else:
        flash('User needs authentication to perform this action', 'warning')
        return redirect('/login-user')
    
    if request.method == 'POST':
        performance = Performance.query.get_or_404(id)
        data = request.form
        score = data.get('score', performance.score)
        average = data.get('average', performance.average)
        progress = data.get('progress', performance.progress)
        
        # Find the performance record by id
        
        # Check if the performance belongs to the logged-in user
        if performance.user_id != user.id:
            flash('Unauthorized action', 'danger')
            return redirect('/')

        # Update the performance fields
        if score is not None:
            performance.score = int(score)
        if average is not None:
            performance.average = int(average)
        if progress is not None:
            performance.progress = int(progress)
        
        # Commit the changes to the database
        db.session.commit()
        
        return redirect(f'/courses/{user.id}/{performance.course_id}')

    return jsonify({'error': 'Method not allowed'}), 405     


def scanned_pdf_to_text_route(file):
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    allowed_extensions = {'pdf'}
    file_extension = os.path.splitext(file.filename)[1].lower()[1:]
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid file extension'}), 400


    pdf_bytes = file.read()
    text = scanned_pdf_to_text(pdf_bytes)
    return text

def image_to_texd_route(file):
    
    
    allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
    file_extension = os.path.splitext(file.filename)[1].lower()[1:]
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid file extension'}), 400

    # Check MIME type
    try:
        img = Image.open(file)
        if img.format.lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid image format'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid image file'}), 400

    file.seek(0)
    img = read_files(file)
    text = image_to_text(img)
    return text

