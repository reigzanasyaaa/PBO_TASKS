
class Jadwal:
  def __init__(self, mata_kuliah, hari, jam, ruang):
    self.mata_kuliah = mata_kuliah
    self.hari = hari
    self.jam = jam
    self.ruang = ruang

  def tampilkan_info(self):
    print(f"Mata Kuliah: {self.mata_kuliah}")
    print(f"Hari: {self.hari}")
    print(f"Jam: {self.jam}")
    print(f"Ruang: {self.ruang}")

  def ubah_ruang(self, ruang_baru):
    self.ruang = ruang_baru
    print(f"Ruang kelas untuk {self.mata_kuliah} diperbarui menjadi: {self.ruang}")
