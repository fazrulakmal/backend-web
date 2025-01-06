from flask import Flask
# from flask_jwt_extended import JWTManager
from models import db
# from auth import auth
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
# jwt = JWTManager(app)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)