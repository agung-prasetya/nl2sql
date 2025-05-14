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
            Fact(kata='sedikit', posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke', posisi=MATCH.posisi_antara), 
            Fact(kata='banyak', posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def asc_r1(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='a', posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='z', posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def asc_r2(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='lama', posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke', posisi=MATCH.posisi_antara), 
            Fact(kata='baru', posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r3(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='murah'), Fact(kata='dahulu')
        )
    )
    def asc_r4(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='kecil',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='besar',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def asc_r5(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='awal',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='akhir',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r7(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='rendah',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='tinggi',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r8(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='tua',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='muda',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r10(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='januari',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='desember',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r11(self):
        self.declare(Fact(jenis_sorting='ASC'))
        
    @Rule(
        AND(
            Fact(kata='aktiva',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='beban',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r12(self):
        self.declare(Fact(jenis_sorting='ASC'))
    
    @Rule(
        AND(
            Fact(kata='tanggal',posisi=MATCH.posisi_1),
            Fact(kata='mulai',posisi=MATCH.posisi_2), 
            Fact(kata='dari',posisi=MATCH.posisi_3), 
            Fact(kata='lama',posisi=MATCH.posisi_4),
            TEST(lambda posisi_1, posisi_2, posisi_3, posisi_4:posisi_1<posisi_2 and posisi_2<posisi_3 and posisi_3<posisi_4)
        )
    )
    def asc_r13(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(
        AND(
            Fact(kata='tanggal',posisi=MATCH.posisi_1),
            Fact(kata='mulai',posisi=MATCH.posisi_2), 
            Fact(kata='dari',posisi=MATCH.posisi_3), 
            Fact(kata='awal',posisi=MATCH.posisi_4),
            TEST(lambda posisi_1, posisi_2, posisi_3, posisi_4:posisi_1<posisi_2 and posisi_2<posisi_3 and posisi_3<posisi_4)
        )
    )
    def asc_r14(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(
        AND(
            Fact(kata='alfabet',posisi=MATCH.posisi_1),
            Fact(kata='dari',posisi=MATCH.posisi_2), 
            Fact(kata='awal',posisi=MATCH.posisi_3),
            TEST(lambda posisi_1, posisi_2, posisi_3:posisi_1<posisi_2 and posisi_2<posisi_3)
        )
    )
    def asc_r15(self):
        self.declare(Fact(jenis_sorting='ASC'))
    
    @Rule(
        AND(
            Fact(kata='cara',posisi=MATCH.posisi_1),
            Fact(kata='naik',posisi=MATCH.posisi_2), 
            TEST(lambda posisi_1, posisi_2:posisi_1<posisi_2)
        )
    )
    def asc_r16(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(
        AND(
            Fact(kata='mulai',posisi=MATCH.posisi_1),
            Fact(kata='tanggal',posisi=MATCH.posisi_2), 
            Fact(kata='awal',posisi=MATCH.posisi_3), 
            TEST(lambda posisi_1, posisi_2, posisi_3:posisi_1<posisi_2 and posisi_2<posisi_3)
        )
    )
    def asc_r17(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(
        AND(
            Fact(kata='rendah',posisi=MATCH.posisi_sebelum), 
            Fact(kata='hingga',posisi=MATCH.posisi_antara), 
            Fact(kata='tinggi',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)

        )
    )
    def asc_r18(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(
        AND(
            Fact(kata='tanggal',posisi=MATCH.posisi_1),
            Fact(kata='awal',posisi=MATCH.posisi_2), 
            Fact(kata='hingga',posisi=MATCH.posisi_3), 
            Fact(kata='baru',posisi=MATCH.posisi_4),
            TEST(lambda posisi_1, posisi_2, posisi_3, posisi_4:posisi_1<posisi_2 and posisi_2<posisi_3 and posisi_3<posisi_4)
        )
    )
    def asc_r19(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(
        AND(
            Fact(kata='sedikit',posisi=MATCH.posisi_1),
            Fact(kata='hingga',posisi=MATCH.posisi_2), 
            Fact(kata='banyak',posisi=MATCH.posisi_3), 
            TEST(lambda posisi_1, posisi_2, posisi_3:posisi_1<posisi_2 and posisi_2<posisi_3)
        )
    )
    def asc_r20(self):
        self.declare(Fact(jenis_sorting='ASC'))

    @Rule(Fact(kata='ascending'))
    def asc_r21(self):
        self.declare(Fact(jenis_sorting='ASC'))

    #DESC
    @Rule(
        AND(
            Fact(kata='banyak',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='sedikit',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r1(self):
        self.declare(Fact(jenis_sorting='DESC'))
    
    @Rule(
        AND(
            Fact(kata='z',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='a',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r2(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='baru',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='lama',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r3(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='mahal'), Fact(kata='dahulu')
        )
    )
    def desc_r4(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='besar',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='kecil',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r5(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='cara'), Fact(kata='turun')
        )
    )
    def desc_r6(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='tinggi',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='rendah',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r7(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='akhir',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='awal',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r8(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='muda',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='tua',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r9(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='desember',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='januari',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r10(self):
        self.declare(Fact(jenis_sorting='DESC'))
        
    @Rule(
        AND(
            Fact(kata='beban',posisi=MATCH.posisi_sebelum), 
            Fact(kata='ke',posisi=MATCH.posisi_antara), 
            Fact(kata='aktiva',posisi=MATCH.posisi_sesudah),
            TEST(lambda posisi_sebelum, posisi_antara, posisi_sesudah:posisi_sebelum<posisi_antara and posisi_sesudah>posisi_antara)
        )
    )
    def desc_r11(self):
        self.declare(Fact(jenis_sorting='DESC'))
    
    @Rule(
        AND(
            Fact(kata='tanggal',posisi=MATCH.posisi_1), 
            Fact(kata='mulai',posisi=MATCH.posisi_2), 
            Fact(kata='dari',posisi=MATCH.posisi_3),
            Fact(kata='baru',posisi=MATCH.posisi_4),
            TEST(lambda posisi_1, posisi_2, posisi_3, posisi_4:posisi_1<posisi_2 and posisi_3<posisi_4)
        )
    )
    def desc_r12(self):
        self.declare(Fact(jenis_sorting='DESC'))

    @Rule(
        AND(
            Fact(kata='alfabet',posisi=MATCH.posisi_1),
            Fact(kata='dari',posisi=MATCH.posisi_2), 
            Fact(kata='akhir',posisi=MATCH.posisi_3),
            TEST(lambda posisi_1, posisi_2, posisi_3:posisi_1<posisi_2 and posisi_2<posisi_3)
        )
    )
    def desc_r13(self):
        self.declare(Fact(jenis_sorting='DESC'))

    @Rule(
        AND(
            Fact(kata='mulai',posisi=MATCH.posisi_1), 
            Fact(kata='dari',posisi=MATCH.posisi_2), 
            Fact(kata='tanggal',posisi=MATCH.posisi_3),
            Fact(kata='baru',posisi=MATCH.posisi_4),
            TEST(lambda posisi_1, posisi_2, posisi_3, posisi_4:posisi_1<posisi_2 and posisi_3<posisi_4)
        )
    )
    def desc_r14(self):
        self.declare(Fact(jenis_sorting='DESC'))
    
    @Rule(Fact(kata='descending'))
    def desc_r15(self):
        self.declare(Fact(jenis_sorting='DESC'))

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
            Fact(jenis_sorting='ASC'), Fact(jenis_sorting='DESC')
        )
    )
    def rule_remove_nosorting_if_sorting_exist(self):
        for id, fact in list(self.facts.items()):
            if 'jenis_sorting' in fact and fact['jenis_sorting']=='NOSORTING':
                self.retract(id)
                break
        self.halt()

    
    @Rule(Fact(kalimat=MATCH.kalimat), salience=3)
    def rule_extract_kalimat_to_kata(self, kalimat):
        kalimat = kalimat.lower().strip()
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        kalimat = re.sub(r'[^a-zA-Z0-9 ]','',kalimat)
        
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        kalimat_stemming = stemmer.stem(kalimat)
        daftar_kata_dasar = kalimat_stemming.split()
        for id, kata in enumerate(daftar_kata_dasar):
            self.declare(Fact(kata=kata, posisi=id))


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
            tabel_name = tabel.replace('_',' ')
            if tabel_name in kalimat.lower():
                is_domain_match=True
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
            if 'jenis_sorting' in fact:
                return fact['jenis_sorting']
        return 'NOSORTING'

