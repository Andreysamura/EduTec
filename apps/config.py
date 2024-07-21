import os
import random
import string
from flask_mail import Mail

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))

    # Social AUTH context
    SOCIAL_AUTH_GITHUB = False
    GITHUB_ID = os.getenv('GITHUB_ID', None)
    GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)

    # Enable/Disable Github Social Login
    if GITHUB_ID and GITHUB_SECRET:
        SOCIAL_AUTH_GITHUB = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database Configuration
    DB_ENGINE = 'mysql'
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASS = os.getenv('DB_PASS', 'VfooWpTHzoSisQxakVLHSBijpzuFnEKA')
    DB_HOST = os.getenv('DB_HOST', 'hviaduct.proxy.rlwy.net')
    DB_PORT = os.getenv('DB_PORT', '57378')
    DB_NAME = os.getenv('DB_NAME', 'integradora')

    SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'josendreyd551@outlook.com'
    MAIL_PASSWORD = 'Monaguillo'
    MAIL_DEFAULT_SENDER = 'josendreyd551@outlook.com'

# Inicializar Flask-Mail
mail = Mail()

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True

config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
