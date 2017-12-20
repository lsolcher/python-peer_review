from flask import Flask, request, flash, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import PaperForm, ReviewerForm, LoginForm, RegisterForm, RateForm
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Luc/AnacondaProjects/prs/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

paper_authors = db.Table('paper_authors', db.Model.metadata,
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'))
                          )

paper_reviewers = db.Table('paper_reviewers', db.Model.metadata,
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'))
                          )
 
class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    papers = db.relationship("Paper", 
                             secondary=paper_authors,
                             backref="written"
                            )
    reviews = db.relationship("Paper", 
                             secondary=paper_reviewers,
                             backref="reviews"
                            )
    
    def __repr__(self):
        return '<Author:{}>'.format(self.username)
    
    #def admin(self):
    #    return self.is_admin

    
class Paper(db.Model):
    #__tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=0)
    authors = db.relationship("User",
                              secondary=paper_authors,
                              backref="author"
                             )
    reviewers = db.relationship("User",
                              secondary=paper_reviewers,
                              backref="reviewer"
                             )
    
    
    def __repr__(self):
        return '<Paper{}>'.format(self.title)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/papers', methods = ['GET', 'POST'])
@login_required
def papers():
    form = PaperForm()
    q = User.query.all()
    form.authors.choices =  [(user.id, user.username) for user in q]
    if form.validate_on_submit():
            a = User.query.filter(User.id.in_(form.authors.data)).all()
            if len(a) == 0 or len(a) > 3:
                flash('Specify at least 1 and at most 3 authors', 'error')
            else:
                #a = q.filter(User.id.in_(form.authors.data))
                #a = User.query.get(form.authors.data)
                papertitle = form.title.data + " by "
                for author in a:
                    papertitle += author.username + ", "
                papertitle = papertitle[:-2]
                paper = Paper(title=papertitle, abstract=form.abstract.data, authors=a)#authors=[user]) #authors=dict(form.authors.choices).get(form.authors.data))            
                db.session.add(paper)
                db.session.commit()
                flash('Paper was successfully submitted')
                #return redirect(url_for('index'))
    return render_template('papers.html', form=form)

@app.route('/assign_reviewers', methods = ['GET', 'POST'])
@login_required
def assign_reviewers():
    print(current_user)
    print(current_user.is_admin)
    if current_user.is_admin == False:
        return render_template('403.html'), 403
    form = ReviewerForm()
    qP = Paper.query.all()
    form.paper.choices = [(paper.id, paper.title) for paper in qP]
    #qU = User.query.filter(User.username != session['username']).all()
    qU = User.query.all()
    form.reviewers.choices =  [(user.id, user.username) for user in qU]
    if form.validate_on_submit():      
            reviewer = User.query.filter(User.id.in_(form.reviewers.data)).all()
            paperID = form.paper.data
            paperObject =  Paper.query.get(paperID)
            invalid = False
            if len(reviewer) == 0:
                flash('Specify at least 1 author you want to be reviewer', 'error')   
                invalid = True
            if invalid == False:
                for r in reviewer:
                    for p in r.papers:
                        if p == paperObject:
                            invalid = True
                            flash('One or more of the chosen reviewers are author(s) of the chosen paper. Please select only reviewers who are no authors.')           
            if invalid == False:
                for r in reviewer:
                    r.reviews.append(paperObject)
                    paperObject.reviewers.append(r)
                db.session.commit()
                flash('Successfully assigned reviewers')
    return render_template('assign_reviewers.html', form=form)

@app.route('/rate_papers', methods = ['GET', 'POST'])
@login_required
def rate_papers():
    form = RateForm()
    #qP = Paper.query.filter(Paper.reviewers.any(paper.id=paper_id)).all()
    #print(qP)
    children = Paper.reviewers.any()
    qP = session.query(Paper, children)
    form.paper.choices = [(paper.id, paper.title) for paper in qP]
    #qU = User.query.filter(User.username != session['username']).all()
    #qU = User.query.all()
    #form.reviewers.choices =  [(user.id, user.username) for user in qU]
    if form.validate_on_submit():   
        paperID = form.paper.data
        paperObject =  Paper.query.get(paperID)
        paperObject.rating =form.score.data
        db.session.commit()
        flash('Successfully submitted your rating')
    return render_template('rate_papers.html', form=form)


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
                session['admin'] = user.is_admin
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
    #papers_to_review = Paper.query.filter()
    data=[]
    return render_template('dashboard.html', name=current_user.username,data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('403.html'), 403

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()
    
def create_admin():
    exists = User.query.filter_by(email='admin@test.de').first()
    if not exists:
        hashed_password = generate_password_hash('admin', method='sha256')
        user = User(username='admin', email='admin@test.de', password=hashed_password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        

    

if __name__ == '__main__':
    init_db()
    create_admin()
    app.run(debug=True)
