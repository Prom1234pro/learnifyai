from flask import session





def is_auth():
    if 'user' in session:
        return True
    else:
        return False
