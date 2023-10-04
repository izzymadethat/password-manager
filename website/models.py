from website import db
from datetime import datetime

class User(db.Model):
    """DB Model for User Account Information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    logins = db.relationship('Login', backref='logins', lazy=True)
    notes = db.relationship('Note', backref='notes', lazy=True)
    cards= db.relationship('CreditCard', backref='cards', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}' '{self.image_file}')"
    
class Login(db.Model):
    """DB Model for User Login Entry."""
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(100), default=website)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    note = db.Column(db.Text)
    favorite = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Note(db.Model):
    """DB Model for User Secure Notes."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    entry = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    primary = db.Column(db.Boolean) 
