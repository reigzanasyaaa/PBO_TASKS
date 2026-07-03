import datetime
class Transaksi:
    """
    Blueprint untuk satu catatan transaksi keuangan (pemasukan/pengeluaran).
    Menerapkan prinsip Enkapsulasi OOP.
    """
    def __init__(
        self,
        tipe: str,
        deskripsi: str,
        jumlah: float,
        kategori: str,
        tanggal: datetime.date,
        catatan: str = "",
        id: int = None
    ):
        self._id = id
        self._tipe = tipe
        self._deskripsi = deskripsi
        self._jumlah = jumlah
        self._kategori = kategori
        self._tanggal = tanggal
        self._catatan = catatan

    @property
    def id(self): return self._id
    @property
    def tipe(self): return self._tipe
    @property
    def deskripsi(self): return self._deskripsi
    @property
    def jumlah(self): return self._jumlah
    @property
    def kategori(self): return self._kategori
    @property
    def tanggal(self): return self._tanggal
    @property
    def catatan(self): return self._catatan

    def to_dict(self):
        return {
            "id": self._id,
            "tipe": self._tipe,
            "deskripsi": self._deskripsi,
            "jumlah": self._jumlah,
            "kategori": self._kategori,
            "tanggal": str(self._tanggal),
            "catatan": self._catatan
        }

    def __repr__(self):
        return (f"Transaksi(id={self._id}, tipe={self._tipe}, "
                f"deskripsi='{self._deskripsi}', jumlah={self._jumlah})")

class LogKegiatan:
    """
    Blueprint untuk satu entri log kegiatan harian penghuni kos.
    """
    def __init__(
        self,
        aktivitas: str,
        kategori: str,
        durasi_menit: int,
        tanggal: datetime.date,
        waktu: str = "",
        catatan: str = "",
        selesai: bool = False,
        id: int = None
    ):
        self._id = id
        self._aktivitas = aktivitas
        self._kategori = kategori
        self._durasi_menit = durasi_menit
        self._tanggal = tanggal
        self._waktu = waktu
        self._catatan = catatan
        self._selesai = selesai

    @property
    def id(self): return self._id
    @property
    def aktivitas(self): return self._aktivitas
    @property
    def kategori(self): return self._kategori
    @property
    def durasi_menit(self): return self._durasi_menit
    @property
    def tanggal(self): return self._tanggal
    @property
    def waktu(self): return self._waktu
    @property
    def catatan(self): return self._catatan
    @property
    def selesai(self): return bool(self._selesai)

    def __repr__(self):
        return (f"LogKegiatan(id={self._id}, aktivitas='{self._aktivitas}', "
                f"tanggal={self._tanggal})")

class TargetTabungan:
    """
    Blueprint untuk satu target tabungan/saving goal.
    """
    def __init__(
        self,
        nama_target: str,
        jumlah_target: float,
        terkumpul: float = 0,
        deadline: datetime.date = None,
        deskripsi: str = "",
        aktif: bool = True,
        id: int = None
    ):
        self._id = id
        self._nama_target = nama_target
        self._jumlah_target = jumlah_target
        self._terkumpul = terkumpul
        self._deadline = deadline
        self._deskripsi = deskripsi
        self._aktif = aktif

    @property
    def id(self): return self._id
    @property
    def nama_target(self): return self._nama_target
    @property
    def jumlah_target(self): return self._jumlah_target
    @property
    def terkumpul(self): return self._terkumpul
    @property
    def deadline(self): return self._deadline
    @property
    def deskripsi(self): return self._deskripsi
    @property
    def aktif(self): return bool(self._aktif)

    @property
    def persentase(self) -> float:
        if self._jumlah_target <= 0:
            return 0.0
        return min((self._terkumpul / self._jumlah_target) * 100, 100)

    def __repr__(self):
        return (f"TargetTabungan(id={self._id}, nama='{self._nama_target}', "
                f"progress={self.persentase:.1f}%)")

class Tagihan:
    """
    Blueprint untuk satu tagihan bulanan penghuni kos
    (sewa, listrik, air, wifi, dll).
    """
    def __init__(
        self,
        nama: str,
        kategori: str,
        jumlah: float,
        tanggal_jatuh_tempo: datetime.date,
        sudah_bayar: bool = False,
        catatan: str = "",
        id: int = None
    ):
        self._id = id
        self._nama = nama
        self._kategori = kategori
        self._jumlah = jumlah
        self._tanggal_jatuh_tempo = tanggal_jatuh_tempo
        self._sudah_bayar = sudah_bayar
        self._catatan = catatan

    @property
    def id(self): return self._id
    @property
    def nama(self): return self._nama
    @property
    def kategori(self): return self._kategori
    @property
    def jumlah(self): return self._jumlah
    @property
    def tanggal_jatuh_tempo(self): return self._tanggal_jatuh_tempo
    @property
    def sudah_bayar(self): return bool(self._sudah_bayar)
    @property
    def catatan(self): return self._catatan

    def to_dict(self):
        return {
            "id": self._id,
            "nama": self._nama,
            "kategori": self._kategori,
            "jumlah": self._jumlah,
            "tanggal_jatuh_tempo": str(self._tanggal_jatuh_tempo),
            "sudah_bayar": self._sudah_bayar,
            "catatan": self._catatan
        }

    def __repr__(self):
        return (f"Tagihan(id={self._id}, nama='{self._nama}', "
                f"jumlah={self._jumlah}, lunas={self._sudah_bayar})")

class ItemBelanja:
    """
    Blueprint untuk satu item dalam checklist belanja kebutuhan kos.
    """
    def __init__(
        self,
        nama: str,
        jumlah: str = "1",
        sudah_beli: bool = False,
        catatan: str = "",
        id: int = None
    ):
        self._id = id
        self._nama = nama
        self._jumlah = jumlah
        self._sudah_beli = sudah_beli
        self._catatan = catatan

    @property
    def id(self): return self._id
    @property
    def nama(self): return self._nama
    @property
    def jumlah(self): return self._jumlah
    @property
    def sudah_beli(self): return bool(self._sudah_beli)
    @property
    def catatan(self): return self._catatan

    def to_dict(self):
        return {
            "id": self._id,
            "nama": self._nama,
            "jumlah": self._jumlah,
            "sudah_beli": self._sudah_beli,
            "catatan": self._catatan
        }

    def __repr__(self):
        return (f"ItemBelanja(id={self._id}, nama='{self._nama}', "
                f"jumlah='{self._jumlah}', sudah_beli={self._sudah_beli})")