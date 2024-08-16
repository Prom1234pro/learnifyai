from datetime import datetime
import json
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

if __name__ == '__main__':
    app.run(debug=True)

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


