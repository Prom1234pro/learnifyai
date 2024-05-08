from datetime import datetime
from flask import render_template, request, redirect, session, get_flashed_messages
from main import create_app
from main.models import User, Group, Course, db
from main.register import load_active_sessions, save_active_sessions
from flask_socketio import SocketIO
# from flask_login import LoginManager, login_user, current_user, logout_user

app, bcrypt = create_app()
socketio = SocketIO(app)

def is_auth():
    if 'user' in session:
        return True
    else:
        return False
            
@app.route('/')
def landing_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('landing_page.html', messages=messages)


@app.route('/practice/<string:user_id>/<string:course_id>')
def quiz(user_id, course_id):
    messages = get_flashed_messages(with_categories=True)
    course = Course.query.get_or_404(course_id)
    if not is_auth():     
        return redirect(f"/logout/{user_id}?return_url=/practice/{user_id}")
    return render_template('quiz.html', user_id=user_id, messages=messages, quizzes=course.quizzes, enum = enumerate, len=len)

@app.route('/courses/<string:id>/<string:group_id>')
def course_(id, group_id):
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(id)
    courses = group.courses
    messages = get_flashed_messages(with_categories=True)
    if not is_auth():
        return redirect(f"/logout/{id}?return_url=http://localhost:5000/courses/{id}")
    user_activity(id)
    return render_template('course.html', messages=messages, user=user, group_id=group_id, courses=courses)

def user_activity(user_id):
    user = User.query.get(user_id)
    active_sessions = load_active_sessions()
    active_sessions.pop(user.id, None)
    active_sessions[user.id] = {'email': user.email, 'last_activity': datetime.utcnow().isoformat()}
    save_active_sessions(active_sessions)
    session["user"] = user
    return 'User activity updated'


@app.route('/logout/<string:id>')
def logout(id):
    args = request.args
    url = args.to_dict()
    active_sessions = load_active_sessions()
    active_sessions.pop(id, None)
    save_active_sessions(active_sessions)
    session.pop('user', None)
    session.modified = True
    session.clear()
    url_query = url.get('return_url', None)
    if url_query is not None:
        return redirect(f'/login-user?return_url={url_query}')
    return redirect('/login-user')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    user = session.get('user')
    print(user)
    print('Client disconnected')

@socketio.on('user-offline')
def handle_offline(id):
    user = User.query.get_or_404(id)
    user.is_logged_in = False
    print("Offline")
    db.session.commit()

if __name__ == '__main__':
    socketio.run(app)
