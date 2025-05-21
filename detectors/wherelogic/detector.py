from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class WherelogicDetector(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        
        
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
        salience=500
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
    
    
    
    #Identifikasi frase yang merujuk pada OPERATOR 
    @Rule(
        AND(
            AS.fact_operator << Fact(frase=MATCH.frase),
            TEST(lambda fact_operator: 'adalah_operator' not in fact_operator),
            TEST(lambda frase: frase in ['lebih dari', 'kurang dari',' di atas','di bawah','kandung','yang','dengan']
            ),
        ),
        salience=460
    )
    def rule_identifikasi_operator(self,fact_operator):
        self.modify(fact_operator, adalah_operator=True)
        
        
    
    #-------------------------------------------------AND----------------------------------------------------------------
    
    
    
    #Identifikasi AND
    #Pola 1: [table] ... [kolom][operator]...AND...[kolom][operator]...
    @Rule(
        AND(
            AS.fact_table << Fact(frase=MATCH.tabel, adalah_nama_tabel=True),
            AS.fact_kolom1 << Fact(frase=MATCH.kolom1, adalah_nama_kolom=True),
            AS.fact_operator1 << Fact(frase=MATCH.operator1, adalah_operator=True),
            AS.fact_dan << Fact(frase='dan'),
            AS.fact_kolom2 << Fact(frase=MATCH.kolom2, adalah_nama_kolom=True),
            AS.fact_operator2 << Fact(frase=MATCH.operator2, adalah_operator=True),
            TEST(lambda fact_table, fact_kolom1, fact_operator1, fact_dan, fact_kolom2, fact_operator2:
                            fact_table['posisi_akhir'] < fact_kolom1['posisi_awal'] and 
                            fact_kolom1['posisi_akhir'] < fact_operator1['posisi_awal'] and 
                            fact_operator1['posisi_akhir'] < fact_dan['posisi_awal'] and 
                            fact_dan['posisi_akhir'] < fact_kolom2['posisi_awal'] and 
                            fact_kolom2['posisi_akhir'] < fact_operator2['posisi_awal']
            )
        ),
        salience=300
    )
    def rule_identifikasi_and_pola1(self):
        self.declare(Fact(jenis_operator_logika='AND'))
    
        
    
    #Identifikasi AND
    #Pola 2: [table] AND...[kolom][operator]...
    @Rule(
        AND(
            AS.fact_table << Fact(frase=MATCH.tabel, adalah_nama_tabel=True),
            AS.fact_dan << Fact(frase='dan'),
            AS.fact_kolom1 << Fact(frase=MATCH.kolom1, adalah_nama_kolom=True),
            AS.fact_operator1 << Fact(frase=MATCH.operator1, adalah_operator=True),
            TEST(lambda fact_table, fact_dan, fact_kolom1, fact_operator1:
                            fact_table['posisi_akhir'] < fact_kolom1['posisi_awal'] and 
                            fact_dan['posisi_akhir'] < fact_kolom1['posisi_awal'] and 
                            fact_kolom1['posisi_akhir'] < fact_operator1['posisi_awal']
            )
        ),
        salience=295
    )
    def rule_identifikasi_and_pola2(self):
        self.declare(Fact(jenis_operator_logika='AND'))
    
    
    #++++++++++++++++++++++++++++++++++++++++++++OR+++++++++++++++++++++++++++++++++++++++++++++++++++
    
    #Identifikasi OR
    #Pola 1: [table] ... [kolom][operator]...OR...[kolom][operator]...
    @Rule(
        AND(
            AS.fact_table << Fact(frase=MATCH.tabel, adalah_nama_tabel=True),
            AS.fact_kolom1 << Fact(frase=MATCH.kolom1, adalah_nama_kolom=True),
            AS.fact_operator1 << Fact(frase=MATCH.operator1, adalah_operator=True),
            AS.fact_atau << Fact(frase='atau'),
            AS.fact_kolom2 << Fact(frase=MATCH.kolom2, adalah_nama_kolom=True),
            AS.fact_operator2 << Fact(frase=MATCH.operator2, adalah_operator=True),
            TEST(lambda fact_table, fact_kolom1, fact_operator1, fact_atau, fact_kolom2, fact_operator2:
                            fact_table['posisi_akhir'] < fact_kolom1['posisi_awal'] and 
                            fact_kolom1['posisi_akhir'] < fact_operator1['posisi_awal'] and 
                            fact_operator1['posisi_akhir'] < fact_atau['posisi_awal'] and 
                            fact_atau['posisi_akhir'] < fact_kolom2['posisi_awal'] and 
                            fact_kolom2['posisi_akhir'] < fact_operator2['posisi_awal']
            )
        ),
        salience=300
    )
    def rule_identifikasi_or_pola1(self):
        self.declare(Fact(jenis_operator_logika='OR'))
        
    
    #Identifikasi OR
    #Pola 2: [table] OR...[kolom][operator]...
    @Rule(
        AND(
            AS.fact_table << Fact(frase=MATCH.tabel, adalah_nama_tabel=True),
            AS.fact_atau << Fact(frase='atau'),
            AS.fact_kolom1 << Fact(frase=MATCH.kolom1, adalah_nama_kolom=True),
            AS.fact_operator1 << Fact(frase=MATCH.operator1, adalah_operator=True),
            TEST(lambda fact_table, fact_atau, fact_kolom1, fact_operator1:
                            fact_table['posisi_akhir'] < fact_kolom1['posisi_awal'] and 
                            fact_atau['posisi_akhir'] < fact_kolom1['posisi_awal'] and 
                            fact_kolom1['posisi_akhir'] < fact_operator1['posisi_awal']
            )
        ),
        salience=295
    )
    def rule_identifikasi_or_pola2(self):
        self.declare(Fact(jenis_operator_logika='OR'))
        

    #++++++++++++++++++++++++++++++++++++++++++++NOT+++++++++++++++++++++++++++++++++++++++++++++++++++
    #Identifikasi NOT
    #Pola 1: [table] NOT [kolom]
    @Rule(
        AND(
            Fact(frase=MATCH.tabel, adalah_nama_tabel=True),
            Fact(frase=MATCH.kolom, adalah_nama_kolom=True),
            Fact(frase=MATCH.frase),
            TEST(lambda frase: frase in ['tidak','bukan','selain'])
        ),
        salience=290
    )
    def rule_identifikasi_not_pola1(self):
        self.declare(Fact(jenis_operator_logika='NOT'))
        
        
        
    
    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(
            Fact(kalimat=kalimat, ternormalisasi=False), 
            Fact(database=database)
        )
        self.run()
        
        # for fact in self.facts.items():
        #     print(fact)
        
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