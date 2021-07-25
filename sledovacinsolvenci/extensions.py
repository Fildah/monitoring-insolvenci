from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Czech for LoginManager
login_manager.login_message = u'Pro přístup k této stránce je potřeba se přihlásit.'
login_manager.login_message_category = 'warning'
login_manager.needs_refresh_message = u'Pro přístup k této stránce se prosím znovu přihlašte.'
login_manager.needs_refresh_message_category = 'warning'
