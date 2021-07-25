import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sledovacinsolvenci.extensions import db, login_manager
from sledovacinsolvenci.partners.models import user2partner


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
    partners = db.relationship('Partner', secondary=user2partner, backref=db.backref('users'), lazy='dynamic')

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()

    def password_check(self, password):
        return check_password_hash(self.password, password)
