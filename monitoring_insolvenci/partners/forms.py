from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PartnerForm(FlaskForm):
    ico = StringField('IČO', validators=[DataRequired(), Length(max=8)])
    submit = SubmitField('Založit')


class ImportPartnerForm(FlaskForm):
    file = FileField('Soubor', validators=[FileRequired(), FileAllowed(['txt'], 'Jen txt soubor!')])
    submit = SubmitField('Přidat partnery ze souboru')
