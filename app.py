from flask import Flask, request, flash, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField,  PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Luc/AnacondaProjects/prs/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    papers = db.relationship('Paper', backref='user')
    
    def __repr__(self):
        return '<Author:{}>'.format(self.name)
    
class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)
    
    def __repr__(self):
        return '<Paper{}>'.format(self.title)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class PaperForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=4, max=15)])
    authors1 = SelectField('authors1', id ='paper_authors1')
    authors2 = SelectField('authors2', id ='paper_authors2')
    authors3 = SelectField('authors3', id ='paper_authors3')
    abstract = StringField('abstract', validators=[InputRequired(), Length(min=4, max=15)])


@app.route('/papers', methods = ['GET', 'POST'])
def papers():
    form = PaperForm()
    q = User.query.filter(User.username != session['username']).all()
    form.authors1.choices =  [(user.id, user.username) for user in q]
    form.authors2.choices =  [(user.id, user.username) for user in q]
    form.authors3.choices =  [(user.id, user.username) for user in q]
    if form.validate_on_submit():
            paper = Paper(title=form.title.data, authors=form.authors.data, author_id=form.abstract.data)
            db.session.add(paper)
            db.session.commit()
            flash('Paper was successfully submitted')
            return redirect(url_for('index'))
    return render_template('papers.html', form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                session['username'] = form.username.data
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        session['username'] = form.username.data
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
