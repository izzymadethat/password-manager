import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models import User, Login, Note, CreditCard

DB_NAME = 'passman.db'

app = Flask(__name__)
db = SQLAlchemy()
app.config.from_mapping(
    SECRET_KEY='developer',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}'
)
db.init_app(app)

with app.app_context():
    db.create_all()
    
from website import routes
