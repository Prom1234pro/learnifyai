from datetime import datetime
from flask import render_template, request, redirect, session, get_flashed_messages
from main import create_app, mail
# from main.models.models import User, Group, Course, db
from main.reg import register_routes
# from main.routes.routes import load_active_sessions, save_active_sessions
from flask_mail import Message
# from flask_socketio import SocketIO
# from flask_login import LoginManager, login_user, current_user, logout_user

app, bcrypt = create_app()
register_routes(app)
# socketio = SocketIO(app)
            

    
@app.route('/')
def landing_page():
    # msg = Message("Email with Embedded Image",
    #               sender="contact@tpaservices.me",
    #               recipients=["promiseimadonmwinyi@gmail.com"])
    
    # # The HTML body with the embedded image
    # msg.body = """
    # Some one just entered the site
    # """
    
    # # Attach the image
    # # with app.open_resource("image.jpg") as fp:
    # #     msg.attach("image.jpg", "image/jpeg", fp.read(), headers=[('Content-ID', '<image1>')])
    
    # mail.send(msg)
    # print("Email sent")
    messages = get_flashed_messages(with_categories=True)
    return render_template('pages/landing_page.html', messages=messages)

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
