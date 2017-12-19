# -*- coding: utf-8 -*-
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()

class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    is_reviewer = db.Column(db.Boolean, default=False, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    papers = db.relationship("Paper", 
                             secondary=association_table,
                             backref="User"
                            )
    
    def __repr__(self):
        return '<Author:{}>'.format(self.username)
    
class Paper(db.Model):
    #__tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=0)
    authors = db.relationship("User",
                              secondary=association_table,
                              backref="Paper"
                             )
    
    def __repr__(self):
        return '<Paper{}>'.format(self.title)