import datetime

import jwt
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from monitoring_insolvenci import config
from monitoring_insolvenci.extensions import db, login_manager

# Spojova tabulka mezi User a Partner
user2partner = db.Table('user2partner', db.Column('id', db.Integer, primary_key=True),
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                        db.Column('partner_id', db.Integer, db.ForeignKey('partners.id'))
                        )


# Funkce pro naceteni uzivatele v ramci rozsireni Flask_Login
# Prijima int id uzivatel
# Vraci User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Trida User pro ukladani uzivatelu
class User(db.Model, UserMixin):
    # Parametry tabulky
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

    # Inicializace tridy
    # Prijima string email, firts_name, last_name a password
    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        self.token = jwt.encode({"user_id": self.id}, config.SECRET_KEY, algorithm="HS256")

    # Generuje slovnik z atributu instance User
    # Vraci slovnik s udaji Usera
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

    # Porovnava hesla
    # Prijima heslo k provnani
    # Vraci boolean
    def password_check(self, password):
        return check_password_hash(self.password, password)

    # Porovnava tokeny
    # Prijima token k provnani
    # Vraci boolean
    def jwt_check(self, token):
        if self.token == token:
            return True
        else:
            return False

    # Meni parametr admin
    def toggle_admin(self):
        self.admin = not self.admin
        db.session.commit()

    # Meni parametr active
    def toggle_active(self):
        self.active = not self.active
        db.session.commit()
