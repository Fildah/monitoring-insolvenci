from flask_httpauth import HTTPTokenAuth
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from monitoring_insolvenci.config import LOGIN_MESSAGE, LOGIN_MESSAGE_CATEGORY, REFRESH_MESSAGE, \
    REFRESH_MESSAGE_CATEGORY

# Inicializce rozsireni
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
api_auth = HTTPTokenAuth()

# Prepsani zprav v rozsireni Flask_Login
login_manager.login_message = LOGIN_MESSAGE
login_manager.login_message_category = LOGIN_MESSAGE_CATEGORY
login_manager.needs_refresh_message = REFRESH_MESSAGE
login_manager.needs_refresh_message_category = REFRESH_MESSAGE_CATEGORY
