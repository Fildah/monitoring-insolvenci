from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PartnerForm(FlaskForm):
    ico = StringField('ICO', validators=[DataRequired(), Length(max=8)])
    submit = SubmitField('Zalozit')
