from wtforms import StringField, SelectMultipleField,  PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, Length
from flask_wtf import FlaskForm 

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

DEFAULT_CHOICES = []
SCORE = [(-2, '-2'),(-1, '-1'),(0, '0'),(1, '1'),(2, '2')]

class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""
        
class NoValidationSelectField(SelectField):
    def pre_validate(self, form):
        """per_validation is disabled"""

class PaperForm(FlaskForm):    
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=15)])
    authors = NoValidationSelectMultipleField('Authors', choices = DEFAULT_CHOICES)
    abstract = TextAreaField('Abstract', validators=[InputRequired(), Length(min=1)])

class ReviewerForm(FlaskForm):
    paper = NoValidationSelectField('Paper', choices = DEFAULT_CHOICES)
    reviewers = NoValidationSelectMultipleField('Reviewers',choices =  DEFAULT_CHOICES)
    
class RateForm(FlaskForm):
    paper = NoValidationSelectField('Paper', choices = DEFAULT_CHOICES)
    score = SelectField('Score',choices = SCORE, coerce=int)
