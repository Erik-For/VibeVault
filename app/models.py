from app import db
from flask_login import UserMixin
import bcrypt

class User(db.Model, UserMixin):
    __tablename = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    usertype = db.Column(db.Integer, default=0) # 0 default, 1 admin, 2 super user
    email = db.Column(db.String(100), unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(32))

    def __init__(self, email, username, password):
        self.email = email.lower()
        self.username = username
        self.display_name = username
        self.password = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def is_admin(self):
        return (self.usertype >= 1)

    def is_super_user(self):
        return (self.usertype == 2)

    def check_password(self, password):
        return bcrypt.checkpw(str(password).encode('utf-8'), self.password.encode('utf-8'))
   