from experta import *
import json
import re
import textdistance

class DMLDetector(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(jenis_dml='NODML')

    @Rule(
        OR(
            Fact(kata='tambahkan'),Fact(kata='baru')
        )
    )
    def db_inventori_1_INSERT_1(self):
        self.declare(Fact(jenis_dml='INSERT'))

    @Rule(
        OR(
            Fact(kata='masukkan'),
            Fact(kata='baru')
        )
    )
    def db_inventori_1_INSERT_2(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        OR(
            Fact(kata='simpan'),
            Fact(kata='baru')
        )
    )
    def db_inventori_1_INSERT_3(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        OR(
            Fact(kata='catat'),
            Fact(kata='baru')
        )
    )
    def db_inventori_2_INSERT_1(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        OR(
            Fact(kata='daftarkan'),
            Fact(kata='baru')
        )
    )
    def db_inventori_2_INSERT_2(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        AND(
            
            Fact(kata='rekam')
        )
    )
    def db_inventori_2_INSERT_3(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        OR(
            Fact(kata='inputkan'),
            Fact(kata='baru')
        )
    )
    def db_inventori_3_INSERT_1(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        OR(
            Fact(kata='buat'),
            Fact(kata='baru')
        )
    )
    def db_hotel_1_INSERT_1(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    @Rule(
        OR(
            Fact(kata='sisipkan'),
            Fact(kata='baru')
        )
    )
    def db_akuntansi_1_INSERT_1(self):
        self.declare(Fact(jenis_dml='INSERT'))
        
    # SELECT
    @Rule(
        AND(
            
            Fact(kata='tampilkan'),
        )
    )
    def db_inventori_1_SELECT_1(self):
        self.declare(Fact(jenis_dml='SELECT'))
        
    @Rule(
        AND(
            
            Fact(kata='cari')
        )
    )
    def db_inventori_1_SELECT_2(self):
        self.declare(Fact(jenis_dml='SELECT'))
        
    @Rule(
        AND(
            
            Fact(kata='ambil')
        )
    )
    def db_inventori_1_SELECT_3(self):
        self.declare(Fact(jenis_dml='SELECT'))
        
    @Rule(
        AND(
            
            Fact(kata='lihat')
        )
    )
    def db_inventori_1_SELECT_4(self):
        self.declare(Fact(jenis_dml='SELECT'))
        
    @Rule(
        AND(
            
            Fact(kata='periksa'),
            Fact(kata='diambil')
        )
    )
    def db_kepegawaian_1_SELECT_1(self):
        self.declare(Fact(jenis_dml='SELECT'))
        
    @Rule(
        AND(
            
            Fact(kata='pilih'),
        )
    )
    def db_akuntansi_2_SELECT_1(self):
        self.declare(Fact(jenis_dml='SELECT'))
        
    # UPDATE
    @Rule(
        AND(
            
            Fact(kata='perbarui'),
        )
    )
    def db_inventori_1_UPDATE_1(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='ubah'),
        )
    )
    def db_inventori_1_UPDATE_2(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='ubah'),
            Fact(kata='baru'),
        )
    )
    def db_pemesanan_dan_penjualan_1_UPDATE_1(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='edit'),
        )
    )
    def db_inventori_1_UPDATE_3(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='edit'),
            Fact(kata='baru'),
        )
    )
    def db_inventori_2_UPDATE_1(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='atur'),
        )
    )
    def db_inventori_1_UPDATE_4(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='sesuaikan'),
        )
    )
    def db_inventori_1_UPDATE_5(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='ganti'),
        )
    )
    def db_inventori_1_UPDATE_6(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    @Rule(
        AND(
            
            Fact(kata='update'),
        )
    )
    def db_akuntansi_1_UPDATE_1(self):
        self.declare(Fact(jenis_dml='UPDATE'))
        
    # DELETE
    @Rule(
        AND(
            
            Fact(kata='hapus'),
        )
    )
    def db_inventori_1_DELETE_1(self):
        self.declare(Fact(jenis_dml='DELETE'))
        
    @Rule(
        AND(
            
            Fact(kata='buang'),
        )
    )
    def db_inventori_1_DELETE_2(self):
        self.declare(Fact(jenis_dml='DELETE'))
        
    @Rule(
        AND(
            
            Fact(kata='hilangkan'),
        )
    )
    def db_inventori_1_DELETE_3(self):
        self.declare(Fact(jenis_dml='DELETE'))
        
    @Rule(
        AND(
            
            Fact(kata='singkirkan'),
        )
    )
    def db_inventori_1_DELETE_4(self):
        self.declare(Fact(jenis_dml='DELETE'))
        
    @Rule(
        AND(
            
            Fact(kata='musnahkan'),
        )
    )
    def db_inventori_3_DELETE_1(self):
        self.declare(Fact(jenis_dml='DELETE'))
        
    @Rule(
        AND(
            
            Fact(kata='delete'),
        )
    )
    def db_akuntansi_2_DELETE_1(self):
        self.declare(Fact(jenis_dml='DELETE'))

    @Rule(
        OR(
            Fact(jenis_dml='SELECT'), Fact(jenis_dml='INSERT'), Fact(jenis_dml='UPDATE'), Fact(jenis_dml='DELETE')
        )
    )
    def rule_remove_nodml_if_dml_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_dml' in fact and fact['jenis_dml']=='NODML':
                self.retract(id)

    
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
        daftar_kata = [fact['kata'] for _,fact in self.facts.items() 
                       if isinstance(fact, Fact) and 'kata' in fact]
        daftar_tabel = [fact['tabel'] for _,fact in self.facts.items() 
                        if isinstance(fact, Fact) and 'tabel' in fact]
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
    

    def detect(self, kalimat, file_database_json):
        with open(file_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(Fact(kalimat=kalimat), Fact(database=database))
        self.run()

        for fact in self.facts.values():
            if 'jenis_dml' in fact:
                return fact['jenis_dml']
        return 'NODML'