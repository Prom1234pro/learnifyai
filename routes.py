from flask import Blueprint, request, jsonify

from .models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/customer/register', methods=['POST'])
def user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')