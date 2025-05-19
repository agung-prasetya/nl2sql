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
        salience=300
    )    
    def rule_penambahan_fact_kalimat_ternormalisasi(self, fact_kalimat_tak_ternormalisasi):
        kalimat_ternormalisasi = fact_kalimat_tak_ternormalisasi['kalimat'].lower().strip()
        kalimat_ternormalisasi = re.sub(r'\s+', ' ', kalimat_ternormalisasi).strip()
        kalimat_ternormalisasi = re.sub(r'[.,\'"\/\\\)\\(;:]','',kalimat_ternormalisasi)
        
        self.modify(fact_kalimat_tak_ternormalisasi, kalimat=kalimat_ternormalisasi, ternormalisasi=True)
    
    
    #Urutan 2 - penambahan kalimat ter-stemming
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=True), 
        salience=295
    )    
    def rule_penambahan_fact_kalimat_terstemming(self, kalimat):
        kalimat_terstemming = self.stemmer.stem(kalimat)
        self.declare(Fact(kalimat=kalimat_terstemming, terstemming=True))
        
    
    #Urutan 3 - penambahan fact kata dari kedua kalimat ternormalisasi dan terstemming
    #Kata yang sudah dalam bentuk kata dasar tidak ditambahkan untuk mengurangi jumlah fact.
    @Rule(
        AND(
            Fact(kalimat=MATCH.kalimat_ternormalisasi, ternormalisasi=True), 
            Fact(kalimat=MATCH.kalimat_terstemming, terstemming=True)
        ),
        salience=290
    )    
    def rule_penambahan_fact_kata(self, kalimat_ternormalisasi, kalimat_terstemming):
        daftar_kata_kalimat_ternormalisasi = kalimat_ternormalisasi.split()
        for id, kata in enumerate(daftar_kata_kalimat_ternormalisasi):
            self.declare(Fact(kata=kata, posisi=id))
            
        daftar_kata_kalimat_terstemming = kalimat_terstemming.split()
        for id, kata in enumerate(daftar_kata_kalimat_terstemming):
            if kata not in daftar_kata_kalimat_ternormalisasi:
                self.declare(Fact(kata=kata, posisi=id))
        
    
    @Rule(
        AS.fact_kata << Fact(kata=MATCH.kata),
        TEST(lambda fact_kata: 'jenis_aksi' not in fact_kata),
        TEST(lambda kata: kata in ['buat','bangun','cipta','tambah','siap','sedia','inisialisasi',
                                   'mulai dengan','rancang','susun','tetap','formula','bentuk',
                                    'konstruksi']
        ),
        salience=285
    )
    def rule_identifikasi_jenis_aksi_create(self,fact_kata):
        self.modify(fact_kata, jenis_aksi='create')
        
        
    #Delete == drop
    @Rule(
        AS.fact_kata << Fact(kata=MATCH.kata),
        TEST(lambda fact_kata: 'jenis_aksi' not in fact_kata),
        TEST(lambda kata: kata in ['hapus','hilang','buang','copot','lepas','singkir','musnah',
                                   'bersih','kosong','enyah','rusak']
        ),
        salience=285
    )
    def rule_identifikasi_jenis_aksi_create(self,fact_kata):
        self.modify(fact_kata, jenis_aksi='drop')
     
     
     
     
        
    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(
            Fact(kalimat=kalimat, ternormalisasi=False), 
            Fact(database=database)
        )
        self.run()
        for fact in self.facts.items():
            print(fact)
            
        for fact in self.facts.values():
            if 'jenis_kalimat' in fact:
                return fact['jenis_kalimat']
        return 'TIDAKTERDEFINISI'