from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbname.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@host/databaser'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models