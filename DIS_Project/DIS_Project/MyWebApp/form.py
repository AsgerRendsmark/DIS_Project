from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea

class searchForm(FlaskForm):
    search = StringField('Searched', validators = [DataRequired()])
    submit = SubmitField('submit') 