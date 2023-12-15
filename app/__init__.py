import os, secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv(".flaskenv")

app = Flask(__name__)

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=("VibeVault", os.getenv('MAIL_USERNAME'))
)

mail = Mail(app)

app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex())

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbname.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1/vault'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
}


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models