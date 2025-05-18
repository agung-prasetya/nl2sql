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
        OR(
            Fact(kalimat=MATCH.kalimat_ternormalisasi, ternormalisasi=True), 
            Fact(kalimat=MATCH.kalimat_terstemming, terstemming=True)
        ),
        salience=290
    )    
    def rule_penambahan_fact_kata(self, kalimat_ternormalisasi, kalimat_terstemming):
        daftar_kata_kalimat_ternormalisasi = kalimat_ternormalisasi.split()
        for id, kata in daftar_kata_kalimat_ternormalisasi:
            self.declare(Fact(kata=kata, posisi=id))
            
        daftar_kata_kalimat_terstemming = kalimat_terstemming.split()
        for id, kata in daftar_kata_kalimat_terstemming:
            if kata not in daftar_kata_kalimat_ternormalisasi:
                self.declare(Fact(kata=kata, posisi=id))
        
        
        
    #Urutan 2 - identifikasi apakah DDL - CREATE DATABASE nama_database
    #Kalimat yang teridentifikasi DDL - CREARE DATABASE sudah bisa disimpulkan kalimat TERDEFINISI
    @Rule(
        AND(
            Fact(kata='buat', posisi=MATCH.posisi1),
            OR(
                AND(
                    Fact(kata='basis', posisi=MATCH.posisi2), 
                    Fact(kata='data', posisi=MATCH.posisi3),
                    TEST(lambda posisi1,posisi2,posisi3: posisi1<posisi2 and posisi2==posisi3-1)
                ),
                AND(
                    Fact(kata='database', posisi=MATCH.posisi3),
                    TEST(lambda posisi1,posisi3: posisi1<posisi3)
                )
            ),
            Fact(kata=MATCH.kata, posisi=MATCH.posisi2)
            
        ),
        salience=285
    )
    def rule_identifikasi_apakah_ddl(self):
        self.declare(Fact(jenis_kalimat='TERDEFINISI'))
    
        
        
        
    #Urutan 2 - identifikasi apakah DML
    
    
    
        
        
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