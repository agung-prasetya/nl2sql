from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class UndefDetector(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        
    #Urutan 1
    #Rule ini mengubah kalimat yang tak ternormalisasi ke normalisasi.
    #Rule ini dieksekusi yang paling awal karena input paling awal agar sistem ini bekerja adalah dengan adanya kalimat ternormalisasi.
    #Kalimat ternormalisasi dalam konteks ini adalah sebuah kalimat yang penulisanya terstandar, yaitu 
    # semua huruf adalah huruf kecil, tidak ada tanda baca seperti .,'"/\, jumlah spasi adalah 1 untuk pemisah antar kata.
    #Pada penelitian ini, selain kata-kata imbuhan, versi kata dasarnya juga dimasukkan sebagai fact.
    #Rule ini akan aktif apabila agenda memiliki sebuah fact dengan informasi kalimat dan ternormalisasi False.
    #Agar rule ini diekseksui untuk pertama kali, maka bobot nya harus terbesar. Bobot/salience nya adalah 300
    @Rule(
        AS.fact_kalimat_tak_ternormalisasi << Fact(kalimat=MATCH.kalimat, ternormalisasi=False), 
        salience=500
    )    
    def rule_penambahan_fact_kalimat_ternormalisasi(self, fact_kalimat_tak_ternormalisasi):
        kalimat_ternormalisasi = fact_kalimat_tak_ternormalisasi['kalimat'].lower().strip()
        kalimat_ternormalisasi = re.sub(r'\s+', ' ', kalimat_ternormalisasi).strip()
        kalimat_ternormalisasi = re.sub(r'[.,\'"\/\\\)\\(;:]','',kalimat_ternormalisasi)
        
        self.modify(fact_kalimat_tak_ternormalisasi, kalimat=kalimat_ternormalisasi, ternormalisasi=True)
    
    
    #Urutan 2 - penambahan kalimat ter-stemming
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=True), 
        salience=495
    )    
    def rule_penambahan_fact_kalimat_terstemming(self, kalimat):
        kalimat_terstemming = self.stemmer.stem(kalimat)
        self.declare(Fact(kalimat=kalimat_terstemming, terstemming=True))
        
    
    #Urutan 3 - penambahan fact frase (kata termasuk frase) dari kedua kalimat ternormalisasi dan terstemming
    @Rule(
        AND(
            Fact(kalimat=MATCH.kalimat_ternormalisasi, ternormalisasi=True), 
            Fact(kalimat=MATCH.kalimat_terstemming, terstemming=True)
        ),
        salience=490
    )    
    def rule_penambahan_fact_frase(self, kalimat_ternormalisasi, kalimat_terstemming):
        daftar_frase_ternormalisasi = self.get_frase(kalimat=kalimat_ternormalisasi)
        for frase in daftar_frase_ternormalisasi:
            self.declare(Fact(frase=frase['frase'],posisi_awal=frase['posisi_awal'],posisi_akhir=frase['posisi_akhir']))
            
        daftar_frase_terstemming = self.get_frase(kalimat=kalimat_terstemming)
        for frase in daftar_frase_terstemming:
            if not any(item for item in daftar_frase_ternormalisasi if item['frase']==frase['frase']):
                self.declare(Fact(frase=frase['frase'], posisi_awal=frase['posisi_awal'], posisi_akhir=frase['posisi_akhir']))

    
    #Ekstraksi database - tabel - kolom menjadi bagian dari fact tabel
    @Rule(AS.fact_database << Fact(database=MATCH.database), salience=490)
    def rule_ekstraksi_tabel_kolom(self, fact_database):
        self.declare(Fact(database=fact_database['database']))
        for tabel in fact_database['database']['entitas']:
            for kolom in fact_database['database']['entitas'][tabel]:
                self.declare(Fact(tabel=tabel.replace('_',' '), kolom=kolom.replace('_',' ')))
        self.retract(fact_database)
        
    #Identifikasi kata - DML INSERT 
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_dml' not in fact_frase),
        TEST(lambda frase: frase in ['tambah','masuk','sisip','input']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_dml_insert(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_dml='insert')
    
    #Identifikasi kata - DML UPDATE 
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_dml' not in fact_frase),
        TEST(lambda frase: frase in ['edit','update','ubah','perbarui']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_dml_update(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_dml='update')
    
    #Identifikasi kata - DML SELECT 
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_dml' not in fact_frase),
        TEST(lambda frase: frase in ['tampil','lihat','cari','ambil','tunjuk','berapa jumlah','berapa rata-rata','tahu']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_dml_select(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_dml='select')
        
    #Identifikasi kata - DML DELETE 
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_dml' not in fact_frase),
        TEST(lambda frase: frase in ['hapus','delete','hilang','musnah']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_dml_delete(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_dml='delete')
           
        
    #Identifikasi kata - CREATE 
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_ddl' not in fact_frase),
        TEST(lambda frase: frase in ['buat','bangun','cipta','tambah','siap','sedia','inisialisasi',
                                   'mulai dengan','rancang','susun','tetap','formula','bentuk','konstruksi']
        ),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_ddl_create(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_ddl='create')
        
        
    #Identifikasi kata - DROP
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_ddl' not in fact_frase),
        TEST(lambda frase: frase in ['hapus','hilang','buang','copot','lepas','singkir','musnah',
                                   'bersih','kosong','enyah','rusak']
        ),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_ddl_drop(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_ddl='drop')
     
     
     
    #Identifikasi kata - ALTER
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi' not in fact_frase),
        TEST(lambda frase: frase in ['ubah','edit','modifikasi','perbarui','revisi','ganti','sesuaikan','koreksi','tingkatkan']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_alter(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_ddl='alter')
        
    
    
    #Identifikasi kata - SHOW
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_ddl' not in fact_frase),
        TEST(lambda frase: frase in ['tampil','lihat','ambil','cari','periksa','lacak','telusuri','tinjau','akses','dapatkan']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_ddl_show(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_ddl='show')
        
        
    #Identifikasi kata - USE
    @Rule(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'jenis_aksi_ddl' not in fact_frase),
        TEST(lambda frase: frase in ['gunakan','pilih','ambil','terapkan','beralih ke','pakailah','aktifkan']),
        salience=470
    )
    def rule_identifikasi_jenis_aksi_ddl_use(self,fact_frase):
        self.modify(fact_frase, jenis_aksi_ddl='use')
        
    
    #Identifikasi frase yang merujuk pada nama database
    @Rule(
        Fact(database=MATCH.database),
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'adalah_nama_database' not in fact_frase),
        TEST(lambda frase, database: frase==database),
        salience=465
    )
    def rule_identifikasi_nama_database(self,fact_frase):
        self.modify(fact_frase, adalah_nama_database=True)
    
        
    #Identifikasi frase yang merujuk pada nama tabel
    @Rule(
        Fact(tabel=MATCH.tabel),
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'adalah_nama_tabel' not in fact_frase),
        TEST(lambda frase, tabel: frase in tabel),
        salience=460
    )
    def rule_identifikasi_nama_tabel(self,fact_frase):
        self.modify(fact_frase, adalah_nama_tabel=True)
        
        
        
    #Identifikasi frase yang merujuk pada nama kolom suatu tabel
    @Rule(
        AND(
            Fact(tabel=MATCH.tabel, kolom=MATCH.kolom),
            Fact(frase=MATCH.frase_tabel, adalah_nama_tabel=True),
            TEST(lambda tabel, frase_tabel: frase_tabel in tabel),
        
            AS.fact_kolom << Fact(frase=MATCH.frase_kolom),
            TEST(lambda fact_kolom: 'adalah_nama_kolom' not in fact_kolom),
            TEST(lambda frase_kolom, kolom: frase_kolom in kolom)
        ),
        salience=460
    )
    def rule_identifikasi_nama_kolom(self,fact_kolom):
        self.modify(fact_kolom, adalah_nama_kolom=True)
    
    
    
    #Identifikasi DML - POLA 1
    #Pola select, tabel, kolom, tabel, kolom
    #contoh: Tampilkan semua reservasi yang dilakukan oleh tamu dengan email 'tamu@example.com' beserta total pembayaranya.
    @Rule(
        AND(
            Fact(jenis_aksi_dml='select'),
            Fact(adalah_nama_tabel=True, frase=MATCH.tabel1),
            Fact(adalah_nama_kolom=True, frase=MATCH.kolom1),
            Fact(adalah_nama_tabel=True, frase=MATCH.tabel2),
            Fact(adalah_nama_kolom=True, frase=MATCH.kolom2),
        ),
        salience=455
    )
    def rule_identifikasi_dml_1(self):
        self.declare(Fact(jenis_kalimat='TERDEFINISI'))
        
        
    
    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(
            Fact(kalimat=kalimat, ternormalisasi=False), 
            Fact(database=database)
        )
        self.run()
            
        for fact in self.facts.values():
            if 'jenis_kalimat' in fact:
                return fact['jenis_kalimat']
        return 'TIDAKTERDEFINISI'


    def get_frase(self, kalimat):
        daftar_frase=[]
        daftar_kata = kalimat.split()
        jumlah_kata = len(daftar_kata)
        for kelompok_frase in range(1, jumlah_kata+1):
            for posisi_kata in range(jumlah_kata+1-kelompok_frase):
                frase = []
                for bagian in range(kelompok_frase):
                    frase.append(daftar_kata[posisi_kata + bagian])
                                
                daftar_frase.append(
                    {'frase':' '.join(frase), 'posisi_awal':posisi_kata, 'posisi_akhir':posisi_kata+kelompok_frase-1}
                )
        return daftar_frase