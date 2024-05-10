import json
from datetime import timedelta
from flask import session


SESSION_TIMEOUT = timedelta(hours=24)
ACTIVE_SESSIONS_FILE = 'active_sessions.json'

def load_active_sessions():
    try:
        with open(ACTIVE_SESSIONS_FILE) as file:
            active_sessions_serializable = json.load(file)
            # Convert ISO format strings back to datetime objects
            return {
                user_id: {
                    'email': session_data['email'],
                    'last_activity': session_data['last_activity']
                } for user_id, session_data in active_sessions_serializable.items()
            }
    except FileNotFoundError:
        return {}

# Load active sessions from the JSON file when the application starts

def save_active_sessions(active_sessions):
    with open(ACTIVE_SESSIONS_FILE, 'w') as file:
        json.dump(active_sessions, file)


def is_auth():
    if 'user' in session:
        return True
    else:
        return False