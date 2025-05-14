from experta import *
import json
import re
import textdistance

class QtyDetector(KnowledgeEngine):
    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('bilangan_bulat')),
            TEST(lambda kata: kata in ['nol','satu','dua','tiga','empat','lima','enam','tujuh','delapan','sembilan'])
        ), salience=2
    )
    def rule1_kata_dasar_bilangan_bulat_1_digit(self, fact, kata):
        self.modify(fact, kelas_kata='bilangan_bulat')
            


    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('bilangan_bulat')),
            TEST(lambda kata: kata in ['sepuluh','sebelas','seratus','seribu','sejuta','semilyar'])
        ), salience=2)
    def rule2_kata_imbuhan_bilangan_bulat_2_digit_lebih(self, fact, kata):
        self.modify(fact, kelas_kata='bilangan_bulat')




    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('bilangan_pecahan')),
            OR(
                TEST(lambda kata: kata == 'setengah'),
                TEST(lambda kata: 'seper' in kata and kata[len('seper'):] in 
                     ['dua','tiga','empat','lima','enam','tujuh','delapan','sembilan'])
            )
        )
    )
    def rule3_kata_imbuhan_bilangan_pecahan(self, fact, kata):
        self.modify(fact, kelas_kata='bilangan_pecahan')
        
        
    
    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, posisi=MATCH.posisi, kelas_kata=~L('pembagi_bilangan')),
            Fact(posisi=MATCH.posisi_sebelum, kelas_kata='bilangan_bulat'),
            TEST(lambda posisi, posisi_sebelum:posisi_sebelum==posisi-1),
            TEST(lambda kata:'per' in kata)
        ), salience=1)
    def rule4_kata_imbuhan_bilangan_pecahan(self, fact, kata, posisi, posisi_sebelum):
        self.modify(fact, kelas_kata='pembagi_bilangan')
            

    
    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('satuan_kelipatan')),
            TEST(lambda kata:kata in ['puluh','ratus','ribu','juta','milyar','triliun'])
        ), salience=2)
    def rule5_kata_imbuhan_satuan_kelipatan(self, fact, kata):
        self.modify(fact, kelas_kata='satuan_kelipatan')
            

    
    @Rule(
        'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('urutan')),
        OR(
            TEST(lambda kata: kata=='pertama'),
            AND(
                'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('urutan')),
                TEST(lambda kata: kata.startswith('ke')),
                TEST(lambda kata: kata in 'ke-seratus' ),
                OR(
                    TEST(lambda kata: kata in 'ke-seratus' ),
                    TEST(lambda kata: re.fullmatch(
                        r'[ivxlcdm]+', 
                        kata[len('ke') if '-' in kata else len('ke')+1]) is not None)
                )
            )
        )
    )
    def rule6_kata_dasar_urutan(self, fact, kata):
        self.modify(fact, kelas_kata='urutan')



    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('bilangan_bulat')),
            TEST(lambda kata:re.fullmatch(r'[ivxlcdm]+',kata) is not None)
        ), salience=2)
    def rule7_kata_dasar_bilangan_bulat_romawi(self, fact, kata):
        self.modify(fact, kelas_kata='bilangan_bulat')



    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, kelas_kata=~L('bilangan_pecahan')),
            OR(
                TEST(lambda kata:re.fullmatch(r'[0-9]+\.[0-9]+',kata) is not None),
                TEST(lambda kata:re.fullmatch(r'[0-9]+,[0-9]+',kata) is not None)
            )
            
        )
    )
    def rule8_literal_angka_pecahan(self, fact, kata):
        self.modify(fact, kelas_kata='bilangan_pecahan')

    
    
    @Rule(
        AND(
            'fact' << Fact(kata=MATCH.kata, adalah_kuantitas=False),
            TEST(lambda kata:re.fullmatch(r'^rp[0-9].*',kata) is not None)
        )
    )
    def rule9_literal_rupiah_angka(self, fact, kata):
        match = re.search(r'rp([\d\.]+,\d+)', kata)
        if match:
            self.modify(fact, 
                        adalah_kuantitas=True, nilai=match.group(1).replace('.', ''), 
                        satuan='rupiah', kelas_kata='bilangan_pecahan')
    
    

    # tanggal
    #satuan rp, $
    # huruf romawi
    # urutan pertama, kedua, ketiga, keempat
    #letter angka
    #frase
    #%
    
    
    
    @Rule(Fact(kalimat=MATCH.kalimat), salience=3)
    def rule_extract_kalimat_to_kata(self, kalimat):
        kalimat = kalimat.lower().strip()
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()

        for posisi,kata in enumerate(kalimat.split()):
            self.declare(Fact(kata=kata, posisi=posisi, kelas_kata='unknown', adalah_kuantitas=False))


    @Rule(Fact(database=MATCH.database), salience=3)
    def rule_extract_database(self, database):
        for tabel in database['entitas']:
            self.declare(Fact(tabel=tabel))
    

    @Rule(AND(Fact(kalimat=MATCH.kalimat),Fact(database=MATCH.database)),salience=2)
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
    
    def detect(self, kalimat):
        self.reset()
        self.declare(Fact(kalimat=kalimat))
        self.run()

        for fact in self.facts.items():
            print(fact)

    