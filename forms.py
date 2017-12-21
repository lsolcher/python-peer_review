from wtforms import StringField, SelectMultipleField,  PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, Length
from flask_wtf import FlaskForm 
from flask_table import Table, Col, BoolCol, ButtonCol, LinkCol

DEFAULT_CHOICES = []
SCORE = [(-2, '-2 - totally unacceptable'),(-1, '-1 - deficient'),(0, '0 - sufficient'),(1, '1 - good'),(2, '2 - just as awesome as this lab submission')]


class LoginForm(FlaskForm):
    username = StringField('Username or email', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

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

class PaperOverviewTable(Table):
    title = Col('Papertitle   ')
    abstract = Col('   Abstract   ')
    authors = Col('   Authors   ')
    score = Col('   Ratings   ')
    is_accepted = BoolCol('   Accepted   ')
    accept = LinkCol('   Assesss   ', 'score_overview', url_kwargs=dict(id='id'))
    
    
