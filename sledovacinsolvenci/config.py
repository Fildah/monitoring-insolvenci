import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:example@localhost/sledovacinsolvenci'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'tempsecretkey'
