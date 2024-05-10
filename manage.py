from datetime import datetime
from flask import render_template, request, redirect, session, get_flashed_messages
from main import create_app
from main.models.models import User, Group, Course, db
from main.routes import register_routes
# from main.routes.routes import load_active_sessions, save_active_sessions
from flask_socketio import SocketIO
# from flask_login import LoginManager, login_user, current_user, logout_user

app, bcrypt = create_app()
register_routes(app)
socketio = SocketIO(app)
            
@app.route('/')
def landing_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('landing_page.html', messages=messages)

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
    socketio.run(app, debug=True)
