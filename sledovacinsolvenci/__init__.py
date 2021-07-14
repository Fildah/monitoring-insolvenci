import os.path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sledovacinsolvenci.core.views import core
from sledovacinsolvenci.error_pages.handlers import error_pages

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'data.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

app.register_blueprint(core)
app.register_blueprint(error_pages)
