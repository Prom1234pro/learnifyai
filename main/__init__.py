from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import main.config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.update(main.config.as_dict())
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'promiseimadonmwinyi@gmail.com'
app.config['MAIL_PASSWORD'] = 'pdvmtnuuqktbuhbi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
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

