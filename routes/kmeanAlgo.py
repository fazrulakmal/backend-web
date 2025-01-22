from flask import Blueprint, jsonify, request
from models.Pelanggan import Pelanggan
from models import db
from datetime import datetime
from sqlalchemy import func
import numpy as np
from sklearn.cluster import KMeans
from models.Pelanggan import Pelanggan

kmeanAlgo_blueprint = Blueprint('kmeanAlgoRoute', __name__)




@kmeanAlgo_blueprint.route('/', methods=['GET'])
def calculate_kmeans():
    data = Pelanggan.query.all()
    listdata = Pelanggan([{'nama_penginapan':p.nama_penginapan, 'jumlah_pengguna':p.jumlah_pengguna, 'penggunaan_data_per_bulan':p.penggunaan_data_per_bulan, 'penghasilan_per_bulan':p.penghasilan_per_bulan} for p in Pelanggan])
    
    df = pd.DataFrame(data)

    # Selecting features for clustering
    features = df[["jumlah_pengguna", "penggunaan_data_per_bulan", "penghasilan_per_bulan"]]

    # Applying K-Means
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(features)