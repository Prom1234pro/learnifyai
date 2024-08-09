from datetime import datetime
from flask import jsonify, redirect, render_template, url_for, request
import requests
# from flask import render_template, request, redirect, session, get_flashed_messages
from main import create_app
# from main.models.models import User, Group, Course, db
from main.reg import register_routes
# from main.routes.routes import load_active_sessions, save_active_sessions
from flask_mail import Message
# from flask_socketio import SocketIO
# from flask_login import LoginManager, login_user, current_user, logout_user
from main import mail
from main.utils import admin_required

app, bcrypt = create_app()
register_routes(app)
# socketio = SocketIO(app)
            
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404
    
@app.route('/')
def landing_page():
    # verification_token = "promise is nice"
    # try:
    #     verification_link = url_for('auth.verify_email', token=verification_token)
    #     msg = Message(subject='Verify Your Email Address', sender='promiseimadonmwinyi@gmail.com', recipients=["promiseimadonmwinyi@gmail.com"])
    #     msg.body = f"Please click the following link to verify your email address: http://127.0.0.1:5000{verification_link}"

    #     mail.send(msg)
    # except Exception as e:
    #     print(f"Error sending verification email: {e}")
    #     return redirect('/register')
    return redirect('/login-user')

@app.route('/admin-editor/create-quiz')
@admin_required
def admin_editor_create_quiz():
    return render_template('index.html')

def read_text(text):
    lines = text.splitlines()
    
    course_id = None
    topic_name = None
    instructions = None
    year = None
    quizzes = []
    
    current_question = {}
    current_options = []

    def add_question():
        if "question_text" in current_question and current_options:
            current_question["topic_name"] = topic_name
            current_question["options"] = current_options.copy()
            quizzes.append(current_question.copy())
            current_question.clear()
            current_options.clear()

    for line in lines:
        line = line.strip()
        
        if line.startswith("Course ID:"):
            course_id = line.split(":", 1)[1].strip()
        
        elif line.startswith("Topic Name:"):
            topic_name = line.split(":", 1)[1].strip()
        
        elif line.startswith("Current Instruction:"):
            instructions = line.split(":", 1)[1].strip()
        
        elif line.startswith("Year:"):
            year = line.split(":", 1)[1].strip()
        
        elif line and not line.startswith(("Course ID:", "Topic Name:", "Topic ID:", "Year:", "Instruction:")):
            if line.endswith("?"):
                add_question()
                current_question["question_text"] = line
                current_question["instructions"] = instructions  
            else:
                option_parts = line.rsplit(",", 1)
                option_text = option_parts[0].strip()
                is_correct = option_parts[1].strip().lower() == "true" if len(option_parts) > 1 else False
                current_options.append({
                    "option_text": option_text,
                    "is_correct": is_correct
                })

    add_question()

    return {
        "course_id": course_id,
        "year": year,
        "quizzes": quizzes
    }

@app.route('/convert-text-to-json', methods=['POST'])
def convert_text_to_json():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data from the request body
        text = data.get('text')    # Extract the text from the data
        
        if not text:
            return jsonify({'error': 'No text data provided'}), 400
        
        try:
            json_data = read_text(text)  # Convert text to JSON
            # print(json_data)
            # Call /admin/create-quiz/obj_ internally
            response = requests.post(
                'http://localhost:5000/admin/create-quiz/obj_',  # Adjust the URL if needed
                json=json_data
            )
            
            if response.status_code == 201:
                return jsonify({'message': 'Quiz created successfully'}), 201
            else:
                return jsonify({'error': f'Error creating quiz: {response.json().get("error")}'
                                         if response.json().get("error") else 'Unknown error'}), response.status_code
        
        except Exception as e:
            return jsonify({'error': f'Error processing text: {e}'}), 400

    return jsonify({'error': 'Invalid request method'}), 405
# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     user = session.get('user')
#     print(user)
#     print('Client disconnected')

# @socketio.on('user-offline')
# def handle_offline(id):
#     user = User.query.get_or_404(id)
#     user.is_logged_in = False
#     print("Offline")
    # db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True)
