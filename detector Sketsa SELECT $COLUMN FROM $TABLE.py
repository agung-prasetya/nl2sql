from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class SketchDetector(KnowledgeEngine):
    #Urutan 1
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=False),
        salience=500
    )
    def rule_normalisasi_kalimat(self, fact_kalimat, kalimat):
        kalimat_ternormalisasi = kalimat.lower()
        kalimat_ternormalisasi = re.sub(r'[.,]$','',kalimat_ternormalisasi)
        
        self.modify(fact_kalimat, kalimat=kalimat_ternormalisasi, ternormalisasi=True)
    
    
    #Urutan 2
    @Rule(
        Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
        salience=495
    )
    def rule_stemming_kalimat(self, kalimat):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        kalimat_stemming = stemmer.stem(kalimat)
        
        self.declare(Fact(kalimat=kalimat_stemming, terstemming=True))
    
    
    #Urutan 3
    @Rule(
        AND(
            Fact(kalimat=MATCH.kalimat1, ternormalisasi=True),
            Fact(kalimat=MATCH.kalimat2, terstemming=True)
        ),
        salience=490
    )
    def rule_ekstraksi_kata(self, kalimat1, kalimat2):
        daftar_kata_kalimat_ternormalisasi = kalimat1.split()
        for id, kata in enumerate(daftar_kata_kalimat_ternormalisasi):
            self.declare(Fact(kata=kata, posisi=id))
            
        daftar_kata_kalimat_terstemming = kalimat2.split()
        for id, kata in enumerate(daftar_kata_kalimat_terstemming):
            if kata not in daftar_kata_kalimat_ternormalisasi:
                self.declare(Fact(kata=kata, posisi=id))
                
    
    #Urutan 4
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_nama_tabel' not in fact_kata),
            Fact(database=MATCH.database),
            TEST(lambda kata, database: any(nama_tabel for nama_tabel in database['entitas'] if nama_tabel in kata))
        ),
        salience=485
    )
    def rule_identifikasi_kata_yang_merujuk_nama_tabel(self, fact_kata):
        self.modify(fact_kata, apakah_nama_tabel=True)


    # Sketsa SELECT $COLUMN FROM $TABLE
    @Rule(
    AND(
        AS.fact_kata << Fact(kata=MATCH.kata),
        TEST(lambda fact_kata: 'apakah_nama_kolom' not in fact_kata),
        Fact(database=MATCH.database),
        Fact(kata_nama_tabel=MATCH.nama_tabel),
        TEST(lambda kata, database, nama_tabel: 
            nama_tabel in database['entitas'] and kata in database['entitas'][nama_tabel].keys())
    ),
    salience=485
    )
    def rule_identifikasi_kata_yang_merujuk_nama_kolom(self, fact_kata):
        self.modify(fact_kata, apakah_nama_kolom=True)



    #Deteksi frase
    
    #Urutan 5
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_select' not in fact_kata),
            TEST(lambda kata: kata in ['tampil','lihat','tunjuk','ambil','cari','dapat'])
        ),
        salience=480
    )
    def rule_identifikasi_kata_yang_merujuk_select(self, fact_kata):
        self.modify(fact_kata, apakah_select=True)
        
        
    #Urutan 5
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_semua_kolom' not in fact_kata),
            TEST(lambda kata: kata in ['semua', 'seluruh', 'lengkap', 'data'])
        ),
        salience=480
    )
    def rule_identifikasi_kata_yang_merujuk_semua_kolom(self, fact_kata):
        self.modify(fact_kata, apakah_semua_kolom=True)

    # Sketsa SELECT * FROM $TABLE WHERE $CONDITION
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_condition' not in fact_kata),
            TEST(lambda kata: kata in ['yang', 'pada', 'dimana', 'dengan', 'untuk'])
        ),
        salience=480
    )
    def rule_identifikasi_kata_condition(self, fact_kata):
        self.modify(fact_kata, apakah_condition=True)

    # Sketsa SELECT $COLUMN FROM $TABLE
    @Rule(
    AND(
        AS.fact_kata << Fact(kata=MATCH.kata),
        TEST(lambda fact_kata: 'apakah_nama_tabel' not in fact_kata),
        Fact(database=MATCH.database),
        TEST(lambda kata, database: kata in database['entitas'])
    ),
    salience=485
    )
    def rule_identifikasi_kata_yang_merujuk_nama_tabel(self, fact_kata):
        self.modify(fact_kata, apakah_nama_tabel=True)
        self.declare(Fact(kata_nama_tabel=fact_kata['kata']))

    
    
    # Sketsa SELECT * FROM $TABLE WHERE $CONDITION
    @Rule(
        AND(
            Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, apakah_select=True),
            Fact(kata=MATCH.kata2, posisi=MATCH.posisi2, apakah_semua_kolom=True),
            Fact(kata=MATCH.kata3, posisi=MATCH.posisi3, apakah_nama_tabel=True),
            Fact(kata=MATCH.kata4, posisi=MATCH.posisi4, apakah_condition=True),
            TEST(lambda posisi1, posisi2, posisi3, posisi4: posisi1 < posisi2 < posisi3 < posisi4)
        ),
        salience=476
    )
    def rule_identifikasi_sketsa_2(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE WHERE $CONDITION"))


    #Urutan 5
    @Rule(
        AND(
            Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, apakah_select=True),
            Fact(kata=MATCH.kata2, posisi=MATCH.posisi2, apakah_semua_kolom=True),
            Fact(kata=MATCH.kata3, posisi=MATCH.posisi3, apakah_nama_tabel=True),
            TEST(lambda posisi1,posisi2,posisi3: posisi1<posisi2<posisi3)
        ),
        salience=475
    )
    def rule_identifikasi_sketsa_1(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE"))

    
    # Sketsa SELECT $COLUMN FROM $TABLE
    @Rule(
        AND(
            Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, apakah_select=True),
            Fact(kata=MATCH.kata2, posisi=MATCH.posisi2, apakah_nama_kolom=True),
            Fact(kata=MATCH.kata3, posisi=MATCH.posisi3, apakah_nama_tabel=True),
            TEST(lambda posisi1, posisi2, posisi3: posisi1 < posisi2 < posisi3)
        ),
        salience=477
    )
    def rule_sketsa_select_kolom(self):
        self.declare(Fact(jenis_sketsa="SELECT $COLUMN FROM $TABLE"))
        
        
        
    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(Fact(kalimat=kalimat, ternormalisasi=False), Fact(database=database))
        self.run()

        for fact in self.facts.values():
            if 'jenis_sketsa' in fact:
                return fact['jenis_sketsa']
        return 'NOSKETCH'