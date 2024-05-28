from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import main.config
from .models.models import db
from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.update(main.config.as_dict())
mail = Mail(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# from .routes import register_routes

def create_app():
    db.init_app(app)
    Migrate(app, db)
    # register_routes(app)
    Session(app)

    return app, bcrypt

