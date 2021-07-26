from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sledovacinsolvenci.config import LOGIN_MESSAGE, LOGIN_MESSAGE_CATEGORY, REFRESH_MESSAGE, REFRESH_MESSAGE_CATEGORY

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Czech for LoginManager
login_manager.login_message = LOGIN_MESSAGE
login_manager.login_message_category = LOGIN_MESSAGE_CATEGORY
login_manager.needs_refresh_message = REFRESH_MESSAGE
login_manager.needs_refresh_message_category = REFRESH_MESSAGE_CATEGORY
