from experta import *
import json
import re
import textdistance
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class SortingDetector(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(jenis_sorting='NOSORTING')

    #ASC
    @Rule(
        AND(
            Fact(kata='sedikit'), Fact(kata='ke'), Fact(kata='banyak')
        )
    )
    def asc_r1(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='A'), Fact(kata='ke'), Fact(kata='Z')
        )
    )
    def asc_r2(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='terlama'), Fact(kata='ke'), Fact(kata='terbaru')
        )
    )
    def asc_r3(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='termurah'), Fact(kata='dahulu')
        )
    )
    def asc_r4(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='terkecil'), Fact(kata='ke'), Fact(kata='terbesar')
        )
    )
    def asc_r5(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='secara'), Fact(kata='menaik') 
        )
    )
    def asc_r6(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='awal'), Fact(kata='ke'), Fact(kata='akhir')
        )
    )
    def asc_r7(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='terendah'), Fact(kata='ke'), Fact(kata='tertinggi')
        )
    )
    def asc_r8(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='tua'), Fact(kata='ke'), Fact(kata='muda')
        )
    )
    def asc_r10(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='januari'), Fact(kata='ke'), Fact(kata='desember')
        )
    )
    def asc_r11(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='aktiva'), Fact(kata='ke'), Fact(kata='beban')
        )
    )
    def asc_r12(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    #DESC
    @Rule(
        AND(
            Fact(kata='banyak'), Fact(kata='ke'), Fact(kata='sedikit')
        )
    )
    def desc_r1(self):
        self.declare(Fact(jenis_sorting='DESC'))
    
    @Rule(
        AND(
            Fact(kata='Z'), Fact(kata='ke'), Fact(kata='A')
        )
    )
    def desc_r2(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='terbaru'), Fact(kata='ke'), Fact(kata='terlama')
        )
    )
    def desc_r3(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='termahal'), Fact(kata='dahulu')
        )
    )
    def desc_r4(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='terbesar'), Fact(kata='ke'), Fact(kata='terkecil')
        )
    )
    def desc_r5(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='secara'), Fact(kata='menurun')
        )
    )
    def desc_r6(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='tertinggi'), Fact(kata='ke'), Fact(kata='terendah')
        )
    )
    def desc_r7(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='akhir'), Fact(kata='ke'), Fact(kata='awal')
        )
    )
    def desc_r8(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='muda'), Fact(kata='ke'), Fact(kata='tua')
        )
    )
    def desc_r9(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='desember'), Fact(kata='ke'), Fact(kata='januari')
        )
    )
    def desc_r10(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='beban'), Fact(kata='ke'), Fact(kata='aktiva')
        )
    )
    def desc_r11(self):
        self.declare(Fact(jenis_sorting='DESC'))
    
    @Rule(
        OR(
            Fact(jenis_sorting='ASC'), Fact(jenis_sorting='DESC')
        )
    )
    def rule_remove_nosorting_if_sorting_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_sorting' in fact and fact['jenis_sorting']=='NOSORTING':
                self.retract(id)

    
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
            self.declare(Fact(tabel=tabel.lower()))
    

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

        for fact in self.facts.katas():
            if 'jenis_sorting' in fact:
                return fact['jenis_sorting']
        return 'NOSORTING'