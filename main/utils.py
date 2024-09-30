from functools import wraps
from flask import flash, redirect, url_for, abort, session

from main.authentication.models import Profile, User


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for('auth.login_user_'))
        
        user = User.query.get(user_id)
        if not user:
            flash('You need to log in to access this page.', 'warning')
            return redirect(url_for('auth.login_user_'))  # Redirect to the login page
        return f(*args, **kwargs)
    return decorated_function

def onboarding_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('onboarding_id')
        if not user_id:
            return redirect(url_for('auth.create_user'))  # Redirect to the login page
        
        user = User.query.get(user_id)
        if not user:
            flash('You need to log in to access this page.', 'warning')
            return redirect(url_for('auth.create_user'))  # Redirect to the login page
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        print(user_id)
        if not user_id:
            print("always here")
            return abort(404)
        
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            print("always here 2")
            return abort(404)
        
        return f(*args, **kwargs)
    return decorated_function

def premium_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user').is_premium_user:
            flash('This page is only accessible to premium users.', 'warning')
            return redirect(url_for('upgrade_to_premium'))  # Redirect to upgrade page
        return f(*args, **kwargs)
    return decorated_function

import re

def validate_format(text):
    lines = text.splitlines()
    # lines.append('\n')  
    # lines.append('\n')  


    expected_structure = [
        (r'^(Current Instruction: .*)?$', "Current Instruction is optional but if present, it should be in the format 'Current Instruction: ...'"),
        (r'^.+\?$', "Question should end with a question mark."),
        # (r'^Topic Name: .+$', "Topic Name should be in the format 'Topic Name: ...'"),
        (r'^.+$', "Answer option 1 should be a non-empty line."),
        (r'^.+$', "Answer option 2 should be a non-empty line."),
        (r'^.+$', "Answer option 3 should be a non-empty line."),
        (r'^.+(, true)?$', "Answer option 4 should be a non-empty line, optionally ending with ', true'."),
        (r'^$', "A single empty line is expected here."),
    ]

    if not re.match(r'^School Code: .+$', lines[0].strip()):
        return False, "Error: First line should be 'School Code: ...'"
    if not re.match(r'^School: .+$', lines[1].strip()):
        return False, "Error: First line should be 'School: ...'"
    if not re.match(r'^Subject: .+$', lines[2].strip()):
        return False, "Error: First line should be 'Subject: ...'"
    if not re.match(r'^Year: \d{4}$', lines[3].strip()):
        return False, "Error: Second line should be 'Year: YYYY'"
    if not re.match(r'^$', lines[4].strip()):
        return False, "Error: Third line should be an empty line."
    
    i = 5
    structure_index = 0

    while i < len(lines):
        pattern, error_message = expected_structure[structure_index]
        if pattern == r'^(Current Instruction: .*)?$' and not re.match(r'^Current Instruction: .*$', lines[i].strip()):
            structure_index += 1 
            continue

        if not re.match(pattern, lines[i].strip()):
            return False, f"Error on line {i+1}: {error_message}"
        
        if structure_index == 7:
            options = [lines[i-4].strip(), lines[i-3].strip(), lines[i-2].strip(), lines[i-1].strip()]
            print(options)
            if sum(1 for option in options if re.search(r', true$', option)) != 1:
                return False, f"Error on lines {i-3} to {i}: Exactly one answer option must end with ', true'."

        i += 1
        structure_index += 1
        if structure_index >= len(expected_structure):
            structure_index = 0

    return True, "The file follows the correct format."


