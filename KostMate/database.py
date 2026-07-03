# database.py
import sqlite3
import pandas as pd
from konfigurasi import DB_PATH


def get_db_connection() -> sqlite3.Connection | None:
    """Membuka dan mengembalikan koneksi baru ke database SQLite."""
    try:
        conn = sqlite3.connect(
            DB_PATH,
            timeout=10,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"[DB ERROR] Gagal membuka koneksi: {e}")
        return None


def execute_query(sql: str, params: tuple = (), fetch: bool = False):
    """
    Mengeksekusi query SQL (INSERT, UPDATE, DELETE, CREATE).
    Jika fetch=True, mengembalikan list of Row hasil SELECT.
    """
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[DB ERROR] Gagal eksekusi query: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def fetch_as_dataframe(sql: str, params: tuple = ()) -> pd.DataFrame | None:
    """Mengambil hasil SELECT dan mengembalikan sebagai DataFrame Pandas."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        df = pd.read_sql_query(sql, conn, params=params)
        return df
    except Exception as e:
        print(f"[DB ERROR] Gagal fetch DataFrame: {e}")
        return None
    finally:
        conn.close()


def setup_database():
    """Membuat semua tabel yang dibutuhkan aplikasi."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()

        # Tabel Transaksi Keuangan
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipe TEXT NOT NULL CHECK(tipe IN ('pengeluaran', 'pemasukan')),
                deskripsi TEXT NOT NULL,
                jumlah REAL NOT NULL CHECK(jumlah > 0),
                kategori TEXT,
                tanggal DATE NOT NULL,
                catatan TEXT
            );
        """)

        # Tabel Log Kegiatan Harian
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_kegiatan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aktivitas TEXT NOT NULL,
                kategori TEXT,
                durasi_menit INTEGER DEFAULT 0,
                tanggal DATE NOT NULL,
                waktu TEXT,
                catatan TEXT,
                selesai INTEGER DEFAULT 0
            );
        """)

        # Tabel Target Tabungan
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS target_tabungan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_target TEXT NOT NULL,
                jumlah_target REAL NOT NULL,
                terkumpul REAL DEFAULT 0,
                deadline DATE,
                deskripsi TEXT,
                aktif INTEGER DEFAULT 1
            );
        """)

        # Tabel Tagihan Bulanan
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tagihan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kategori TEXT,
                jumlah REAL NOT NULL,
                tanggal_jatuh_tempo TEXT,
                sudah_bayar INTEGER DEFAULT 0,
                catatan TEXT
            );
        """)

        # Tabel Checklist Belanja
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS belanja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                jumlah TEXT DEFAULT '1',
                sudah_beli INTEGER DEFAULT 0,
                catatan TEXT
            );
        """)

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[DB ERROR] Gagal setup database: {e}")
        return False
    finally:
        conn.close()
