# routes/CRUDcustomers.py

from urllib import response
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models.Pelanggan import Pelanggan
from models import db
from datetime import datetime
from sqlalchemy import func

dataPelanggan_blueprint = Blueprint('PelangganRoute', __name__)

# Create (Add new customer)
@dataPelanggan_blueprint.route('/', methods=['POST'])
@cross_origin()  # This will add CORS headers to this route
def create_customer():
        data = request.json
        new_customer = Pelanggan(
            namaPenginapan=data.get('namaPenginapan'),
            jumlahPenginapan=data.get('jumlahPenginapan'),
            penggunaanData=data.get('penggunaanData'),
            penghasilanBulan=data.get('penghasilanBulan'),
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"status": "Customer created"}), 201


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
