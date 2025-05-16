from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class JoinDetector(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(jenis_join='NOJOIN')

    #================================Masukkan tambahan rule dibawah ini: ==================================
    # ======================= RULE UNTUK DB HOTEL 1 ===========================

    # RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="reservasi"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="reservasi"),
        SEBELUM(kata="sudah", tabel="tamu")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="reservasi"),
        Fact(tabel="kamar"),
        Fact(kata="daftar"),
        Fact(kata="lengkap"),
        SEBELUM(kata="lengkap", tabel="reservasi"),
        SEBELUM(kata="lengkap", tabel="tamu"),
        SEBELUM(kata="lengkap", tabel="kamar")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="reservasi"),
        Fact(tabel="kamar"),
        Fact(kata="semua"),
        Fact(kata="sudah"),
        Fact(kata="dibayar"),
        SEBELUM(kata="dibayar", tabel="reservasi"),
        SEBELUM(kata="dibayar", tabel="tamu"),
        SEBELUM(kata="dibayar", tabel="kamar")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="reservasi"),
        Fact(tabel="kamar"),
        Fact(kata="daftar"),
        Fact(kata="sedang"),
        Fact(kata="ditempati"),
        SEBELUM(kata="ditempati", tabel="reservasi"),
        SEBELUM(kata="ditempati", tabel="tamu"),
        SEBELUM(kata="ditempati", tabel="kamar")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="reservasi"),
        Fact(kata="lengkap"),
        SEBELUM(kata="lengkap", tabel="reservasi"),
        SEBELUM(kata="lengkap", tabel="pembayaran")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="reservasi"),
        Fact(tabel="pembayaran"),
        Fact(kata="sudah"),
        Fact(kata="check-in"),
        Fact(kata="bayar"),
        SEBELUM(kata="check-in", tabel="reservasi"),
        SEBELUM(kata="check-in", tabel="tamu"),
        SEBELUM(kata="bayar", tabel="pembayaran")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="reservasi"),
        Fact(tabel="kamar"),
        Fact(kata="pernah"),
        Fact(kata="dipesan"),
        SEBELUM(kata="dipesan", tabel="reservasi"),
        SEBELUM(kata="dipesan", tabel="tamu"),
        SEBELUM(kata="dipesan", tabel="kamar")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="reservasi"),
        Fact(tabel="pembayaran"),
        Fact(tabel="kamar"),
        Fact(kata="memiliki"),
        Fact(kata="lengkap"),
        SEBELUM(kata="lengkap", tabel="reservasi"),
        SEBELUM(kata="lengkap", tabel="pembayaran"),
        SEBELUM(kata="lengkap", tabel="kamar")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"),
        Fact(tabel="pembayaran"),
        Fact(kata="daftar"),
        Fact(kata="beserta"),
        Fact(kata="lakukan"),
        SEBELUM(kata="lakukan", tabel="pembayaran"),
        SEBELUM(kata="lakukan", tabel="tamu")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="reservasi"),
        Fact(tabel="tamu"),
        Fact(tabel="kamar"),
        Fact(tabel="pembayaran"),
        Fact(kata="lengkap"),
        SEBELUM(kata="lengkap", tabel="reservasi"),
        SEBELUM(kata="lengkap", tabel="tamu"),
        SEBELUM(kata="lengkap", tabel="kamar"),
        SEBELUM(kata="lengkap", tabel="pembayaran")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
        AND(
            Fact(tabel="tamu"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="tamu"), 
            Fact(kata="belum"), 
            SEBELUM(kata="belum", tabel="reservasi")
        )
    )
    def r1(self):
            self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
        AND(
            Fact(tabel="kamar"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="kamar"), 
            Fact(kata="jika"), 
            Fact(kata="ada"), 
            SETELAH(kata="jika", tabel="reservasi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
        AND(
            Fact(tabel="reservasi"), 
            Fact(tabel="pembayaran"), 
            Fact(kata="seluruh"), 
            SEBELUM(kata="seluruh", tabel="reservasi"), 
            Fact(kata="belum"), 
            Fact(kata="pembayarannya"), 
            SETELAH(kata="belum", tabel="pembayaran")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
        AND(
            Fact(tabel="tamu"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="tamu"), 
            Fact(kata="jika"), 
            Fact(kata="tersedia"), 
            SETELAH(kata="jika", tabel="reservasi")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"), 
        Fact(tabel="tamu"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kamar"), 
        Fact(kata="jika"), 
        Fact(kata="ada"), 
        SETELAH(kata="jika", tabel="tamu")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"), 
        Fact(tabel="kamar"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="tamu"), 
        Fact(kata="belum"), 
        Fact(kata="memesan"), 
        SETELAH(kata="belum", tabel="kamar")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="reservasi"), 
        Fact(tabel="pembayaran"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="reservasi"), 
        Fact(kata="belum"), 
        Fact(kata="dibayar"), 
        SETELAH(kata="belum", tabel="pembayaran")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"), 
        Fact(tabel="tamu"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kamar"), 
        Fact(kata="jika"), 
        Fact(kata="ada"), 
        SETELAH(kata="jika", tabel="tamu")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="tamu"), 
        Fact(tabel="checkin"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="tamu"), 
        Fact(kata="belum"), 
        Fact(kata="check-in"), 
        SETELAH(kata="belum", tabel="checkin")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="reservasi"), 
        Fact(tabel="pembayaran"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="reservasi"), 
        Fact(kata="belum"), 
        Fact(kata="pembayaran"), 
        SETELAH(kata="belum", tabel="pembayaran")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
        AND(
            Fact(tabel="pembayaran"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="pembayaran"), 
            Fact(kata="belum"), 
            SEBELUM(kata="belum", tabel="reservasi")
        )
    )
    def r1(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="reservasi"), 
            Fact(tabel="pembayaran"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="reservasi"), 
            Fact(kata="memiliki"), 
            SEBELUM(kata="memiliki", tabel="pembayaran")
        )
    )
    def r2(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="kamar"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="kamar"), 
            Fact(kata="dipesan"), 
            SEBELUM(kata="dipesan", tabel="reservasi")
        )
    )
    def r3(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="reservasi"), 
            Fact(tabel="pembayaran"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="reservasi"), 
            Fact(kata="dibayar"), 
            SEBELUM(kata="dibayar", tabel="pembayaran")
        )
    )
    def r4(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="pembayaran"), 
            Fact(tabel="tamu"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="pembayaran"), 
            Fact(kata="tidak"), 
            SEBELUM(kata="tidak", tabel="tamu")
        )
    )
    def r5(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="reservasi"), 
            Fact(tabel="pembayaran"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="reservasi"), 
            Fact(kata="ditampilkan"), 
            SEBELUM(kata="ditampilkan", tabel="pembayaran")
        )
    )
    def r6(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="kamar"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="kamar"), 
            Fact(kata="dipesan"), 
            SEBELUM(kata="dipesan", tabel="reservasi")
        )
    )
    def r7(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="pembayaran"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="pembayaran"), 
            Fact(kata="ada"), 
            SEBELUM(kata="ada", tabel="reservasi")
        )
    )
    def r8(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="pembayaran"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="pembayaran"), 
            Fact(kata="terkait"), 
            SEBELUM(kata="terkait", tabel="reservasi"), 
            Fact(kata="tidak"), 
            SEBELUM(kata="tidak", tabel="kamar")
        )
    )
    def r9(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
        AND(
            Fact(tabel="pembayaran"), 
            Fact(tabel="reservasi"), 
            Fact(kata="semua"), 
            SEBELUM(kata="semua", tabel="pembayaran"), 
            Fact(kata="terkait"), 
            SEBELUM(kata="terkait", tabel="reservasi"), 
            Fact(kata="tidak"), 
            SEBELUM(kata="tidak", tabel="reservasi")
        )
    )
    def r10(self):
            self.declare(Fact(tipe_join='RIGHTJOIN'))


# ======================= RULE UNTUK DB HOTEL 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pemesanan"),
        Fact(kata="telah"),
        SEBELUM(kata="telah", tabel="pemesanan"),
        SEBELUM(kata="telah", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="pemesanan"),
        Fact(kata="dipesan"),
        SEBELUM(kata="dipesan", tabel="pemesanan"),
        SEBELUM(kata="dipesan", tabel="kamar")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="tipe_kamar"),
        Fact(kata="tipe"),
        SEBELUM(kata="tipe", tabel="tipe_kamar"),
        SEBELUM(kata="tipe", tabel="kamar")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="fasilitas"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="fasilitas"),
        SEBELUM(kata="memiliki", tabel="kamar")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="layanan"),
        Fact(kata="menggunakan"),
        SEBELUM(kata="menggunakan", tabel="layanan"),
        SEBELUM(kata="menggunakan", tabel="pemesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="jabatan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="jabatan"),
        SEBELUM(kata="memiliki", tabel="pegawai")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="dibayar"),
        SEBELUM(kata="dibayar", tabel="pembayaran"),
        SEBELUM(kata="dibayar", tabel="pemesanan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="layanan"),
        Fact(kata="digunakan"),
        SEBELUM(kata="digunakan", tabel="layanan"),
        SEBELUM(kata="digunakan", tabel="pemesanan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="tipe_kamar"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="tipe_kamar"),
        SEBELUM(kata="memiliki", tabel="kamar")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pemesanan"),
        Fact(kata="melakukan"),
        SEBELUM(kata="melakukan", tabel="pemesanan"),
        SEBELUM(kata="melakukan", tabel="pelanggan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

#RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"), 
        Fact(tabel="pemesanan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="pelanggan"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pemesanan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"), 
        Fact(tabel="pemesanan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kamar"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pemesanan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="tipe_kamar"), 
        Fact(tabel="kamar"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="tipe_kamar"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="kamar")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="fasilitas"), 
        Fact(tabel="kamar"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="fasilitas"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="kamar")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="layanan"), 
        Fact(tabel="pemesanan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="layanan"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pemesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="pegawai"), 
        Fact(tabel="jabatan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="pegawai"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="jabatan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="jabatan"), 
        Fact(tabel="pegawai"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="jabatan"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pegawai")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="pemesanan"), 
        Fact(tabel="pembayaran"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="pemesanan"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pembayaran")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="pelanggan"), 
        Fact(tabel="pemesanan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="pelanggan"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pemesanan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule( 
    AND(
        Fact(tabel="kamar"), 
        Fact(tabel="tipe_kamar"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kamar"), 
        OR(
            Fact(kata="jika"),
            Fact(kata="yang")
        ),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="tipe_kamar")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pemesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="pelanggan"),
        SEBELUM(kata="pelanggan", tabel="pemesanan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="kamar"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemesanan"),
        Fact(kata="kamar"),
        SEBELUM(kata="kamar", tabel="pemesanan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="tipe_kamar"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kamar"),
        Fact(kata="tipe kamar"),
        SEBELUM(kata="tipe kamar", tabel="kamar")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="fasilitas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kamar"),
        Fact(kata="fasilitas"),
        SEBELUM(kata="fasilitas", tabel="kamar")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="layanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemesanan"),
        Fact(kata="layanan"),
        SEBELUM(kata="layanan", tabel="pemesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="jabatan"),
        SEBELUM(kata="jabatan", tabel="pegawai")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="jabatan"),
        SEBELUM(kata="jabatan", tabel="pegawai")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemesanan"),
        Fact(kata="pembayaran"),
        SEBELUM(kata="pembayaran", tabel="pemesanan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemesanan"),
        Fact(kata="pelanggan"),
        SEBELUM(kata="pelanggan", tabel="pemesanan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kamar"),
        Fact(tabel="tipe_kamar"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kamar"),
        Fact(kata="tipe kamar"),
        SEBELUM(kata="tipe kamar", tabel="kamar")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))


# ======================= RULE UNTUK DB INVENTORI 1 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="memiliki pemasok"),
        SEBELUM(kata="memiliki pemasok", tabel="pemasok"),
        SEBELUM(kata="memiliki pemasok", tabel="barang")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="transaksi"),
        Fact(kata="pernah melakukan transaksi"),
        SEBELUM(kata="pernah melakukan transaksi", tabel="transaksi"),
        SEBELUM(kata="pernah melakukan transaksi", tabel="pelanggan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="punya detail pembelian"),
        SEBELUM(kata="punya detail pembelian", tabel="detail_transaksi"),
        SEBELUM(kata="punya detail pembelian", tabel="transaksi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="transaksi"),
        Fact(kata="pernah dijual ke pelanggan"),
        SEBELUM(kata="pernah dijual ke pelanggan", tabel="detail_transaksi"),
        SEBELUM(kata="pernah dijual ke pelanggan", tabel="transaksi"),
        SEBELUM(kata="pernah dijual ke pelanggan", tabel="barang")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemasok"),
        Fact(tabel="barang"),
        Fact(kata="memasok minimal satu barang"),
        SEBELUM(kata="memasok minimal satu barang", tabel="barang"),
        SEBELUM(kata="memasok minimal satu barang", tabel="pemasok")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pelanggan"),
        Fact(kata="terkait dengan pelanggan aktif"),
        SEBELUM(kata="terkait dengan pelanggan aktif", tabel="pelanggan"),
        SEBELUM(kata="terkait dengan pelanggan aktif", tabel="transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="barang"),
        Fact(kata="memiliki satu atau lebih barang"),
        SEBELUM(kata="memiliki satu atau lebih barang", tabel="detail_transaksi"),
        SEBELUM(kata="memiliki satu atau lebih barang", tabel="barang"),
        SEBELUM(kata="memiliki satu atau lebih barang", tabel="transaksi")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="barang"),
        Fact(kata="pernah membeli barang tertentu"),
        SEBELUM(kata="pernah membeli barang tertentu", tabel="detail_transaksi"),
        SEBELUM(kata="pernah membeli barang tertentu", tabel="barang"),
        SEBELUM(kata="pernah membeli barang tertentu", tabel="transaksi")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="transaksi"),
        Fact(kata="pernah masuk ke dalam rincian transaksi"),
        SEBELUM(kata="pernah masuk ke dalam rincian transaksi", tabel="detail_transaksi"),
        SEBELUM(kata="pernah masuk ke dalam rincian transaksi", tabel="barang"),
        SEBELUM(kata="pernah masuk ke dalam rincian transaksi", tabel="transaksi")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="menangani transaksi tertentu"),
        SEBELUM(kata="menangani transaksi tertentu", tabel="pengguna"),
        SEBELUM(kata="menangani transaksi tertentu", tabel="transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="barang"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="pemasok")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="jika pernah"),
        SEBELUM(kata="jika pernah", tabel="transaksi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="peran"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pengguna"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="peran")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="barang"),
        Fact(kata="kalau tersedia"),
        SEBELUM(kata="kalau tersedia", tabel="pemasok")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        Fact(kata="belum ada"),
        SEBELUM(kata="belum ada", tabel="detail_transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="seluruh"),
        SEBELUM(kata="seluruh", tabel="barang"),
        Fact(kata="jika tersedia"),
        SEBELUM(kata="jika tersedia", tabel="pemasok")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="transaksi"),
        Fact(kata="terdaftar"),
        SEBELUM(kata="terdaftar", tabel="pelanggan"),
        Fact(kata="belum pernah"),
        SEBELUM(kata="belum pernah", tabel="transaksi")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        Fact(kata="tanpa"),
        SEBELUM(kata="tanpa", tabel="detail_transaksi")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="barang"),
        Fact(kata="belum pernah"),
        SEBELUM(kata="belum pernah", tabel="detail_transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemasok"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="barang")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        Fact(kata="tidak lengkap"),
        SEBELUM(kata="tidak lengkap", tabel="transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="tidak lengkap"),
        SEBELUM(kata="tidak lengkap", tabel="pelanggan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="barang"),
        Fact(kata="tidak ditemukan"),
        SEBELUM(kata="tidak ditemukan", tabel="barang")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        Fact(kata="hilang"),
        SEBELUM(kata="hilang", tabel="transaksi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemasok"),
        Fact(kata="tidak memiliki"),
        SEBELUM(kata="tidak memiliki", tabel="barang")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="hilang"),
        SEBELUM(kata="hilang", tabel="pelanggan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        Fact(kata="dihapus"),
        SEBELUM(kata="dihapus", tabel="barang")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemasok"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="barang")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="barang"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        Fact(kata="tidak tersedia"),
        SEBELUM(kata="tidak tersedia", tabel="barang")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULE UNTUK DB INVENTORI 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="kategori")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="stok"),
        Fact(kata="tersedia"),
        SEBELUM(kata="tersedia", tabel="produk"),
        SEBELUM(kata="tersedia", tabel="stok")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemasok"),
        Fact(tabel="transaksi"),
        Fact(kata="telah"),
        SEBELUM(kata="telah", tabel="pemasok"),
        SEBELUM(kata="telah", tabel="transaksi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="transaksi"),
        Fact(kata="tercatat"),
        SEBELUM(kata="tercatat", tabel="produk"),
        SEBELUM(kata="tercatat", tabel="transaksi")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="stok"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="stok")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kategori"),
        Fact(tabel="produk"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="kategori"),
        SEBELUM(kata="memiliki", tabel="produk")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemasok"),
        Fact(tabel="transaksi"),
        Fact(kata="melakukan"),
        SEBELUM(kata="melakukan", tabel="pemasok"),
        SEBELUM(kata="melakukan", tabel="transaksi")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="kategori")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="stok"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="stok")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="transaksi"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="kategori"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="kategori")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="stok"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="stok")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemasok"), 
        Fact(tabel="transaksi"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="pemasok"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="transaksi"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="stok"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="stok")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kategori"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kategori"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemasok"), 
        Fact(tabel="transaksi"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="pemasok"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="kategori"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="kategori")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="stok"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="stok")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kategori"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kategori"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="kategori"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="kategori"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="transaksi"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"), 
        Fact(tabel="pemasok"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="transaksi"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="pemasok")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="stok"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="stok"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"), 
        Fact(tabel="pemasok"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="transaksi"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="pemasok")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"), 
        Fact(tabel="transaksi"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="produk"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="stok"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="stok"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"), 
        Fact(tabel="pemasok"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="transaksi"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="pemasok")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="stok"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="stok"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"), 
        Fact(tabel="produk"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="transaksi"), 
        Fact(kata="belum"), 
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))


# ======================= RULES UNTUK DB AKADEMIK 1 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="kelas"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="kelas"),
        SEBELUM(kata="sudah", tabel="mahasiswa")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="nilai"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="nilai"),
        SEBELUM(kata="nilai", tabel="nilai"),
        SEBELUM(kata="nilai", tabel="mahasiswa"),
        SEBELUM(kata="nilai", tabel="mata_kuliah")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="mengajar"),
        SEBELUM(kata="mengajar", tabel="kelas"),
        SEBELUM(kata="mengajar", tabel="dosen"),
        SEBELUM(kata="mengajar", tabel="mata_kuliah")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(tabel="kelas"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="krs"),
        SEBELUM(kata="memiliki", tabel="mahasiswa"),
        SEBELUM(kata="memiliki", tabel="kelas")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="nilai"),
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(kata="dikaitkan"),
        SEBELUM(kata="dikaitkan", tabel="nilai"),
        SEBELUM(kata="dikaitkan", tabel="krs"),
        SEBELUM(kata="dikaitkan", tabel="mahasiswa")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="kelas"),
        SEBELUM(kata="memiliki", tabel="dosen"),
        SEBELUM(kata="memiliki", tabel="mata_kuliah")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="diajarkan"),
        Fact(kata="tahun ajaran"),
        SEBELUM(kata="diajarkan", tabel="kelas"),
        SEBELUM(kata="diajarkan", tabel="dosen"),
        SEBELUM(kata="diajarkan", tabel="mata_kuliah"),
        SEBELUM(kata="tahun ajaran", tabel="kelas")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(tabel="nilai"),
        Fact(kata="menerima"),
        SEBELUM(kata="menerima", tabel="krs"),
        SEBELUM(kata="menerima", tabel="mahasiswa"),
        SEBELUM(kata="menerima", tabel="nilai")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="nilai"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="krs"),
        SEBELUM(kata="memiliki", tabel="nilai")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="kelas"),
        Fact(tabel="nilai"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="krs"),
        SEBELUM(kata="memiliki", tabel="kelas"),
        SEBELUM(kata="memiliki", tabel="nilai")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mahasiswa"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="kelas")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mata_kuliah"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="dosen")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="nilai"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="nilai")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mahasiswa"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="krs")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="dosen"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="mata_kuliah")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="mahasiswa")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="nilai"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="nilai")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(tabel="nilai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mahasiswa"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="nilai")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mata_kuliah"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="kelas")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="dosen"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="kelas")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="nilai"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="nilai"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="mahasiswa")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="nilai"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="nilai"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="krs")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="krs")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mata_kuliah"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="dosen")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="mahasiswa")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="nilai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="nilai")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="nilai"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="nilai"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="mahasiswa")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="dosen")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="mahasiswa")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="nilai"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="nilai"),
        Fact(kata="jika ada"),
        SEBELUM(kata="jika ada", tabel="krs")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULES UNTUK DB AKADEMIK 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="krs"),
        SEBELUM(kata="memiliki", tabel="mahasiswa")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="kelas"),
        SEBELUM(kata="memiliki", tabel="mata_kuliah")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(kata="mengajar"),
        SEBELUM(kata="mengajar", tabel="kelas"),
        SEBELUM(kata="mengajar", tabel="dosen")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="mata_kuliah"),
        SEBELUM(kata="memiliki", tabel="kelas")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="krs"),
        SEBELUM(kata="memiliki", tabel="mahasiswa")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="kelas"),
        SEBELUM(kata="memiliki", tabel="mata_kuliah")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(kata="mengajar"),
        SEBELUM(kata="mengajar", tabel="kelas"),
        SEBELUM(kata="mengajar", tabel="dosen")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="dosen"),
        SEBELUM(kata="memiliki", tabel="kelas")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="krs"),
        SEBELUM(kata="memiliki", tabel="mahasiswa")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="mengambil"),
        SEBELUM(kata="mengambil", tabel="krs"),
        SEBELUM(kata="mengambil", tabel="mahasiswa"),
        SEBELUM(kata="mengambil", tabel="mata_kuliah")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))


# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mahasiswa"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="krs")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mata_kuliah"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="dosen"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="mata_kuliah")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mahasiswa"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="krs")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mata_kuliah"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="dosen"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="dosen")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mahasiswa"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mahasiswa"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="krs")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="mata_kuliah"),
        Fact(tabel="krs"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="mata_kuliah"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="krs")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="mahasiswa")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="mata_kuliah")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="dosen")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="mahasiswa")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="mata_kuliah"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="mata_kuliah")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="kelas"),
        Fact(tabel="dosen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kelas"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="dosen")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="dosen"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="dosen"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="mahasiswa"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="mahasiswa")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="krs"),
        Fact(tabel="kelas"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="krs"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kelas")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULES UNTUK DB KEPAGAWAAN 1 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="jabatan"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="pegawai"),
        SEBELUM(kata="sudah", tabel="jabatan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="departemen"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="pegawai"),
        SEBELUM(kata="sudah", tabel="departemen")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="pelatihan"),
        Fact(kata="pernah"),
        SEBELUM(kata="pernah", tabel="pegawai"),
        SEBELUM(kata="pernah", tabel="pelatihan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="riwayat_pendidikan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pegawai"),
        SEBELUM(kata="memiliki", tabel="riwayat_pendidikan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="absensi"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pegawai"),
        SEBELUM(kata="memiliki", tabel="absensi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="gaji"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="pegawai"),
        SEBELUM(kata="sudah", tabel="gaji")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="cuti"),
        Fact(kata="pernah"),
        SEBELUM(kata="pernah", tabel="pegawai"),
        SEBELUM(kata="pernah", tabel="cuti")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="promosi_jabatan"),
        Fact(kata="pernah"),
        SEBELUM(kata="pernah", tabel="pegawai"),
        SEBELUM(kata="pernah", tabel="promosi_jabatan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="pelatihan"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="pegawai"),
        SEBELUM(kata="sudah", tabel="pelatihan"),
        FIELD(tabel="pelatihan", nama="sertifikat", nilai="true")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="absensi"),
        Fact(tabel="gaji"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="pegawai"),
        SEBELUM(kata="sudah", tabel="absensi"),
        SEBELUM(kata="sudah", tabel="gaji"),
        FIELD(tabel="gaji", nama="bulan", nilai="5")
        )
    )
    def r_10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="jabatan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="departemen"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="departemen")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="pelatihan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pelatihan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="gaji"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="gaji")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="cuti"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="cuti")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="riwayat_pendidikan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="riwayat_pendidikan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="absensi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="absensi")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelatihan"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelatihan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="promosi_jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="pernah"),
        SEBELUM(kata="pernah", tabel="promosi_jabatan")
        )
    )
    def r_9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="departemen"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="departemen"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="pegawai"),
        Fact(tabel="jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pegawai"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="jabatan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="departemen"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="departemen"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelatihan"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelatihan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="promosi_jabatan"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="promosi_jabatan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="cuti"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="cuti"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="departemen"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="departemen"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="riwayat_pendidikan"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="riwayat_pendidikan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="absensi"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="absensi"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran_gaji"),
        Fact(tabel="pegawai"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran_gaji"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pegawai")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="promosi_jabatan"),
        Fact(tabel="jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="promosi_jabatan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="jabatan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULES UNTUK DB KEPAGAWAAN 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="departemen"),
        Fact(kata="nama"),
        SEBELUM(kata="nama", tabel="departemen"),
        SEBELUM(kata="nama", tabel="karyawan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="jabatan"),
        Fact(kata="jabatan"),
        SEBELUM(kata="jabatan", tabel="jabatan"),
        SEBELUM(kata="jabatan", tabel="karyawan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="cuti"),
        Fact(kata="pengajuan"),
        SEBELUM(kata="pengajuan", tabel="cuti"),
        SEBELUM(kata="pengajuan", tabel="karyawan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="absensi"),
        Fact(kata="absensi"),
        SEBELUM(kata="absensi", tabel="absensi"),
        SEBELUM(kata="absensi", tabel="karyawan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="absensi"),
        Fact(kata="absensi"),
        SEBELUM(kata="absensi", tabel="absensi"),
        SEBELUM(kata="absensi", tabel="karyawan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="cuti"),
        Fact(kata="pengajuan"),
        SEBELUM(kata="pengajuan", tabel="cuti"),
        SEBELUM(kata="pengajuan", tabel="karyawan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="jabatan"),
        Fact(tabel="departemen"),
        Fact(kata="jabatan"),
        Fact(kata="departemen"),
        SEBELUM(kata="jabatan", tabel="jabatan"),
        SEBELUM(kata="jabatan", tabel="karyawan"),
        SEBELUM(kata="departemen", tabel="departemen"),
        SEBELUM(kata="departemen", tabel="karyawan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="absensi"),
        Fact(kata="absensi"),
        SEBELUM(kata="absensi", tabel="absensi"),
        SEBELUM(kata="absensi", tabel="karyawan"),
        Fact(kata="hari ini")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="jabatan"),
        Fact(kata="jabatan"),
        SEBELUM(kata="jabatan", tabel="jabatan"),
        SEBELUM(kata="jabatan", tabel="karyawan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="cuti"),
        Fact(kata="cuti"),
        SEBELUM(kata="cuti", tabel="cuti"),
        SEBELUM(kata="cuti", tabel="karyawan"),
        Fact(kata="tanggal")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="cuti"),
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="karyawan"),  
        Fact(kata="cuti"),  
        SEBELUM(kata="cuti", tabel="cuti")  
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="departemen"),
        Fact(tabel="karyawan"),
        Fact(kata="semua"),  
        SEBELUM(kata="semua", tabel="departemen"),  
        Fact(kata="karyawan"),  
        SEBELUM(kata="karyawan", tabel="karyawan")  
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="jabatan"),
        Fact(tabel="karyawan"),
        Fact(kata="semua"),  
        SEBELUM(kata="semua", tabel="jabatan"),  
        Fact(kata="karyawan"),  
        SEBELUM(kata="karyawan", tabel="karyawan") 
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="absensi"),
        Fact(kata="semua"),  
        SEBELUM(kata="semua", tabel="karyawan"),  
        Fact(kata="absensi"),  
        SEBELUM(kata="absensi", tabel="absensi")  
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="cuti"),
        Fact(tabel="karyawan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="cuti"),
        Fact(kata="karyawan"),
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="jabatan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="karyawan"),
        Fact(kata="jabatan"),
        SEBELUM(kata="jabatan", tabel="jabatan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="departemen"),
        Fact(tabel="karyawan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="departemen"),
        Fact(kata="karyawan"),
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="absensi"),
        Fact(tabel="karyawan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="absensi"),
        Fact(kata="karyawan"),
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="jabatan"),
        Fact(tabel="karyawan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="jabatan"),
        Fact(kata="karyawan"),
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="karyawan"),
        Fact(tabel="absensi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="karyawan"),
        Fact(kata="absensi"),
        SEBELUM(kata="absensi", tabel="absensi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='leftjoin'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="cuti"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="cuti"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="absensi"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="absensi"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="jabatan"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="jabatan"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="departemen"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="departemen"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="absensi"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="absensi"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="jabatan"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="jabatan"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="cuti"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="cuti"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="absensi"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="absensi"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="departemen"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="departemen"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="cuti"), 
        Fact(tabel="karyawan"), 
        Fact(kata="semua"), 
        SEBELUM(kata="semua", tabel="cuti"), 
        Fact(kata="karyawan"), 
        SEBELUM(kata="karyawan", tabel="karyawan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULES UNTUK DB AKUNTANSI 1 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="detail_transaksi"),
        SEBELUM(kata="sudah", tabel="transaksi")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="digunakan"),
        SEBELUM(kata="digunakan", tabel="akun"),
        SEBELUM(kata="digunakan", tabel="detail_transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="transaksi"),
        SEBELUM(kata="sudah", tabel="pengguna")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pengguna"),
        Fact(kata="valid"),
        SEBELUM(kata="valid", tabel="pengguna"),
        SEBELUM(kata="valid", tabel="transaksi")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

        @Rule(
        AND(
            Fact(tabel="transaksi"),
            Fact(tabel="detail_transaksi"),
            Fact(kata="memiliki"),
            SEBELUM(kata="memiliki", tabel="detail_transaksi"),
            SEBELUM(kata="memiliki", tabel="transaksi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="terlibat"),
        SEBELUM(kata="terlibat", tabel="detail_transaksi"),
        SEBELUM(kata="terlibat", tabel="akun")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="terkait"),
        Fact(kata="valid"),
        SEBELUM(kata="terkait", tabel="transaksi"),
        SEBELUM(kata="terkait", tabel="pengguna")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="detail_transaksi"),
        SEBELUM(kata="memiliki", tabel="akun"),
        SEBELUM(kata="memiliki", tabel="transaksi")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="pernah"),
        SEBELUM(kata="pernah", tabel="detail_transaksi"),
        SEBELUM(kata="pernah", tabel="transaksi"),
        SEBELUM(kata="pernah", tabel="pengguna")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="detail_transaksi"),
        SEBELUM(kata="memiliki", tabel="akun"),
        SEBELUM(kata="memiliki", tabel="transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pengguna"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        SEBELUM(kata="belum", tabel="akun")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pengguna"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        SEBELUM(kata="belum", tabel="akun")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pengguna"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pengguna"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        SEBELUM(kata="belum", tabel="pengguna")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pengguna"),
        Fact(kata="aktif"),
        SEBELUM(kata="aktif", tabel="pengguna"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="akun"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        SEBELUM(kata="belum", tabel="akun")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pengguna"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        SEBELUM(kata="belum", tabel="pengguna")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULES UNTUK DB AKUNTANSI 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="perusahaan"),
        Fact(tabel="akun"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="akun"),
        SEBELUM(kata="memiliki", tabel="perusahaan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        SEBELUM(kata="terkait", tabel="detail_transaksi"),
        SEBELUM(kata="terkait", tabel="transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="periode_akuntansi"),
        Fact(tabel="transaksi"),
        SEBELUM(kata="tercatat", tabel="transaksi"),
        SEBELUM(kata="tercatat", tabel="periode_akuntansi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        SEBELUM(kata="mencatat", tabel="transaksi"),
        SEBELUM(kata="mencatat", tabel="pengguna")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        SEBELUM(kata="terkait", tabel="akun"),
        SEBELUM(kata="terkait", tabel="detail_transaksi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        SEBELUM(kata="digunakan", tabel="akun"),
        SEBELUM(kata="digunakan", tabel="detail_transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="perusahaan"),
        Fact(tabel="periode_akuntansi"),
        SEBELUM(kata="menetapkan", tabel="periode_akuntansi"),
        SEBELUM(kata="menetapkan", tabel="perusahaan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pengguna"),
        SEBELUM(kata="mencatat", tabel="transaksi"),
        SEBELUM(kata="mencatat", tabel="pengguna")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="periode_akuntansi"),
        SEBELUM(kata="terkait", tabel="periode_akuntansi"),
        SEBELUM(kata="terkait", tabel="transaksi")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        SEBELUM(kata="terlibat", tabel="akun"),
        SEBELUM(kata="terlibat", tabel="detail_transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="perusahaan"),
        Fact(tabel="akun"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="perusahaan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="akun")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="transaksi"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="periode_akuntansi"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="periode_akuntansi"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pengguna"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="transaksi")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_transaksi"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="akun")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="rincikan"),
        SEBELUM(kata="rincikan", tabel="akun"),
        Fact(kata="detail"),
        SEBELUM(kata="detail", tabel="detail_transaksi")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="perusahaan"),
        Fact(tabel="periode_akuntansi"),
        Fact(kata="tampilkan"),
        SEBELUM(kata="tampilkan", tabel="perusahaan"),
        Fact(kata="periode"),
        SEBELUM(kata="periode", tabel="periode_akuntansi")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="pengguna"),
        Fact(kata="sebutkan"),
        SEBELUM(kata="sebutkan", tabel="transaksi"),
        Fact(kata="pengguna"),
        SEBELUM(kata="pengguna", tabel="pengguna")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="periode_akuntansi"),
        Fact(tabel="transaksi"),
        Fact(kata="daftar"),
        SEBELUM(kata="daftar", tabel="periode_akuntansi"),
        Fact(kata="transaksi"),
        SEBELUM(kata="transaksi", tabel="transaksi"),
        Fact(kata="terjadi"),
        SEBELUM(kata="terjadi", tabel="periode_akuntansi")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="tampilkan"),
        SEBELUM(kata="tampilkan", tabel="akun"),
        Fact(kata="saldo"),
        SEBELUM(kata="saldo", tabel="akun"),
        Fact(kata="detail"),
        SEBELUM(kata="detail", tabel="detail_transaksi")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="perusahaan"),
        Fact(tabel="akun"),
        Fact(kata="tampilkan"),
        SEBELUM(kata="tampilkan", tabel="akun"),
        Fact(kata="perusahaan"),
        SEBELUM(kata="perusahaan", tabel="perusahaan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="transaksi"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="lihat"),
        SEBELUM(kata="lihat", tabel="detail_transaksi"),
        Fact(kata="transaksi"),
        SEBELUM(kata="transaksi", tabel="transaksi")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="periode_akuntansi"),
        Fact(tabel="transaksi"),
        Fact(kata="sebutkan"),
        SEBELUM(kata="sebutkan", tabel="transaksi"),
        Fact(kata="periode"),
        SEBELUM(kata="periode", tabel="periode_akuntansi")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="daftar"),
        SEBELUM(kata="daftar", tabel="transaksi"),
        Fact(kata="pengguna"),
        SEBELUM(kata="pengguna", tabel="pengguna")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="tampilkan"),
        SEBELUM(kata="tampilkan", tabel="akun"),
        Fact(kata="detail"),
        SEBELUM(kata="detail", tabel="detail_transaksi")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="akun"),
        Fact(tabel="detail_transaksi"),
        Fact(kata="rincikan"),
        SEBELUM(kata="rincikan", tabel="detail_transaksi"),
        Fact(kata="akun"),
        SEBELUM(kata="akun", tabel="akun")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="perusahaan"),
        Fact(tabel="periode_akuntansi"),
        Fact(kata="tampilkan"),
        SEBELUM(kata="tampilkan", tabel="periode_akuntansi"),
        Fact(kata="perusahaan"),
        SEBELUM(kata="perusahaan", tabel="perusahaan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pengguna"),
        Fact(tabel="transaksi"),
        Fact(kata="sebutkan"),
        SEBELUM(kata="sebutkan", tabel="transaksi"),
        Fact(kata="pengguna"),
        SEBELUM(kata="pengguna", tabel="pengguna")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="periode_akuntansi"),
        Fact(tabel="transaksi"),
        Fact(kata="daftar"),
        SEBELUM(kata="daftar", tabel="transaksi"),
        Fact(kata="periode"),
        SEBELUM(kata="periode", tabel="periode_akuntansi")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_transaksi"),
        Fact(tabel="akun"),
        Fact(kata="tampilkan"),
        SEBELUM(kata="tampilkan", tabel="detail_transaksi"),
        Fact(kata="akun"),
        SEBELUM(kata="akun", tabel="akun")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULE UNTUK DB PEMESANAN 1 ===========================

# RULE INNER JOIN
    @Rule( 
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="memiliki", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="dibayar"),
        SEBELUM(kata="dibayar", tabel="pesanan"),
        SEBELUM(kata="dibayar", tabel="pembayaran"),
        SEBELUM(kata="dipesan", tabel="produk"),
        SEBELUM(kata="dipesan", tabel="detail_pesanan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="dipesan"),
        SEBELUM(kata="dipesan", tabel="produk"),
        SEBELUM(kata="dipesan", tabel="detail_pesanan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="dibeli"),
        SEBELUM(kata="dibeli", tabel="produk"),
        SEBELUM(kata="dibeli", tabel="pesanan"),
        SEBELUM(kata="dibeli", tabel="pembayaran")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pesanan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pembayaran"),
        SEBELUM(kata="memiliki", tabel="pesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="memiliki"),
        Fact(kata="benar-benar"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="memiliki", tabel="pelanggan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="pesanan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="detail_pesanan"),
        SEBELUM(kata="memiliki", tabel="pesanan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="memiliki"),
        Fact(kata="dipesan"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="memiliki", tabel="pembayaran"),
        SEBELUM(kata="dipesan", tabel="produk"),
        SEBELUM(kata="dipesan", tabel="detail_pesanan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="melakukan"),
        Fact(kata="pembayaran"),
        SEBELUM(kata="melakukan", tabel="pelanggan"),
        SEBELUM(kata="pembayaran", tabel="pembayaran"),
        SEBELUM(kata="pembayaran", tabel="pesanan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="dipesan"),
        Fact(kata="dibayar"),
        SEBELUM(kata="dipesan", tabel="produk"),
        SEBELUM(kata="dipesan", tabel="detail_pesanan"),
        SEBELUM(kata="dibayar", tabel="pesanan"),
        SEBELUM(kata="dibayar", tabel="pembayaran")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pembayaran")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pembayaran")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pelanggan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_pesanan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pembayaran"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="pesanan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="pesanan"),
        Fact(kata="data"),
        SEBELUM(kata="data", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULE UNTUK DB PEMESANAN 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="melakukan"),
        SEBELUM(kata="melakukan", tabel="pesanan"),
        SEBELUM(kata="melakukan", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="memiliki", tabel="pelanggan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="produk"),
        SEBELUM(kata="ada", tabel="detail_pesanan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pembayaran"),
        Fact(tabel="pesanan"),
        Fact(kata="telah dilakukan"),
        SEBELUM(kata="telah dilakukan", tabel="pembayaran"),
        SEBELUM(kata="telah dilakukan", tabel="pesanan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="memiliki", tabel="detail_pesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="melakukan"),
        Fact(kata="menggunakan"),
        SEBELUM(kata="melakukan", tabel="pesanan"),
        SEBELUM(kata="melakukan", tabel="pelanggan"),
        SEBELUM(kata="menggunakan", tabel="pembayaran"),
        SEBELUM(kata="menggunakan", tabel="pesanan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="terdapat"),
        SEBELUM(kata="terdapat", tabel="produk"),
        SEBELUM(kata="terdapat", tabel="detail_pesanan"),
        SEBELUM(kata="terdapat", tabel="pesanan"),
        COND(nama="pesanan.id_pesanan", nilai=123)
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="melakukan"),
        Fact(kata="menggunakan"),
        SEBELUM(kata="melakukan", tabel="pesanan"),
        SEBELUM(kata="melakukan", tabel="pelanggan"),
        SEBELUM(kata="menggunakan", tabel="pembayaran"),
        SEBELUM(kata="menggunakan", tabel="pesanan"),
        COND(nama="pembayaran.metode_pembayaran", nilai="transfer bank")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="detail_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="pernah dipesan"),
        SEBELUM(kata="pernah dipesan", tabel="produk"),
        SEBELUM(kata="pernah dipesan", tabel="detail_pesanan"),
        SEBELUM(kata="pernah dipesan", tabel="pesanan"),
        SEBELUM(kata="pernah dipesan", tabel="pelanggan"),
        COND(nama="pelanggan.id_pelanggan", nilai=123)
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="memiliki", tabel="pembayaran")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="setiap"),
        SEBELUM(kata="setiap", tabel="pelanggan"),
        Fact(kata="tidak ada"),
        SEBELUM(kata="tidak ada", tabel="pesanan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="daftar lengkap"),
        SEBELUM(kata="daftar lengkap", tabel="pelanggan"),
        Fact(kata="alamat pengiriman"),
        SEBELUM(kata="alamat pengiriman", tabel="pesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="total harga"),
        SEBELUM(kata="total harga", tabel="pesanan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="metode pembayaran"),
        SEBELUM(kata="metode pembayaran", tabel="pembayaran")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="setiap"),
        SEBELUM(kata="setiap", tabel="pelanggan"),
        Fact(kata="tanggal pembayaran"),
        SEBELUM(kata="tanggal pembayaran", tabel="pembayaran")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="pembayaran"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="status pembayaran"),
        SEBELUM(kata="status pembayaran", tabel="pembayaran")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(tabel="detail_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="jumlah produk"),
        SEBELUM(kata="jumlah produk", tabel="detail_pesanan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="nama pelanggan"),
        SEBELUM(kata="nama pelanggan", tabel="pelanggan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="alamat pengiriman"),
        SEBELUM(kata="alamat pengiriman", tabel="pesanan"),
        SEBELUM(kata="alamat pengiriman", tabel="pelanggan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="nomor telepon"),
        SEBELUM(kata="nomor telepon", tabel="pesanan"),
        SEBELUM(kata="nomor telepon", tabel="pelanggan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="email"),
        SEBELUM(kata="email", tabel="pesanan"),
        SEBELUM(kata="email", tabel="pelanggan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="id_pelanggan"),
        SEBELUM(kata="id_pelanggan", tabel="pesanan"),
        SEBELUM(kata="id_pelanggan", tabel="pelanggan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="tanggal_pendaftaran"),
        SEBELUM(kata="tanggal_pendaftaran", tabel="pesanan"),
        SEBELUM(kata="tanggal_pendaftaran", tabel="pelanggan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="alamat_pengiriman"),
        SEBELUM(kata="alamat_pengiriman", tabel="pesanan"),
        SEBELUM(kata="alamat_pengiriman", tabel="pelanggan")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="nama_pelanggan"),
        SEBELUM(kata="nama_pelanggan", tabel="pesanan"),
        SEBELUM(kata="nama_pelanggan", tabel="pelanggan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="nomor_telepon"),
        SEBELUM(kata="nomor_telepon", tabel="pesanan"),
        SEBELUM(kata="nomor_telepon", tabel="pelanggan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

# ======================= RULE UNTUK DB PENJUALAN 1 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="penjualan"),
        Fact(kata="sudah"),
        SEBELUM(kata="sudah", tabel="penjualan"),
        SEBELUM(kata="sudah", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="pernah"),
        SEBELUM(kata="pernah", tabel="detail_penjualan"),
        SEBELUM(kata="pernah", tabel="produk")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="detail_penjualan"),
        SEBELUM(kata="memiliki", tabel="penjualan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="detail_penjualan"),
        SEBELUM(kata="memiliki", tabel="penjualan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="penjualan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="penjualan"),
        SEBELUM(kata="memiliki", tabel="pelanggan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="dijual"),
        SEBELUM(kata="dijual", tabel="detail_penjualan"),
        SEBELUM(kata="dijual", tabel="produk")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="pelanggan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="pelanggan"),
        SEBELUM(kata="memiliki", tabel="penjualan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="kategori_produk"),
        Fact(tabel="produk"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="kategori_produk")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="detail_penjualan"),
        Fact(tabel="produk"),
        Fact(tabel="penjualan"),
        Fact(kata="memiliki"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="memiliki", tabel="penjualan"),
        SEBELUM(kata="memiliki", tabel="detail_penjualan")
        )
    )
    def r9(self):
        self.declare(TipeJoinTiga(nama='INNERJOIN'))

@rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="penjualan"),
        Fact(kata="melakukan"),
        SEBELUM(kata="melakukan", tabel="penjualan"),
        SEBELUM(kata="melakukan", tabel="pelanggan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
@rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="penjualan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="penjualan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="termasuk"),
        SEBELUM(kata="termasuk", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_penjualan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="pelanggan"),
        Fact(kata="lengkap"),
        SEBELUM(kata="lengkap", tabel="penjualan"),
        Fact(kata="meskipun"),
        SEBELUM(kata="meskipun", tabel="penjualan"),
        Fact(kata="tanpa"),
        SEBELUM(kata="tanpa", tabel="pelanggan")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="detail_penjualan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="jika"),
        SEBELUM(kata="jika", tabel="penjualan"),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="penjualan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori_produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kategori_produk")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="detail_penjualan")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="kategori_produk"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kategori_produk"),
        Fact(kata="meski"),
        SEBELUM(kata="meski", tabel="kategori_produk"),
        Fact(kata="kosong"),
        SEBELUM(kata="kosong", tabel="produk")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="penjualan"),
        Fact(kata="jika"),
        SEBELUM(kata="jika", tabel="detail_penjualan"),
        Fact(kata="tersedia"),
        SEBELUM(kata="tersedia", tabel="detail_penjualan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

@rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="beserta"),
        SEBELUM(kata="beserta", tabel="pelanggan"),
        Fact(kata="riwayat"),
        SEBELUM(kata="riwayat", tabel="penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="penjualan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='LEFTJOIN'))

# RULE RIGHT JOIN
@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="pelanggan"),
        Fact(kata="tercatat"),
        SEBELUM(kata="tercatat", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="detail_penjualan"),
        Fact(tabel="penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="detail_penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="penjualan"),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="penjualan")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_penjualan"),
        Fact(kata="termasuk"),
        SEBELUM(kata="termasuk", tabel="detail_penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="produk"),
        Fact(kata="lengkap"),
        SEBELUM(kata="lengkap", tabel="produk")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="detail_penjualan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_penjualan"),
        Fact(kata="bahkan"),
        SEBELUM(kata="bahkan", tabel="detail_penjualan"),
        Fact(kata="dihapus"),
        SEBELUM(kata="dihapus", tabel="produk")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="detail_penjualan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_penjualan"),
        Fact(kata="meskipun"),
        SEBELUM(kata="meskipun", tabel="detail_penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="produk"),
        Fact(kata="cocok"),
        SEBELUM(kata="cocok", tabel="produk")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="penjualan"),
        Fact(kata="hilang"),
        SEBELUM(kata="hilang", tabel="pelanggan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="kategori_produk"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="termasuk"),
        SEBELUM(kata="termasuk", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kategori_produk"),
        Fact(kata="dimasukkan"),
        SEBELUM(kata="dimasukkan", tabel="kategori_produk")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="detail_penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="detail_penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="produk"),
        Fact(kata="tersedia"),
        SEBELUM(kata="tersedia", tabel="produk"),
        Fact(kata="stok"),
        SEBELUM(kata="stok", tabel="produk")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="penjualan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="penjualan"),
        Fact(kata="jika"),
        SEBELUM(kata="jika", tabel="pelanggan"),
        Fact(kata="tersedia"),
        SEBELUM(kata="tersedia", tabel="pelanggan"),
        Fact(kata="namun"),
        SEBELUM(kata="namun", tabel="penjualan"),
        Fact(kata="tetap"),
        SEBELUM(kata="tetap", tabel="penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="pelanggan"),
        Fact(kata="ada"),
        SEBELUM(kata="ada", tabel="pelanggan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='RIGHTJOIN'))

@rule(
    AND(
        Fact(tabel="detail_penjualan"),
        Fact(tabel="penjualan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="detail_penjualan"),
        Fact(kata="walaupun"),
        SEBELUM(kata="walaupun", tabel="detail_penjualan"),
        Fact(kata="tidak"),
        SEBELUM(kata="tidak", tabel="penjualan"),
        Fact(kata="ditemukan"),
        SEBELUM(kata="ditemukan", tabel="penjualan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='RIGHTJOIN',))

# ======================= RULES UNTUK DB PENJUALAN 2 ===========================

# RULE INNER JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="telah"),
        Fact(kata="membuat"),
        SEBELUM(kata="telah", tabel="pesanan"),
        SEBELUM(kata="telah", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="termasuk"),
        Fact(kata="kategori"),
        SEBELUM(kata="termasuk", tabel="produk"),
        SEBELUM(kata="kategori", tabel="kategori")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="pemasok"),
        Fact(kata="disuplai"),
        Fact(kata="pemasok"),
        SEBELUM(kata="disuplai", tabel="produk"),
        SEBELUM(kata="pemasok", tabel="pemasok")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="item_pesanan"),
        Fact(kata="memiliki"),
        Fact(kata="item"),
        SEBELUM(kata="memiliki", tabel="pesanan"),
        SEBELUM(kata="item", tabel="item_pesanan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="item_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="terkait"),
        Fact(kata="produk"),
        SEBELUM(kata="terkait", tabel="item_pesanan"),
        SEBELUM(kata="produk", tabel="produk")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="memiliki"),
        Fact(kata="alamat"),
        Fact(kata="pengiriman"),
        SEBELUM(kata="memiliki", tabel="pelanggan"),
        SEBELUM(kata="alamat", tabel="pesanan"),
        SEBELUM(kata="pengiriman", tabel="pesanan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(tabel="pemasok"),
        Fact(kata="memiliki"),
        Fact(kata="informasi"),
        Fact(kata="kategori"),
        Fact(kata="pemasok"),
        SEBELUM(kata="memiliki", tabel="produk"),
        SEBELUM(kata="kategori", tabel="kategori"),
        SEBELUM(kata="pemasok", tabel="pemasok")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="kategori"),
        Fact(tabel="produk"),
        Fact(kata="memiliki"),
        Fact(kata="produk"),
        SEBELUM(kata="memiliki", tabel="kategori"),
        SEBELUM(kata="produk", tabel="produk")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="pemasok"),
        Fact(tabel="produk"),
        Fact(kata="menyuplai"),
        Fact(kata="produk"),
        SEBELUM(kata="menyuplai", tabel="pemasok"),
        SEBELUM(kata="produk", tabel="produk")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="item_pesanan"),
        Fact(tabel="pesanan"),
        Fact(kata="dipesan"),
        Fact(kata="informasi"),
        Fact(kata="pesanan"),
        SEBELUM(kata="dipesan", tabel="produk"),
        SEBELUM(kata="informasi", tabel="pesanan"),
        SEBELUM(kata="pesanan", tabel="pesanan")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='INNERJOIN'))

# RULE LEFT JOIN
    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kategori")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="pemasok"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemasok"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="kategori"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kategori"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="item_pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="item_pesanan")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="pelanggan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pelanggan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pemasok")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="kategori"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="kategori"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="pemasok"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pemasok"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='leftjoin'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kategori")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='leftjoin'))

# RULE RIGHT JOIN
    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pelanggan")
        )
    )
    def r1(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kategori")
        )
    )
    def r2(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="produk"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="produk"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pemasok")
        )
    )
    def r3(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="item_pesanan"),
        Fact(tabel="pesanan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="item_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pesanan")
        )
    )
    def r4(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="item_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="item_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r5(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pelanggan")
        )
    )
    def r6(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="item_pesanan"),
        Fact(tabel="produk"),
        Fact(tabel="kategori"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="item_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="kategori")
        )
    )
    def r7(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="item_pesanan"),
        Fact(tabel="produk"),
        Fact(tabel="pemasok"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="item_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pemasok")
        )
    )
    def r8(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="pesanan"),
        Fact(tabel="pelanggan"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="pelanggan")
        )
    )
    def r9(self):
        self.declare(Fact(tipe_join='rightjoin'))

    @Rule(
    AND(
        Fact(tabel="item_pesanan"),
        Fact(tabel="produk"),
        Fact(kata="semua"),
        SEBELUM(kata="semua", tabel="item_pesanan"),
        Fact(kata="belum"),
        SEBELUM(kata="belum", tabel="produk")
        )
    )
    def r10(self):
        self.declare(Fact(tipe_join='rightjoin'))
    #======================================================================================================

        
        @Rule()
    def rule_remove_duplicates_facts(self):
        seen = set()
        duplicates = []
        
        for fid, fact in self.facts.items():
            if isinstance(fact, Fact):
                key = tuple(fact.items())
                if key in seen:
                    duplicates.append(fid)
                else:
                    seen.add(key)

        for fid in duplicates:
            self.retract(fid)
    
        @Rule(
        OR(
            Fact(jenis_join='LEFTJOIN'), Fact(jenis_join='RIGHTJOIN'), Fact(jenis_join='INNERJOIN')
        )
    )
    def rule_remove_nojoin_if_join_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_join' in fact and fact['jenis_join']=='NOJOIN':
                self.retract(id)
        self.halt()

    
        @Rule(Fact(kalimat=MATCH.kalimat), salience=3)
    def rule_extract_kalimat_to_kata(self, kalimat):
        kalimat = kalimat.lower().strip()
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        kalimat = re.sub(r'[^a-zA-Z0-9 ]','',kalimat)
        daftar_kata = kalimat.split()
        
        for kata in daftar_kata:
            self.declare(Fact(kata=kata))
            

        @Rule(Fact(database=MATCH.database), salience=3)
    def rule_extract_database(self, database):
        for tabel in database['entitas']:
            self.declare(Fact(tabel=tabel))
    

        @Rule(
        AND(Fact(kalimat=MATCH.kalimat),Fact(database=MATCH.database)),salience=2
    )
    def rule_add_matching_domain(self, kalimat, database):
        is_domain_match = False
        daftar_kata = [fact['kata'] for _,fact in self.facts.items() if isinstance(fact, Fact) and 'kata' in fact]
        daftar_tabel = [fact['tabel'] for _,fact in self.facts.items() if isinstance(fact, Fact) and 'tabel' in fact]
        for kata in daftar_kata:
            for tabel in daftar_tabel:
                if textdistance.jaccard.normalized_similarity(kata, tabel)>0.7:
                    is_domain_match = True
                    break
            if is_domain_match:
                break
        self.declare(Fact(domain_cocok=is_domain_match))


        @Rule(Fact(domain_cocok=False))
    def rule_quit_if_domain_not_match(self):
        self.halt()

    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(Fact(kalimat=kalimat), Fact(database=database))
        self.run()

        for fact in self.facts.values():
            if 'jenis_join' in fact:
                return fact['jenis_join']
        return 'NOJOIN'