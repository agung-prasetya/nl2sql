from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class JoinDetector(KnowledgeEngine):
    #Urutan 1
    #Rule ini mengubah kalimat yang tak ternormalisasi ke normalisasi.
    #Rule ini dieksekusi yang paling awal karena input paling awal agar sistem ini bekerja adalah dengan adanya kalimat ternormalisasi.
    #Kalimat ternormalisasi dalam konteks ini adalah sebuah kalimat yang penulisanya terstandar, yaitu 
    # semua huruf adalah huruf kecil, tidak ada tanda baca seperti .,'"/\, jumlah spasi adalah 1 untuk pemisah antar kata
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
        
        
        
            
    #Urutan 3 - penambahan fact frase 
    #Urutan rule ini harus dibawah urutan rule_cek_kecocokan_domain agar tidak dieksekusi 
    # sebelum adanya kepastian bahwa domain cocok.
    #Sebuah kata dianggap sebagai frase.
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
        salience=290
    )
    def rule_penambahan_fact_frase(self, fact_kalimat):
        daftar_kata = fact_kalimat['kalimat'].split()
        jumlah_kata = len(daftar_kata)
        for kelompok_frase in range(1, jumlah_kata+1):
            for posisi_kata in range(jumlah_kata+1-kelompok_frase):
                frase = []
                for bagian in range(kelompok_frase):
                    frase.append(daftar_kata[posisi_kata + bagian])
                
                fact_frase = Fact(
                    frase=' '.join(frase), posisi_awal=posisi_kata, posisi_akhir=posisi_kata+kelompok_frase-1, 
                    terperiksa=False, adalah_nama_tabel=False
                )
                
                self.declare(fact_frase)
        
        self.retract(fact_kalimat)
        
    
    
    #Urutan 3 - penambahan fact tabel
    #Rule ini dapat dikerjakan secara bersamaan dengan rule_penambahan_fact_kata
    # karena tidak mungkin terjadi konflik.
    #Rule ini juga akan menghapus fact database karena sudah tidak diperlukan.
    @Rule(
        AS.fact_database << Fact(database=MATCH.database),
        salience=290
    )
    def rule_penambahan_fact_tabel(self, fact_database, database):
        for tabel in database['entitas']:
            self.declare(Fact(tabel=tabel.replace('_',' ')))
            
        self.retract(fact_database)
        
        
        
        
    #Urutan 4 - identifikasi frase yang merujuk nama tabel
    #Rule ini pada prinsipnya menandai apakah fact frase merujuk pada nama tabel.
    @Rule(
        AND(            
            AS.fact_frase << Fact(frase=MATCH.frase, terperiksa=False, adalah_nama_tabel=False),
            Fact(tabel=MATCH.tabel),
            TEST(lambda tabel,frase:tabel==frase)
        ),
        salience=285
    )
    def rule_identifikasi_frase_yang_merupakan_nama_tabel(self, fact_frase):
        self.modify(fact_frase, terperiksa=True, adalah_nama_tabel=True)
        
    
    
    #Urutan terakhir - 
    @Rule(
        AND(
            AS.fact_frase1 << Fact(frase=MATCH.frase1),
            TEST(lambda frase1: frase1 in ['semua pasangan','semua kombinasi','semua kemungkinan','kemunginan kombinasi',
                                         'semua potensi pasangan','semua pasangan']),
            AS.fact_tabel1 << Fact(frase=MATCH.frase_tabel1, adalah_nama_tabel=True),
            AS.fact_frase2 << Fact(frase=MATCH.frase2),
            TEST(lambda frase2: frase2 in ['dan','dengan']),
            AS.fact_tabel2 << Fact(frase=MATCH.frase_tabel2, adalah_nama_tabel=True),
            TEST(lambda fact_frase1,fact_tabel1,fact_frase2,fact_tabel2: 
                            fact_frase1['posisi_akhir'] < fact_tabel1['posisi_awal'] and 
                            fact_tabel1['posisi_akhir'] < fact_frase2['posisi_awal'] and
                            fact_frase2['posisi_akhir'] < fact_tabel2['posisi_awal']
            ),
        ),
        salience=100
    )
    def rule_identifikasi_cross_join(self):
        self.declare(Fact(jenis_join='CROSSJOIN'))
        self.halt()
        
    
    
    
    @Rule(
        AND(
            AS.fact_frase1 << Fact(frase=MATCH.frase1),
            TEST(lambda frase1: frase1 in ['semua','seluruh']),
            AS.fact_tabel1 << Fact(frase=MATCH.frase_tabel1, adalah_nama_tabel=True),
            AS.fact_frase2 << Fact(frase=MATCH.frase2),
            TEST(lambda frase2: frase2 in ['beserta','berikut','dan']),
            AS.fact_tabel2 << Fact(frase=MATCH.frase_tabel2, adalah_nama_tabel=True),
            AS.fact_frase3 << Fact(frase=MATCH.frase3),
            TEST(lambda frase3: frase3 in ['ada','tersedia','memiliki']),
            TEST(lambda fact_frase1,fact_tabel1,fact_frase2,fact_tabel2, fact_frase3: 
                            fact_frase1['posisi_akhir'] < fact_tabel1['posisi_awal'] and 
                            fact_tabel1['posisi_akhir'] < fact_frase2['posisi_awal'] and
                            fact_frase2['posisi_akhir'] < fact_tabel2['posisi_awal'] and
                            fact_tabel2['posisi_akhir'] < fact_frase3['posisi_awal']
            ),
        ),
        salience=100
    )
    def rule_identifikasi_left_join(self):
        self.declare(Fact(jenis_join='LEFTJOIN'))
        self.halt()
        

    
    @Rule(
        AND(
            AS.fact_tabel1 << Fact(frase=MATCH.frase_tabel1, adalah_nama_tabel=True),
            AS.fact_frase2 << Fact(frase=MATCH.frase2),
            TEST(lambda frase2: any([
                frase for frase in ['lengkap dengan','yang sudah','yang sedang',
                                    'yang memiliki','yang telah', 'yang diambil',
                                    'yang terlibat dalam', 'yang punya','yang pernah']
                if frase in frase2
                ])
            ),
            AS.fact_tabel2 << Fact(frase=MATCH.frase_tabel2, adalah_nama_tabel=True),
            TEST(lambda fact_tabel1,fact_frase2,fact_tabel2: 
                            fact_tabel1['posisi_akhir'] < fact_frase2['posisi_awal'] and
                            fact_frase2['posisi_akhir'] < fact_tabel2['posisi_awal']
            )
        ),
        salience=50
    )
    def rule_identifikasi_inner_join(self):
        self.declare(Fact(jenis_join='INNERJOIN'))
        self.halt()
        
        
        

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
            if 'jenis_join' in fact:
                return fact['jenis_join']
        return 'NOJOIN'