from flask import Flask
# from flask_jwt_extended import JWTManager
from models import db
# from auth import auth
from config import Config
from flask_cors import CORS

from routes.PelangganRoute import dataPelanggan_blueprint
# from routes.kmeanAlgo import kmeanAlgo_blueprint

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
# jwt = JWTManager(app)

app.register_blueprint(dataPelanggan_blueprint, url_prefix='/api/datapelanggan')
# app.register_blueprint(kmeanAlgo_blueprint, url_prefix='/api/kmeanalgo')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)