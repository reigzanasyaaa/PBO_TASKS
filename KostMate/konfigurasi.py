# konfigurasi.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'kostmate.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

KATEGORI_PENGELUARAN = [
    "Makanan & Minuman",
    "Transportasi",
    "Tagihan & Utilitas",
    "Belanja Kebutuhan",
    "Hiburan & Rekreasi",
    "Kesehatan",
    "Pendidikan",
    "Perawatan Diri",
    "Lainnya"
]

KATEGORI_PEMASUKAN = [
    "Uang Saku",
    "Gaji / Freelance",
    "Transfer Orang Tua",
    "Beasiswa",
    "Penjualan",
    "Lainnya"
]

KATEGORI_LOG = [
    "Olahraga",
    "Belajar",
    "Kebersihan Kamar",
    "Belanja Bulanan",
    "Memasak",
    "Ibadah",
    "Istirahat / Tidur",
    "Sosial / Networking",
    "Lainnya"
]

KATEGORI_TAGIHAN = [
    "Sewa Kos", "Listrik", "Air", "WiFi/Internet", "Lainnya"
]

ITEM_BELANJA_DEFAULT = [
    "Sabun mandi", "Sampo", "Pasta gigi", "Deterjen",
    "Beras", "Minyak goreng", "Telur", "Mie instan",
    "Tisu", "Sabun cuci piring", "Galon air minum", 
    "Skincare", "Obat-obatan", "Vitamin", "Snack", "Buah-buahan"
]

KATEGORI_DEFAULT = "Lainnya"

APP_NAME = "KostMate"
APP_TAGLINE = "Sistem Manajemen Keuangan & Log Kebutuhan Mandiri Penghuni Kos"
