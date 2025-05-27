from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class SketchDetector(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        
        
    @Rule(
        AS.fact_kalimat_tak_ternormalisasi << Fact(kalimat=MATCH.kalimat, ternormalisasi=False), 
        salience=700
    )    
    def rule_penambahan_fact_kalimat_ternormalisasi(self, fact_kalimat_tak_ternormalisasi):
        kalimat_ternormalisasi = fact_kalimat_tak_ternormalisasi['kalimat'].lower().strip()
        kalimat_ternormalisasi = re.sub(r'\s+', ' ', kalimat_ternormalisasi).strip()
        kalimat_ternormalisasi = re.sub(r'[.,\'"\/\\\)\\(;:]','',kalimat_ternormalisasi)
        
        self.modify(fact_kalimat_tak_ternormalisasi, kalimat=kalimat_ternormalisasi, ternormalisasi=True)
        
    
    #Urutan 2 - penambahan kalimat ter-stemming
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=True), 
        salience=600
    )    
    def rule_penambahan_fact_kalimat_terstemming(self, kalimat):
        kalimat_terstemming = self.stemmer.stem(kalimat)
        self.declare(Fact(kalimat=kalimat_terstemming, terstemming=True))
           
        
        
    #Urutan 3 - penambahan fact frase dari kedua kalimat ternormalisasi dan terstemming
    @Rule(
        AND(
            Fact(kalimat=MATCH.kalimat_ternormalisasi, ternormalisasi=True), 
            Fact(kalimat=MATCH.kalimat_terstemming, terstemming=True)
        ),
        salience=595
    )    
    def rule_penambahan_fact_frase(self, kalimat_ternormalisasi, kalimat_terstemming):
        daftar_frase_ternormalisasi = self.get_frase(kalimat=kalimat_ternormalisasi)
        for frase in daftar_frase_ternormalisasi:
            self.declare(Fact(frase=frase['frase']))
            
        daftar_frase_terstemming = self.get_frase(kalimat=kalimat_terstemming)
        for frase in daftar_frase_terstemming:
            if not any(item for item in daftar_frase_ternormalisasi if item['frase']==frase['frase']):
                self.declare(Fact(frase=frase['frase']))
                
                
    #Ekstraksi database - tabel - kolom menjadi bagian dari fact tabel
    @Rule(
        AS.fact_database << Fact(database=MATCH.database), 
        salience=595
    )
    def rule_ekstraksi_tabel_kolom(self, fact_database):
        self.declare(Fact(database=fact_database['database']))
        for tabel in fact_database['database']['entitas']:
            for kolom in fact_database['database']['entitas'][tabel]:
                self.declare(Fact(tabel=tabel.replace('_',' '), kolom=kolom.replace('_',' ')))
        self.retract(fact_database)
        
    
    
    #Identifikasi frase yang merujuk pada nama tabel
    @Rule(
        AND(
            Fact(tabel=MATCH.tabel),
            AS.fact_frase << Fact(frase=MATCH.frase),
            TEST(lambda fact_frase: 'adalah_nama_tabel' not in fact_frase),
            TEST(lambda frase, tabel: frase == tabel)
        ),
        salience=595
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
            TEST(lambda frase_kolom, kolom: frase_kolom == kolom)
        ),
        salience=590
    )
    def rule_identifikasi_nama_kolom(self,fact_kolom):
        self.modify(fact_kolom, adalah_nama_kolom=True)
        

    
    #Urutan 5 - Identifikasi SELECT
    @Rule(
        AND(
            AS.fact_frase << Fact(frase=MATCH.frase),
            TEST(lambda fact_frase: 'apakah_select' not in fact_frase),
            TEST(lambda frase: frase in ['tampil','lihat','tunjuk','ambil','cari', 'dapat', 'hitung'])
        ),
        salience=475
    )
    def rule_identifikasi_frase_yang_merujuk_select(self, fact_frase):
        self.modify(fact_frase, apakah_select=True)
        
        
    #Urutan 5 - Identifikasi * (semua kolom)
    @Rule(
        AND(
            AS.fact_frase << Fact(frase=MATCH.frase),
            TEST(lambda fact_frase: 'apakah_semua_kolom' not in fact_frase),
            TEST(lambda frase: frase in ['semua', 'seluruh', 'lengkap', 'data'])
        ),
        salience=475
    )
    def rule_identifikasi_frase_yang_merujuk_semua_kolom(self, fact_frase):
        self.modify(fact_frase, apakah_semua_kolom=True)
        
        
    #Urutan 5 - Identifikasi GROUP BY
    @Rule(
    AND(
        AS.fact_frase << Fact(frase=MATCH.frase),
        TEST(lambda fact_frase: 'apakah_group_by' not in fact_frase),
        TEST(lambda frase: frase in ['group', 'dasar', 'tiap', 'setiap', 'masing-masing', 'per'])
    ),
    salience=475
    )
    def rule_identifikasi_group_by(self, fact_frase):
        self.modify(fact_frase, apakah_group_by=True)
        
    
    #Urutan 5 - Identifikasi CONDITION
    @Rule(
        AND(
            AS.fact_frase << Fact(frase=MATCH.frase),
            TEST(lambda fact_frase: 'apakah_condition' not in fact_frase),
            TEST(lambda frase: frase in ['yang', 'pada', 'dimana', 'dengan', 'untuk', 'lebih dari',
                                         'diatas','=','lebih besar dari','kurang dari',])
        ),
        salience=475
    )
    def rule_identifikasi_frase_yang_merujuk_condition(self, fact_frase):
        self.modify(fact_frase, apakah_condition=True)
        
    
    #Urutan 5 - Identifikasi fungsi aggregasi
    @Rule(
        AND(
            AS.fact_frase << Fact(frase=MATCH.frase),
            TEST(lambda fact_frase: 'apakah_agg' not in fact_frase),
            TEST(lambda frase: frase in ['jumlah', 'rata', 'maksimum', 'minimum', 'total', 'tinggi', 'rendah'])
        ),
        salience=475
    )
    def rule_identifikasi_frase_agregasi(self, fact_frase):
        self.modify(fact_frase, apakah_agg=True)


    #------------------------------------IDENTIFIKASI SKETCH--------------------------------------#

    #SELECT $AGG $COLUMN FROM $TABLE GROUP BY $COLUMN HAVING $CONDITION
    @Rule(
        AND(
            Fact(apakah_select=True),
            Fact(apakah_agg=True),
            Fact(adalah_nama_tabel=True),
            Fact(apakah_group_by=True),
            Fact(adalah_nama_kolom=True),
            Fact(apakah_condition=True)
        ),
        salience=470
    )
    def rule_identifikasi_sketsa_1(self):
        self.declare(Fact(jenis_sketsa="SELECT $AGG $COLUMN FROM $TABLE GROUP BY $COLUMN HAVING $CONDITION"))
        
    
    #SELECT $AGG $COLUMN FROM $TABLE
    @Rule(
    AND(
        Fact(apakah_select=True),
        Fact(apakah_agg=True),
        Fact(adalah_nama_tabel=True),
        Fact(adalah_nama_kolom=True)
    ),
    salience=465
    )
    def rule_identifikasi_sketsa_2(self):
        self.declare(Fact(jenis_sketsa="SELECT $AGG $COLUMN FROM $TABLE"))
        
    
    #SELECT $COLUMN FROM $TABLE WHERE $CONDITION
    @Rule(
        AND(
            Fact(apakah_select=True),
            Fact(adalah_nama_kolom=True),
            Fact(adalah_nama_tabel=True),
            Fact(apakah_condition=True)
        ),
        salience=460
    )
    def rule_identifikasi_sketsa_3(self):
        self.declare(Fact(jenis_sketsa="SELECT $COLUMN FROM $TABLE WHERE $CONDITION"))
    
    
    #SELECT $COLUMN FROM $TABLE
    @Rule(
        AND(
            Fact(apakah_select=True),
            Fact(adalah_nama_kolom=True),
            Fact(adalah_nama_tabel=True)
        ),
        salience=455
    )
    def rule_identifikasi_sketsa_4(self):
        self.declare(Fact(jenis_sketsa="SELECT $COLUMN FROM $TABLE"))
        
    
    #SELECT * FROM $TABLE WHERE $CONDITION
    @Rule(
        AND(
            Fact(apakah_select=True),
            Fact(apakah_semua_kolom=True),
            Fact(adalah_nama_tabel=True),
            Fact(apakah_condition=True)
        ),
        salience=450
    )
    def rule_identifikasi_sketsa_5(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE WHERE $CONDITION"))
        
    
    #SELECT * FROM $TABLE
    @Rule(
        AND(
            Fact(apakah_select=True),
            Fact(apakah_semua_kolom=True),
            Fact(adalah_nama_tabel=True)
        )    
    )
    def rule_identifikasi_sketsa_6(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE"))




        
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