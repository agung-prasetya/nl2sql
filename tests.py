import unittest
from detectors import QtyDetector

class TestQtyDetector(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.detector=QtyDetector()
        self.filepath_database_json='detectors/qty/dataset/gudang.json'
        
    def test_rule_identifikasi_frase_tanpa_satuan_ke_kuantitas_1(self):
        kalimat=('Tampilkan transaksi yang nilainya diatas satu juta dua ratus sebelas ribu lima ratus tiga puluh enam')
        self.assertListEqual(
            ['satu juta dua ratus sebelas ribu lima ratus tiga puluh enam'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_frase_tanpa_satuan_ke_kuantitas_2(self):
        kalimat=('Tampilkan transaksi yang nilainya antara '
                 'sebelas juta empat ratus tiga puluh lima ribu tujuh puluh satu hingga '
                 'satu juta dua ratus sebelas ribu lima ratus tiga puluh enam')
        self.assertListEqual(
            ['sebelas juta empat ratus tiga puluh lima ribu tujuh puluh satu',
             'satu juta dua ratus sebelas ribu lima ratus tiga puluh enam'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_frase_tanpa_satuan_ke_kuantitas_3(self):
        kalimat=('Tampilkan transaksi yang nilainya antara '
                 'sebelas juta empat ratus tiga puluh lima ribu tujuh puluh satu rupiah hingga '
                 'satu juta dua ratus sebelas ribu lima ratus tiga puluh enam rupiah'
        )
        self.assertListEqual(
            ['sebelas juta empat ratus tiga puluh lima ribu tujuh puluh satu rupiah',
             'satu juta dua ratus sebelas ribu lima ratus tiga puluh enam rupiah'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_kata_tanpa_satuan1(self):
        kalimat=('Tampilkan transaksi yang nilainya antara 1000000 hingga 1500000')
        self.assertListEqual(
            ['1000000','1500000'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_kuantitas_dari_kata_tanpa_satuan2(self):
        kalimat=('Tampilkan transaksi yang nilainya terbanyak keempat.')
        self.assertListEqual(
            ['keempat'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_kata_tanpa_satuan3(self):
        kalimat=('Tampilkan transaksi yang nilainya terbanyak keenam dari 10 teratas')
        self.assertListEqual(
            ['keenam','10'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_kata_tanpa_satuan4(self):
        kalimat=('Tampilkan transaksi antara tanggal 5/12/25 hingga 10/12/25')
        self.assertListEqual(
            ['5/12/25','10/12/25'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_kata_tanpa_satuan5(self):
        kalimat=('Tampilkan transaksi yang diskonnya (dalam persen) diantara 1.5 hingga 2.1')
        self.assertListEqual(
            ['1.5','2.1'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_kuantitas_dari_kata_tanpa_satuan6(self):
        kalimat=('Tampilkan transaksi yang nilainya terbanyak ke-iv dari 10 teratas')
        self.assertListEqual(
            ['ke-iv','10'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_kuantitas_dari_gabungan_satuan_dan_bilangan_bulat_atau_pecahan1(self):
        kalimat=('Tampilkan transaksi yang totalnya diatas Rp 500.000,00 dan dibawah Rp 1.000.000,00')
        self.assertListEqual(
            ['rp 500.000,00','rp 1.000.000,00'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_kuantitas_dari_gabungan_satuan_dan_bilangan_bulat_atau_pecahan2(self):
        kalimat=(f'Tampilkan transaksi yang nilainya diatas $ 10.2 dan dibawah $ 100,23')
        self.assertListEqual(
            ['$ 10.2','$ 100,23'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    
    def test_rule_identifikasi_kuantitas_dari_literal(self):
        kalimat=('Tampilkan transaksi yang totalnya diatas Rp500.000,00 dan dibawah Rp1.000.000,00')
        self.assertListEqual(
            ['rp500.000,00','rp1.000.000,00'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_kuantitas_dari_gabungan_kata_bilangan_bulat_dengan_satuan1(self):
        kalimat=('Tampilkan nama pelanggan yang jumlah produk yang dibelinya '
                 'lebih dari delapan buah.')
        self.assertListEqual(
            ['delapan buah'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_kuantitas_dari_gabungan_kata_bilangan_bulat_dengan_satuan2(self):
        kalimat=('Tampilkan nama pelanggan yang jumlah produk yang dibelinya '
                 'lebih dari delapan biji dan kurang dari sebelas biji')
        self.assertListEqual(
            ['delapan biji', 'sebelas biji'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_gabungan_kata_bilangan_bulat_dengan_satuan3(self):
        kalimat=('Tampilkan nama pelanggan yang jumlah produk yang dibelinya '
                 'lebih dari 250 biji dan kurang dari 1500 biji')
        self.assertListEqual(
            ['250 biji', '1500 biji'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
    def test_rule_identifikasi_frase_tanggal_bulan_tahun1(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 17 Agustus 2025 beserta jumlahnya')
        self.assertListEqual(
            ['17 agustus 2025'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_frase_tanggal_bulan_tahun2(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 1 Agustus 2025 beserta jumlahnya')
        self.assertListEqual(
            ['1 agustus 2025'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_frase_tanggal_bulan_tahun3(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 1 Agustus 25 beserta jumlahnya')        
        self.assertListEqual(
            ['1 agustus 25'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_frase_tanggal_bulan_tahun3(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 01 Agustus 25 beserta jumlahnya')        
        self.assertListEqual(
            ['01 agustus 25'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def rule_identifikasi_kuantitas_dari_frase_tanggal_bulan1(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 20 September')        
        self.assertListEqual(
            ['20 september'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def rule_identifikasi_kuantitas_dari_frase_tanggal_bulan1(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 2 September')        
        self.assertListEqual(
            ['2 september'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def rule_identifikasi_kuantitas_dari_frase_tanggal_bulan2(self):
        kalimat=('Tampilkan transaksi sebelum tanggal 02 September')        
        self.assertListEqual(
            ['02 september'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_frase_bulan_tahun1(self):
        kalimat=('Tampilkan transaksi sebelum Desember 2024')        
        self.assertListEqual(
            ['desember 2024'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
    
    def test_rule_identifikasi_kuantitas_dari_frase_bulan_tahun2(self):
        kalimat=('Tampilkan transaksi sebelum antara Jan 24 - Desember 24')        
        self.assertListEqual(
            ['jan 24','desember 24'],
            self.detector.detect(kalimat, self.filepath_database_json)
        )
        
        
    