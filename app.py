from datetime import datetime
from flask import render_template, request, redirect, session, get_flashed_messages
from main import create_app
from main.models import User, Group, Course
from main.register import load_active_sessions, save_active_sessions
# from flask_login import LoginManager, login_user, current_user, logout_user

app, bcrypt = create_app()
    
def is_auth():
    if 'user' in session:
        return True
    else:
        return False
            
@app.route('/')
def landing_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('landing_page.html', messages=messages)


# @app.route('/groups/<string:id>')
# def group(id):
#     # if not is_auth():     
#     #     return redirect(f"/logout/{id}?return_url=http://localhost:5000/groups/{id}")
#     user_activity(id)
#     return render_template('group.html', user_id=id)

@app.route('/practice/<string:user_id>/<string:course_id>')
def quiz(user_id, course_id):
    print(user_id, course_id)
    course = Course.query.get_or_404(course_id)
    print(len(course.quizzes), "length")
    # if not is_auth():     
    #     return redirect(f"/logout/{id}?return_url=/practice/{id}")
    return render_template('quiz.html', quizzes=course.quizzes, enum = enumerate, len=len)

@app.route('/courses/<string:id>/<string:group_id>')
def course_(id, group_id):
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(id)
    courses = group.courses
    for course in courses:
        print(course.course_name)
    # if not is_auth():
    #     return redirect(f"/logout/{id}?return_url=http://localhost:5000/courses/{id}")
    user_activity(id)
    return render_template('course.html', user=user, group_id=group_id, courses=courses)

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

if __name__ == '__main__':
    app.run(debug=True)
