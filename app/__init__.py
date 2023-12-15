import os, secrets
from flask import Flask, request
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import logging
from logging import Formatter
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


class RequestFormatter(Formatter):
    def format(self, record):
        if request:
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.user = current_user.get_id() if current_user.is_authenticated else 'Anonymous'
        else:
            record.url = None
            record.remote_addr = None
            record.user = 'No request context'

        return super().format(record)

# Define the log format you want to use
log_format = "[%(asctime)s] %(remote_addr)s requested %(url)s with user %(user)s\n" \
             "%(levelname)s in %(module)s: %(message)s"

formatter = RequestFormatter(log_format)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.addHandler(handler)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models