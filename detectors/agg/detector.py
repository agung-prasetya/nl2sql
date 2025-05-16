from experta import *
import json
import re
import textdistance
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class AGGDetector(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(jenis_agregasi='NOAGG')


    @Rule(Fact(kata=MATCH.k), TEST(lambda k: k in [
        "jumlah", "total", "akumulasi", "keseluruhan", "penjumlahan",
        "agregasi", "jumlahkan", "semua", "akumulatif", "rekap"
    ]))
    def fungsi_sum(self):
        self.declare(Fact(jenis_agregasi="SUM"))
        

    @Rule(Fact(kata=MATCH.k), TEST(lambda k: k in [
        "rata-rata", "rerata", "average", "mean", "perhitungan rata-rata",
        "rataan", "nilai rata", "hitung rata-rata", "rata", "per rata"
    ]))
    def fungsi_avg(self):
        self.declare(Fact(jenis_agregasi="AVG"))
        
    @Rule(Fact(kata=MATCH.k), TEST(lambda k: k in [
        "maksimum", "tertinggi", "paling tinggi", "puncak", "nilai maksimum",
        "max", "angka tertinggi", "data terbesar", "jumlah terbesar", "terbesar"
    ]))
    def fungsi_max(self):
        self.declare(Fact(jenis_agregasi="MAX"))
        
    @Rule(Fact(kata=MATCH.k), TEST(lambda k: k in [
        "minimum", "terendah", "paling sedikit", "paling kecil", "terkecil",
        "min", "angka terkecil", "nilai minimum", "jumlah terkecil", "data terkecil"
    ]))
    def fungsi_min(self):
        self.declare(Fact(jenis_agregasi="MIN"))
        
    @Rule(Fact(kata=MATCH.k), TEST(lambda k: k in [
        "berapa banyak", "jumlah data", "total baris", "hitung", "jumlahkan data",
        "data berapa", "kuantitas", "count", "berapa", "jumlah entry"
    ]))
    def fungsi_count(self):
        self.declare(Fact(jenis_agregasi="COUNT"))
        

    
        
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
            Fact(jenis_agregasi='AVG'), Fact(jenis_agregasi='COUNT'), Fact(jenis_agregasi='MAX'), Fact(jenis_agregasi='MIN'), Fact(jenis_agregasi='SUM')
        )
    )
    def rule_remove_noagg_if_agg_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_agregasi' in fact and fact['jenis_agregasi']=='NOAGG':
                self.retract(id)
        self.halt()

    
    @Rule(Fact(kalimat=MATCH.kalimat), salience=3)
    def rule_extract_kalimat_to_kata(self, kalimat):
        kalimat = kalimat.lower().strip()
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
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
        daftar_tabel = [fact['tabel'] for _,fact in self.facts.items() if isinstance(fact, Fact) and 'tabel' in fact]
        for tabel in daftar_tabel:
            if tabel.replace('_',' ') in kalimat:
                is_domain_match = True
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
            if 'jenis_agregasi' in fact:
                return fact['jenis_agregasi']
        return 'NOAGG'