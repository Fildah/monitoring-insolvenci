import os

from dotenv import load_dotenv

# Nacteni .env
load_dotenv()

# Nastaveni zprav Flask_Login
LOGIN_MESSAGE = u'Pro přístup k této stránce je potřeba se přihlásit.'
LOGIN_MESSAGE_CATEGORY = 'warning'
REFRESH_MESSAGE = u'Pro přístup k této stránce se prosím znovu přihlašte.'
REFRESH_MESSAGE_CATEGORY = 'warning'

# Globalni nastaveni aplikace
SERVER_NAME = os.environ.get('SERVER_NAME')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = (os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True')
SECRET_KEY = os.environ.get('SECRET_KEY')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_SSL = (os.environ.get('MAIL_USE_SSL') == 'True')
MAIL_USE_TLS = (os.environ.get('MAIL_USE_TLS') == 'True')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
