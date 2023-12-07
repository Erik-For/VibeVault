import os, secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=("Twatter - Verify your Email", os.getenv('MAIL_USERNAME'))
)

app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex())

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbname.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/vault'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models