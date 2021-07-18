from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PartnerForm(FlaskForm):
    ico = StringField('ICO', validators=[DataRequired()])
    submit = SubmitField('Zalozit')
