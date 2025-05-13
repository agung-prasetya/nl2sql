from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class DDLDetector(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(jenis_ddl='NODDL')

    #Truncate
    #1
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='tanpa'),Fact(kata='tabel')
            )
        )
    def truncate_1(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #2
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='seluruh'),Fact(kata='tahan'),Fact(kata='tabel')
            )
        )
    def truncate_2(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #3
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='semua'),Fact(kata='data'),Fact(kata='tabel')
            )
        )
    def truncate_3(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
        
    #4
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='seluruh'),Fact(kata='data'),Fact(kata='tabel')
            )
        )
    def truncate_4(self):
        self.declare(Fact(jenis_ddl='TRUNCATE')) 
    
    #5
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='data'),Fact(kata='tabel'),Fact(kata='truncate')
            )
        )
    def truncate_5(self):
        self.declare(Fact(jenis_ddl='TRUNCATE')) 
    
    #6
    @Rule(
        AND(
            Fact(kata='kosong'),Fact(kata='tabel')
            )
        )
    def truncate_6(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #7
    @Rule(
        AND(
            Fact(kata='bersih'),Fact(kata='tabel')
            )
        )
    def truncate_7(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #8
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='seluruh'),Fact(kata='isi'),
            Fact(kata='tabel'),
            )
        )
    def truncate_8(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #9
    @Rule(
        AND(
            Fact(kata='truncate')
            )
        )
    def truncate_9(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #10
    @Rule(
        AND(
            Fact(kata='buang'),Fact(kata='semua'),Fact(kata='baris'),
            Fact(kata='tabel'),
            )
        )
    def truncate_10(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #11
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='isi'),Fact(kata='tabel'),
            )
        )
    def truncate_11(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #12
    @Rule(
        AND(
            Fact(kata='reset'),Fact(kata='tabel'),
            )
        )
    def truncate_12(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #13
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='semua'),Fact(kata='entri'),
            Fact(kata='tabel'),
            )
        )
    def truncate_13(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #14
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='semua'),Fact(kata='baris'),
            Fact(kata='tabel'),
            )
        )
    def truncate_14(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #15
    @Rule(
        AND(
            Fact(kata='bersih'),Fact(kata='tabel'),
            )
        )
    def truncate_15(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #16
    @Rule(
        AND(
            Fact(kata='buang'),Fact(kata='isi'),Fact(kata='tabel'),
            )
        )
    def truncate_16(self):
        self.declare(Fact(jenis_ddl='TRUNCATE'))
    
    #DROP
    #1
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='tabel'),
            )
        )
    def drop_1(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #2
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='kolom'),
            )
        )
    def drop_2(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #3
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='constraint'),
            )
        )
    def drop_3(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #4
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='indeks'),
            )
        )
    def drop_4(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #5
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='database'),
            )
        )
    def drop_3(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #6
    @Rule(
        AND(
            Fact(kata='drop'),Fact(kata='tabel'),
            )
        )
    def drop_6(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #7
    @Rule(
        AND(
            Fact(kata='hilang'),Fact(kata='tabel'),
            )
        )
    def drop_7(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #8
    @Rule(
        AND(
            Fact(kata='jatuh'),Fact(kata='tabel'),
            )
        )
    def drop_8(self):
        self.declare(Fact(jenis_ddl='DROP'))                    
    
    #9
    @Rule(
        AND(
            Fact(kata='lenyap'),Fact(kata='tabel'),
            )
        )
    def drop_9(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #10
    @Rule(
        AND(
            Fact(kata='buang'),Fact(kata='tabel'),
            )
        )
    def drop_10(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #11
    @Rule(
        AND(
            Fact(kata='singkir'),Fact(kata='tabel'),
            )
        )
    def drop_11(self):
        self.declare(Fact(jenis_ddl='DROP'))        
    
    #12
    @Rule(
        AND(
            Fact(kata='drop'),Fact(kata='kolom'),
            )
        )
    def drop_12(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #13
    @Rule(
        AND(
            Fact(kata='drop'),Fact(kata='foreign'),Fact(kata='key'),
            )
        )
    def drop_13(self):
        self.declare(Fact(jenis_ddl='DROP'))
    
    #14
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='relasi')
            )
        )
    def drop_14(self):
        self.declare(Fact(jenis_ddl='DROP'))    
    
    #ALTER
    #1
    @Rule(
        AND(
            Fact(kata='tambah'),Fact(kata='kolom')
            )
        )
    def alter_1(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #2
    @Rule(
        AND(
            Fact(kata='ubah'),Fact(kata='tipe'),Fact(kata='data'),
            )
        )
    def alter_2(self):
        self.declare(Fact(jenis_ddl='ALTER')) 
    
    #3
    @Rule(
        AND(
            Fact(kata='tambah'),Fact(kata='foreign'),Fact(kata='key'),
            Fact(kata='kolom'),
            )
        )
    def alter_3(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #4
    @Rule(
        AND(
            Fact(kata='hapus'),Fact(kata='kolom'),Fact(kata='dari'),
            Fact(kata='tabel'),
            )
        )
    def alter_4(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #5
    @Rule(
        AND(
            Fact(kata='ganti'),Fact(kata='nama'),
            )
        )
    def alter_5(self):
        self.declare(Fact(jenis_ddl='ALTER'))  \
    
    #6
    @Rule(
        AND(
            Fact(kata='tambah'),Fact(kata='constraint'),
            )
        )
    def alter_6(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #7
    @Rule(
        AND(
            Fact(kata='buat'),Fact(kata='kolom'),Fact(kata='tabel'),
            )
        )
    def alter_7(self):
        self.declare(Fact(jenis_ddl='ALTER'))                                  
    
    #8
    @Rule(
        AND(
            Fact(kata='tambah'),Fact(kata='default'),Fact(kata='value'),
            Fact(kata='kolom')
            )
        )
    def alter_8(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #9
    @Rule(
        AND(
            Fact(kata='ubah'),Fact(kata='nama')
            )
        )
    def alter_9(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #10
    @Rule(
        AND(
            Fact(kata='ubah'),Fact(kata='kolom')
            )
        )
    def alter_10(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #11
    @Rule(
        AND(
            Fact(kata='jadi'),Fact(kata='kolom'),Fact(kata='tabel'),
            Fact(kata='tidak'),Fact(kata='kosong'),
            )
        )
    def alter_11(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #12
    @Rule(
        AND(
            Fact(kata='tambah'),Fact(kata='indeks'),Fact(kata='kolom'),
            )
        )
    def alter_11(self):
        self.declare(Fact(jenis_ddl='ALTER'))
    
    #CREATE
    #1
    @Rule(
        AND(
            Fact(kata='buat'),Fact(kata='tabel')
            )
        )
    def create_1(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #2
    @Rule(
        AND(
            Fact(kata='buat'),Fact(kata='indeks')
            )
        )
    def create_2(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #3
    @Rule(
        AND(
            Fact(kata='tambah'),Fact(kata='tabel')
            )
        )
    def create_3(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #4
    @Rule(
        AND(
            Fact(kata='butuh'),Fact(kata='tabel')
            )
        )
    def create_4(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #5
    @Rule(
        AND(
            Fact(kata='cipta'),Fact(kata='tabel')
            )
        )
    def create_5(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #6
    @Rule(
        AND(
            Fact(kata='bentuk'),Fact(kata='tabel')
            )
        )
    def create_6(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #7
    @Rule(
        AND(
            Fact(kata='hasil'),Fact(kata='tabel')
            )
        )
    def create_7(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #8
    @Rule(
        AND(
            Fact(kata='bikin'),Fact(kata='tabel')
            )
        )
    def create_8(self):
        self.declare(Fact(jenis_ddl='CREATE'))
    
    #9
    @Rule(
        AND(
            Fact(kata='ingin'),Fact(kata='tabel')
            )
        )
    def create_9(self):
        self.declare(Fact(jenis_ddl='CREATE'))

        
    @Rule()
    def rule_remove_duplicates_facts(self):
        seen = set()
        duplicates = []
        
        for fid, fact in self.facts.items():
            if isinstance(fact, Fact):
                key = tuple(fact.items())
                if key in seen:
                    duplicates.append(fid)
                else:
                    seen.add(key)

        for fid in duplicates:
            self.retract(fid)
    
    @Rule(
        OR(
            Fact(jenis_ddl='TRUNCATE'), Fact(jenis_ddl='DROP'), Fact(jenis_ddl='ALTER'), Fact(jenis_ddl='CREATE')
        )
    )
    def rule_remove_noddl_if_ddl_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_ddl' in fact and fact['jenis_ddl']=='NODDL':
                self.retract(id)
        self.halt()

    
    @Rule(Fact(kalimat=MATCH.kalimat), salience=3)
    def rule_extract_kalimat_to_kata(self, kalimat):
        kalimat = kalimat.lower().strip()
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        kalimat = re.sub(r'[^a-zA-Z0-9 ]','',kalimat)
        daftar_kata = kalimat.split()
        
        for kata in daftar_kata:
            self.declare(Fact(kata=kata))

        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        kalimat_stemming = stemmer.stem(kalimat)
        daftar_kata_dasar = kalimat_stemming.split()
        for kata in daftar_kata_dasar:
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
        daftar_kata = [fact['kata'] for _,fact in self.facts.items() if isinstance(fact, Fact) and 'kata' in fact]
        daftar_tabel = [fact['tabel'] for _,fact in self.facts.items() if isinstance(fact, Fact) and 'tabel' in fact]
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

    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(Fact(kalimat=kalimat), Fact(database=database))
        self.run()

        for fact in self.facts.values():
            if 'jenis_ddl' in fact:
                return fact['jenis_ddl']
        return 'NODDL'