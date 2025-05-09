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
        Fact(kata='tampilkan')
    )
    def db_inventori_1_SELECT_1(self):
        self.declare(Fact(jenis_dml='SELECT'))


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