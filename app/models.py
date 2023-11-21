from app import db
from flask_login import UserMixin
import bcrypt

class User(db.Model, UserMixin):
    __tablename = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.display_name = username
        self.password = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')