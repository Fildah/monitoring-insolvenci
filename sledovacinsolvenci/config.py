import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:example@localhost/sledovacinsolvenci'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'tempsecretkey'
LOGIN_MESSAGE = u'Pro přístup k této stránce je potřeba se přihlásit.'
LOGIN_MESSAGE_CATEGORY = 'warning'
REFRESH_MESSAGE = u'Pro přístup k této stránce se prosím znovu přihlašte.'
REFRESH_MESSAGE_CATEGORY = 'warning'
