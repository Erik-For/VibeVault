import secrets
from app import app
import os

if not os.path.exists(".flaskenv"):
    with open(".flaskenv", "w") as file:
        file.write("FLASK_APP=run.py\n")
        file.write("SECRET_KEY=" + secrets.token_hex())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
