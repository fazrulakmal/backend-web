# routes/CRUDcustomers.py

from urllib import response
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models.Pelanggan import Pelanggan
from models import db
from datetime import datetime
from sqlalchemy import func
import numpy as np
from sklearn.cluster import KMeans
from models.Pelanggan import Pelanggan

dataPelanggan_blueprint = Blueprint('PelangganRoute', __name__)

@dataPelanggan_blueprint.route('/', methods=['POST'])
@cross_origin()  # This will add CORS headers to this route
def create_customer():
    data = request.json  # Get JSON data from the request
    
    if isinstance(data, list):  # Check if the data is a list
        try:
            new_customers = []  # Collect all new customers
            for item in data:
                # Validate required fields
                if not all([item.get('namaPenginapan'), item.get('jumlahPengguna')]):
                    return jsonify({"error": "Missing required fields"}), 400
                
                # Create a new customer object
                new_customer = Pelanggan(
                    nama_penginapan=item.get('namaPenginapan'),
                    jumlah_pengguna=item.get('jumlahPengguna'),
                    penggunaan_data_per_bulan=item.get('penggunaanData', ''),  # Default to empty string if not provided
                    penghasilan_per_bulan=item.get('penghasilanBulan', ''),    # Default to empty string if not provided
                )
                db.session.add(new_customer)  # Add to session
                new_customers.append(new_customer)

            db.session.commit()  # Commit all changes at once
            return jsonify({"status": "Customers created", "count": len(new_customers)}), 201
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return jsonify({"error": str(e)}), 400

    elif isinstance(data, dict):  # Process single record
        try:
            # Validate required fields
            if not all([data.get('namaPenginapan'), data.get('jumlahPengguna')]):
                return jsonify({"error": "Missing required fields"}), 400

            # Create a single customer
            new_customer = Pelanggan(
                nama_penginapan=data.get('namaPenginapan'),
                jumlah_pengguna=data.get('jumlahPengguna'),
                penggunaan_data_per_bulan=data.get('penggunaanData', ''),
                penghasilan_per_bulan=data.get('penghasilanBulan', ''),
            )
            db.session.add(new_customer)
            db.session.commit()
            return jsonify({"status": "Customer created", "id": new_customer.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    else:
        return jsonify({"error": "Invalid data format"}), 400



# Read (Fetch all customers)
@dataPelanggan_blueprint.route('/', methods=['GET'])
def get_customers():
    customers = Pelanggan.query.all()
    customers_list = [{'id': c.id, 'nama_penginapan': c.nama_penginapan, 'jumlah_pengguna': c.jumlah_pengguna,'penggunaan_data_per_bulan': c.penggunaan_data_per_bulan,'penghasilan_per_bulan': c.penghasilan_per_bulan} for c in customers]
    return jsonify(customers_list), 200

# Read (Fetch single customer by ID)
@dataPelanggan_blueprint.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Pelanggan.query.get_or_404(id)
    return jsonify({'id': c.id, 'nama_penginapan': c.nama_penginapan, 'jumlah_pengguna': c.jumlah_pengguna,'penggunaan_data_per_bulan': c.penggunaan_data_per_bulan,'penghasilan_per_bulan': c.penghasilan_per_bulan}), 200

# Update (Modify existing customer by ID)
# @dataPelanggan_blueprint.route('/<int:id>', methods=['PUT'])
# def update_customer(id):
#     data = request.json
#     customer = Customer.query.get_or_404(id)
#     customer.name = data.get('name')
#     customer.email = data.get('email')
#     customer.phone = data.get('phone')
#     customer.subscription = data.get('subscription')
#     signup_date_str = data.get('signup_date')
#     if signup_date_str:
#         customer.signup_date = datetime.strptime(signup_date_str, '%Y-%m-%dT%H:%M')

#     db.session.commit()

#     return jsonify({'message': 'Customer updated successfully!'}), 200

# Delete (Remove customer by ID)
# @inputCustomers_blueprint.route('/<int:id>', methods=['DELETE'])
# def delete_customer(id):
#     customer = Customer.query.get_or_404(id)
#     db.session.delete(customer)
#     db.session.commit()

#     return jsonify({'message': 'Customer deleted successfully!'}), 200


# Read (Fetch all customers)

@dataPelanggan_blueprint.route('/kmeans_clustering', methods=['GET'])
def calculate_kmeans():
    # Fetch data from the database
    customers = Pelanggan.query.all()
    
    # Prepare the data for clustering
    customers_list = [
        {
            'jumlah_pengguna': c.jumlah_pengguna,
            'penggunaan_data_per_bulan': c.penggunaan_data_per_bulan,
            'penghasilan_per_bulan': c.penghasilan_per_bulan
        } 
        for c in customers
    ]
    
    # Convert data to NumPy array
    try:
        data = np.array([
            [
                float(c['jumlah_pengguna']),
                float(c['penggunaan_data_per_bulan']),
                float(c['penghasilan_per_bulan'])
            ]
            for c in customers_list
        ])
    except ValueError:
        return jsonify({"error": "Invalid data in database"}), 400

    # Check if data has enough points for clustering
    if len(data) < 3:
        return jsonify({"error": "Not enough data points for clustering"}), 400

    # Centroid awal (cluster 1 dan cluster 2)
    initial_centroids = np.array([
        [15, 1000, 6000000],  # Cluster 1
        [40, 2000, 10000000]  # Cluster 2
    ])

    # Ensure centroids have the same dimension as data
    if initial_centroids.shape[1] != data.shape[1]:
        return jsonify({"error": "Initial centroids dimensions do not match data dimensions"}), 400

    # K-means clustering dengan centroid awal
    kmeans = KMeans(n_clusters=2, init=initial_centroids, n_init=1, random_state=0)
    kmeans.fit(data)

    # Prepare the result
    result = {
        "Initial_Centroids": initial_centroids.tolist(),
        "Final_Centroids": kmeans.cluster_centers_.tolist(),
        "Clusters": kmeans.labels_.tolist()
    }

    return jsonify(result), 200

