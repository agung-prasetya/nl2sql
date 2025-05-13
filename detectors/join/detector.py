from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class JoinDetector(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(jenis_join='NOJOIN')



        
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
            Fact(jenis_join='LEFTJOIN'), Fact(jenis_join='RIGHTJOIN'), Fact(jenis_join='INNERJOIN')
        )
    )
    def rule_remove_nojoin_if_join_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_join' in fact and fact['jenis_join']=='NOJOIN':
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
            if 'jenis_join' in fact:
                return fact['jenis_join']
        return 'NOJOIN'