import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.auth import auth

DB_NAME = 'passman.db'

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/user")


db = SQLAlchemy()
app.config.from_mapping(
    SECRET_KEY='developer',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}'
)
db.init_app(app)

from website import routes
from website.models import User, Login, Note, CreditCard

with app.app_context():
    db.create_all()
