from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PartnerForm(FlaskForm):
    ico = StringField('ICO', validators=[DataRequired(), Length(max=8)])
    submit = SubmitField('Zalozit')


class ImportPartnerForm(FlaskForm):
    file = FileField('Soubor', validators=[FileRequired(), FileAllowed(['txt'], 'Jen txt soubor!')])
    submit = SubmitField('Pridat partnery ze souboru')
