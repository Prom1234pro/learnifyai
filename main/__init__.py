from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from .models import db
from .config import Config

app = Flask(__name__)
bcrypt = Bcrypt(app)
from .register import register_routes

def create_app():
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    register_routes(app)
    Session(app)

    return app, bcrypt

