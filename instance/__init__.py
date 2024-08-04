from datetime import timedelta
import json
from abc import ABC

with open('./instance/secrets.json', 'r') as f:
    secrets = json.load(f)

class IFlaskDefaultConfiguration(ABC):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = None
    TRAP_HTTP_EXCEPTIONS = False
    TRAP_BAD_REQUEST_ERRORS = None
    SECRET_KEY = None
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = None
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_REFRESH_EACH_REQUEST = True
    USE_X_SENDFILE = False
    SEND_FILE_MAX_AGE_DEFAULT = None
    SERVER_NAME = None
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'
    MAX_CONTENT_LENGTH = None
    TEMPLATES_AUTO_RELOAD = None
    EXPLAIN_TEMPLATE_LOADING = False
    MAX_COOKIE_SIZE = 4093

class IApplicationConfiguration(IFlaskDefaultConfiguration):
    SECRET_KEY = secrets['key'] # type: ignore
    GOOGLE_CLIENT_SECRETS = secrets['web']
    DEBUG=True
    TESTING=True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.db'
    SQLALCHEMY_ECHO=True
    
class Development(IApplicationConfiguration):
    TESTING=False

class Testing(IApplicationConfiguration):
    DEBUG=False
    PROPAGATE_EXCEPTIONS = False # type: ignore

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO=False

class Deployment(IApplicationConfiguration):
    DEBUG=False
    TESTING=False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
    SQLALCHEMY_ECHO=False

