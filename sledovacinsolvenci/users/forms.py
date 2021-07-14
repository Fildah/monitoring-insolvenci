from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

from flask_login import current_user
from sledovacinsolvenci.users.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    submit = SubmitField('Prihlasit')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Jmeno', validators=[DataRequired()])
    last_name = StringField('Prijmeni', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('Zopakuj Heslo', validators=[DataRequired()])
    submit = SubmitField('Registrovat')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email jiz ma platnou registraci')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Jmeno', validators=[DataRequired()])
    last_name = StringField('Prijmeni', validators=[DataRequired()])
    submit = SubmitField('Zmenit')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email jiz ma platnou registraci')