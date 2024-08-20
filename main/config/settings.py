import os
from datetime import timedelta
from dotenv import load_dotenv
import urllib

load_dotenv()


class BaseConfig():
   API_PREFIX = '/api'
   TESTING = False
   DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    UPLOAD_FOLDER = 'main\\static\\media'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=6)
    SESSION_TYPE = 'filesystem'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@db-postgres:5432/flask-deploy'
    # CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
    # CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'


class ProductionConfig(BaseConfig):
    FLASK_ENV = os.environ.get("FLASK_ENV")
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=6)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    UPLOAD_FOLDER = 'main/static/media'
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    PASSWORD = os.environ.get("PASSWORD")

    # Create the connection string
    SESSION_TYPE = 'filesystem'

    # CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
    # CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'


class TestConfig(BaseConfig):
   FLASK_ENV = 'development'
   TESTING = True
   DEBUG = True
   # make celery execute tasks synchronously in the same process
   CELERY_ALWAYS_EAGER = True