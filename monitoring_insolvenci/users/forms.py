from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from monitoring_insolvenci.users.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    submit = SubmitField('Přihlásit')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Jméno', validators=[DataRequired()])
    last_name = StringField('Příjmení', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('Zopakuj Heslo', validators=[DataRequired()])
    submit = SubmitField('Registrovat')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email již má platnou registraci')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Jméno', validators=[DataRequired()])
    last_name = StringField('Příjmení', validators=[DataRequired()])
    submit = SubmitField('Aktualizovat')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email již má platnou registraci')


class GenerateApiTokenForm(FlaskForm):
    token = StringField('Token')
    submit = SubmitField('Zobrazit token')
