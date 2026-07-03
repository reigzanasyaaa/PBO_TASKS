import datetime
import pandas as pd
from model import Transaksi, LogKegiatan, TargetTabungan
import database as db

class ManajerKeuangan:
    """
    Kelas utama yang mengelola semua operasi keuangan dan log kegiatan.
    Menerapkan prinsip Komposisi dan Pemisahan Tanggung Jawab (OOP).
    """

    def __init__(self):
        db.setup_database()

    # ─────────────────────────────────────────────
    # TRANSAKSI

    def tambah_transaksi(self, transaksi: Transaksi) -> bool:
        """Menyimpan satu transaksi baru ke database."""
        sql = """
            INSERT INTO transaksi (tipe, deskripsi, jumlah, kategori, tanggal, catatan)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        result = db.execute_query(sql, (
            transaksi.tipe,
            transaksi.deskripsi,
            transaksi.jumlah,
            transaksi.kategori,
            str(transaksi.tanggal),
            transaksi.catatan
        ))
        return result is not None

    def hapus_transaksi(self, id_transaksi: int) -> bool:
        """Menghapus satu transaksi berdasarkan ID."""
        sql = "DELETE FROM transaksi WHERE id = ?"
        result = db.execute_query(sql, (id_transaksi,))
        return result is not None

    def get_dataframe_transaksi(
        self,
        tipe: str = None,
        tanggal: datetime.date = None,
        bulan: int = None,
        tahun: int = None
    ) -> pd.DataFrame | None:
        """Mengambil semua transaksi sebagai DataFrame, dengan filter opsional."""
        conditions = []
        params = []

        if tipe:
            conditions.append("tipe = ?")
            params.append(tipe)
        if tanggal:
            conditions.append("tanggal = ?")
            params.append(str(tanggal))
        if bulan and tahun:
            conditions.append("strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?")
            params.append(f"{bulan:02d}")
            params.append(str(tahun))

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM transaksi {where} ORDER BY tanggal DESC, id DESC"
        return db.fetch_as_dataframe(sql, tuple(params))

    def hitung_total(self, tipe: str, tanggal: datetime.date = None,
                     bulan: int = None, tahun: int = None) -> float:
        """Menghitung total pemasukan atau pengeluaran."""
        conditions = ["tipe = ?"]
        params = [tipe]

        if tanggal:
            conditions.append("tanggal = ?")
            params.append(str(tanggal))
        if bulan and tahun:
            conditions.append("strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?")
            params.append(f"{bulan:02d}")
            params.append(str(tahun))

        where = f"WHERE {' AND '.join(conditions)}"
        sql = f"SELECT COALESCE(SUM(jumlah), 0) as total FROM transaksi {where}"
        result = db.execute_query(sql, tuple(params), fetch=True)
        if result:
            return float(result[0][0])
        return 0.0

    def get_pengeluaran_per_kategori(
        self,
        tanggal: datetime.date = None,
        bulan: int = None,
        tahun: int = None
    ) -> dict:
        """Mengambil total pengeluaran per kategori."""
        conditions = ["tipe = 'pengeluaran'"]
        params = []

        if tanggal:
            conditions.append("tanggal = ?")
            params.append(str(tanggal))
        if bulan and tahun:
            conditions.append("strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?")
            params.append(f"{bulan:02d}")
            params.append(str(tahun))

        where = f"WHERE {' AND '.join(conditions)}"
        sql = f"""
            SELECT kategori, SUM(jumlah) as total
            FROM transaksi {where}
            GROUP BY kategori
            ORDER BY total DESC
        """
        rows = db.execute_query(sql, tuple(params), fetch=True)
        if rows:
            return {row[0]: row[1] for row in rows}
        return {}

    def get_tren_harian(self, bulan: int, tahun: int) -> pd.DataFrame | None:
        """Mengambil data tren pengeluaran & pemasukan harian dalam sebulan."""
        sql = """
            SELECT tanggal,
                   SUM(CASE WHEN tipe='pengeluaran' THEN jumlah ELSE 0 END) as pengeluaran,
                   SUM(CASE WHEN tipe='pemasukan' THEN jumlah ELSE 0 END) as pemasukan
            FROM transaksi
            WHERE strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?
            GROUP BY tanggal
            ORDER BY tanggal ASC
        """
        return db.fetch_as_dataframe(sql, (f"{bulan:02d}", str(tahun)))
    
    # LOG KEGIATAN
    # ─────────────────────────────────────────────

    def tambah_log(self, log: LogKegiatan) -> bool:
        """Menyimpan satu log kegiatan baru."""
        sql = """
            INSERT INTO log_kegiatan (aktivitas, kategori, durasi_menit, tanggal, waktu, catatan, selesai)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        result = db.execute_query(sql, (
            log.aktivitas,
            log.kategori,
            log.durasi_menit,
            str(log.tanggal),
            log.waktu,
            log.catatan,
            int(log.selesai)
        ))
        return result is not None

    def hapus_log(self, id_log: int) -> bool:
        """Menghapus satu log kegiatan berdasarkan ID."""
        result = db.execute_query("DELETE FROM log_kegiatan WHERE id = ?", (id_log,))
        return result is not None

    def toggle_selesai(self, id_log: int) -> bool:
        """Toggle status selesai pada log kegiatan."""
        sql = "UPDATE log_kegiatan SET selesai = NOT selesai WHERE id = ?"
        result = db.execute_query(sql, (id_log,))
        return result is not None

    def get_dataframe_log(self, tanggal: datetime.date = None) -> pd.DataFrame | None:
        """Mengambil log kegiatan sebagai DataFrame."""
        if tanggal:
            sql = "SELECT * FROM log_kegiatan WHERE tanggal = ? ORDER BY waktu ASC, id DESC"
            return db.fetch_as_dataframe(sql, (str(tanggal),))
        sql = "SELECT * FROM log_kegiatan ORDER BY tanggal DESC, id DESC"
        return db.fetch_as_dataframe(sql)

    # TARGET TABUNGAN
    # ─────────────────────────────────────────────
    def tambah_target(self, target: TargetTabungan) -> bool:
        """Menyimpan target tabungan baru."""
        sql = """
            INSERT INTO target_tabungan (nama_target, jumlah_target, terkumpul, deadline, deskripsi, aktif)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        result = db.execute_query(sql, (
            target.nama_target,
            target.jumlah_target,
            target.terkumpul,
            str(target.deadline) if target.deadline else None,
            target.deskripsi,
            int(target.aktif)
        ))
        return result is not None

    def update_terkumpul(self, id_target: int, tambahan: float) -> bool:
        """Menambah jumlah terkumpul pada target tabungan."""
        sql = "UPDATE target_tabungan SET terkumpul = terkumpul + ? WHERE id = ?"
        result = db.execute_query(sql, (tambahan, id_target))
        return result is not None

    def hapus_target(self, id_target: int) -> bool:
        """Menghapus target tabungan berdasarkan ID."""
        result = db.execute_query("DELETE FROM target_tabungan WHERE id = ?", (id_target,))
        return result is not None

    def get_dataframe_target(self) -> pd.DataFrame | None:
        """Mengambil semua target tabungan aktif."""
        sql = "SELECT * FROM target_tabungan WHERE aktif = 1 ORDER BY id DESC"
        return db.fetch_as_dataframe(sql)
    
    # ── TAGIHAN ──────────────────────────────────────
    def tambah_tagihan(self, tagihan) -> bool:
        """Menyimpan tagihan bulanan baru ke database."""
        sql = """
            INSERT INTO tagihan (nama, kategori, jumlah, tanggal_jatuh_tempo, sudah_bayar, catatan)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        result = db.execute_query(sql, (
            tagihan.nama,
            tagihan.kategori,
            tagihan.jumlah,
            str(tagihan.tanggal_jatuh_tempo),
            int(tagihan.sudah_bayar),
            tagihan.catatan
        ))
        return result is not None

    def get_dataframe_tagihan(self):
        """Mengambil semua tagihan sebagai DataFrame."""
        sql = "SELECT * FROM tagihan ORDER BY tanggal_jatuh_tempo ASC"
        return db.fetch_as_dataframe(sql)

    def toggle_bayar_tagihan(self, id_tagihan: int) -> bool:
        """Toggle status bayar pada tagihan."""
        sql = "UPDATE tagihan SET sudah_bayar = CASE WHEN sudah_bayar=1 THEN 0 ELSE 1 END WHERE id = ?"
        result = db.execute_query(sql, (id_tagihan,))
        return result is not None

    def hapus_tagihan(self, id_tagihan: int) -> bool:
        """Menghapus tagihan berdasarkan ID."""
        result = db.execute_query("DELETE FROM tagihan WHERE id = ?", (id_tagihan,))
        return result is not None

    # ── BELANJA ──────────────────────────────────────
    def tambah_item_belanja(self, item) -> bool:
        """Menyimpan item belanja baru ke database."""
        sql = """
            INSERT INTO belanja (nama, jumlah, sudah_beli, catatan)
            VALUES (?, ?, ?, ?)
        """
        result = db.execute_query(sql, (
            item.nama,
            item.jumlah,
            int(item.sudah_beli),
            item.catatan
        ))
        return result is not None

    def get_dataframe_belanja(self):
        """Mengambil semua item belanja sebagai DataFrame."""
        sql = "SELECT * FROM belanja ORDER BY id ASC"
        return db.fetch_as_dataframe(sql)

    def toggle_beli(self, id_item: int) -> bool:
        """Toggle status beli pada item belanja."""
        sql = "UPDATE belanja SET sudah_beli = CASE WHEN sudah_beli=1 THEN 0 ELSE 1 END WHERE id = ?"
        result = db.execute_query(sql, (id_item,))
        return result is not None

    def hapus_item_belanja(self, id_item: int) -> bool:
        """Menghapus item belanja berdasarkan ID."""
        result = db.execute_query("DELETE FROM belanja WHERE id = ?", (id_item,))
        return result is not None