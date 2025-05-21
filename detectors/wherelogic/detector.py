from experta import *
import json
import re

class WherelogicDetector(KnowledgeEngine):
    @Rule(
        AS.fact_kalimat_tak_ternormalisasi << Fact(kalimat=MATCH.kalimat, ternormalisasi=False), 
        salience=500
    )    
    def rule_penambahan_fact_kalimat_ternormalisasi(self, fact_kalimat_tak_ternormalisasi):
        kalimat_ternormalisasi = fact_kalimat_tak_ternormalisasi['kalimat'].lower().strip()
        kalimat_ternormalisasi = re.sub(r'\s+', ' ', kalimat_ternormalisasi).strip()
        kalimat_ternormalisasi = re.sub(r'[.,\'"\/\\\)\\(;:]','',kalimat_ternormalisasi)
        
        self.modify(fact_kalimat_tak_ternormalisasi, kalimat=kalimat_ternormalisasi, ternormalisasi=True)
        
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
            if 'jenis_operator_logika' in fact:
                return fact['jenis_operator_logika']
        return 'NOOPR'
    
    
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