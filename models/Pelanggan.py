from models import db

class Pelanggan(db.Model):
    __tablename__ = 'pelanggan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_penginapan = db.Column(db.String, nullable=False)
    jumlah_pengguna = db.Column(db.Integer, nullable=False)
    penggunaan_data_per_bulan = db.Column(db.Integer, nullable=False)  # Dalam GB
    penghasilan_per_bulan = db.Column(db.Integer, nullable=False)  # Dalam Rupiah

    def __repr__(self):
        return f"<Penginapan(nama_penginapan='{self.nama_penginapan}', jumlah_pengguna={self.jumlah_pengguna}, penggunaan_data={self.penggunaan_data_per_bulan} GB, penghasilan={self.penghasilan_per_bulan} IDR)>"