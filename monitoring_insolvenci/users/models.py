import datetime

import jwt
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from monitoring_insolvenci import config
from monitoring_insolvenci.extensions import db, login_manager

user2partner = db.Table('user2partner', db.Column('id', db.Integer, primary_key=True),
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                        db.Column('partner_id', db.Integer, db.ForeignKey('partners.id'))
                        )


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
    token = db.Column(db.String(512), default=None)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    partners = db.relationship('Partner', secondary=user2partner, backref=db.backref('users'), lazy='dynamic')

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        self.token = jwt.encode({"user_id": self.id}, config.SECRET_KEY, algorithm="HS256")

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created': self.created,
            'modified': self.modified,
            'token': self.token,
            'admin': self.admin,
            'toggle_admin_link': url_for('users.toggle_admin', user_id=self.id),
            'toogle_active_link': url_for('users.toogle_active', user_id=self.id),
            'active': self.active
        }

    def password_check(self, password):
        return check_password_hash(self.password, password)

    def jwt_check(self, token):
        if self.token == token:
            return True
        else:
            return False

    def toggle_admin(self):
        self.admin = not self.admin
        db.session.commit()

    def toggle_active(self):
        self.active = not self.active
        db.session.commit()
