from experta import *
import json
import re


class QtyDetector(KnowledgeEngine):
    def __init__(self, filepath_database_json):
        super().__init__()
        with open(filepath_database_json, 'r') as file:
            self.database = json.load(file)
    
    #Urutan 1
    @Rule(AS.fact_kalimat_tak_ternormalisasi << Fact(kalimat=MATCH.kalimat, ternormalisasi=False), salience=300)
    def rule_normalisasi_kalimat(self, fact_kalimat_tak_ternormalisasi):
        kalimat_tak_ternormalisasi = fact_kalimat_tak_ternormalisasi['kalimat']
        kalimat_ternormalisasi = kalimat_tak_ternormalisasi.lower().strip()
        kalimat_ternormalisasi = re.sub(r'\s+', ' ', kalimat_ternormalisasi).strip()
        kalimat_ternormalisasi = re.sub(r'\.$','', kalimat_ternormalisasi)

        self.modify(fact_kalimat_tak_ternormalisasi, kalimat=kalimat_ternormalisasi, ternormalisasi=True)
        

    # Urutan 2 : jika domain tidak cocok, proses tidak usah diteruskan. Cocok jika kalimat mengandung setidaknya satu nama tabel
    @Rule(
        AND(
            Fact(database=MATCH.database),
            Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
            TEST(lambda kalimat, database: not any([tabel for tabel in database['entitas'] if tabel.replace('_',' ') in kalimat]))
        ),     
        salience=295
    )
    def rule_cek_kecocokan_domain(self):
        self.halt()


    #Urutan 3: ekstraksi kalimat ke kata. 
    #Urutan rule ini harus dibawah urutan rule_cek_kecocokan_domain agar tidak dieksekusi sebenlum adanya kepastian bahwa domain cocok.
    #Selain itu, "menjadikan urutan rule ini dibawah rule_cek_kecocokan_domain" akan menghindari adanya konflik ketika ada sebuah fakta kalimat ternormaliasi
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
        salience=290
    )
    def rule_ekstraksi_kalimat_to_kata(self, fact_kalimat):
        daftar_kata = fact_kalimat['kalimat'].split()
        for id,kata in enumerate(daftar_kata):
            self.declare(Fact(kata=kata, posisi=id, kelas_kata='unknown', bagian_frase=False, kuantitas=False))
        
        self.declare(Fact(pembatas_kalimat='akhir', posisi=len(daftar_kata)))
        self.declare(Fact(pembatas_kalimat='awal', posisi=-1))

        self.retract(fact_kalimat)


    #Rule-rule berikut ini applicable untuk sebuah kata (tanpa melibatkan kata sebelum dan sesudahnya) 
    # sehingga urutanya harus didahulukan sebelum urutan rule frase.
    #Karena tidak mungkin ada kasus yang menyebabkan konflik, bobot setiap rule pada kelompok Urutan 4.x ini memiliki bobot sama
    
    #Urutan 4 - bilangan bulat
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: kata in ['nol','satu','dua','tiga','empat','lima','enam','tujuh','delapan','sembilan'])
        ),
        salience=285
    )
    def rule_identifikasi_kata_untuk_bilangan_bulat_1_digit(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_bulat')

        

    #Urutan 4 - bilangan bulat
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: kata in ['sepuluh','sebelas','seratus','seribu','sejuta','semilyar'])
        ), 
        salience=285
    )
    def rule_identifikasi_kata_untuk_bilangan_bulat_diatas_2_digit(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_bulat')
        


    #Urutan 4 - bilangan bulat
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: re.match(r'\b(?:\d{1,3}(?:[.,]\d{3})+)\b', kata) is not None)
        ), 
        salience=285
    )
    def rule_identifikasi_literal_angka_untuk_bilangan_bulat_diatas_2_digit(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_bulat')
        


    #Urutan - bilangan bulat bulat
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata:re.fullmatch(r'[ivxlcdm]+',kata) is not None)
        ), 
        salience=285)
    def rule_identifikasi_kata_angka_romawi(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_bulat')
        


    #Urutan - bilangan bulat bulat
    #misalnya mendeteksi 5000
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata:re.fullmatch(r'\b\d+\b',kata) is not None)
        ), 
        salience=285)
    def rule_identifikasi_literal_angka_bilangan_bulat(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_bulat')
        


    #Urutan 4 - kelas kata urutan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: kata=='pertama')
        ),
        salience=285
    )
    def rule_identifikasi_kata_pertama_urutan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='urutan')
        print('rule_identifikasi_kata_pertama_urutan')

    
    #Urutan 4 - kelas kata urutan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata:
                re.match('^ke-?', kata) is not None 
                and 
                any([
                    token for token in ['satu','dua','tiga','empat','lima','enam','tujuh',
                                        'delapan','sembilan','sepuluh','sebelas','seratus',
                                        'seribu','sejuta','semilyar','setriliun']
                    if token in kata]
                )
            )
        ), 
        salience=285)
    def rule_identifikasi_kata_awalan_ke_diikuti_kata_ke_urutan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='urutan')
        


    #Urutan 4 - kelas kata urutan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: re.fullmatch(r'^ke-?\d+', kata) is not None)
        ), 
        salience=285)
    def rule_identifikasi_kata_awalan_ke_diikuti_angka_ke_urutan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='urutan')
        


    #Urutan 4 - kelas kata urutan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: re.fullmatch(r'^ke-?[ivxlcdm]+', kata) is not None)
        ), 
        salience=285)
    def rule_identifikasi_kata_awalan_ke_diikuti_angka_ke_urutan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='urutan')
        

    #Urutan 4 - bilangan pecahan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            OR(
                TEST(lambda kata: kata == 'setengah'),
                TEST(lambda kata: re.match('^seper', kata) is not None and 
                     any([token for token in ['dua','tiga','empat','lima','enam','tujuh','delapan','sembilan']
                         if token in kata])
                )
            )
        ),
        salience=285
    )
    def rule_identifikasi_kata_bilangan_pecahan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_pecahan')
        

    
    #Urutan 4 - bilangan pecahan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata:re.fullmatch(r'[0-9]+[\.\,][0-9]+',kata) is not None)
        ), 
        salience=285)
    def rule_identifikasi_kata_bilangan_pecahan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bilangan_pecahan')
        



    #Urutan 4 - kelipatan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata:kata in ['belas', 'puluh','ratus','ribu','juta','milyar','triliun'])
        ), 
        salience=285)
    def rule_identifikasi_kata_kelipatan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='kelipatan')
        



    #Urutan 4 - satuan
    #Rule ini mendeteksi kata yang termasuk satuan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: kata in 
                ["buah", "biji", "butir", "batang", "lembar", "helai", "meter", "milimeter", 
                "sentimeter", "kilometer", "inci", "kaki", "yard", "mil", "kilogram", 
                "gram", "ons", "ton", "pon", "liter", "mililiter", "gallon", "cup", 
                "hektar", "meter persegi", "detik", "menit", "jam", "hari", "minggu", 
                "bulan", "tahun", "milidetik", "orang", "ekor", "pasang", 
                "lusin", "gross", "karung", "kotak", "paket", "dus", "bit", 
                "byte", "kilobyte", "megabyte", "gigabyte", "rupiah", "dolar", 
                "euro", "yen", "pound", "won", "ringgit", "baht", "rupee", 
                "yuan", "dirham", "derajat", "celcius", "kelvin", "fahrenheit", "persen",
                "m","mm","cm","km","in","kg","g","l","ml","rp","$","%"]
            )
        ),
        salience=285)
    def rule_identifikasi_kata_satuan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='satuan')
        


    #Urutan 4 - bulan
    #Rule ini mendeteksi kata yang termasuk bulan dalam bahasa Indonesia
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: kata in 
                    ["januari", "februari", "maret", "april", "mei", 
                    "juni", "juli", "agustus", "september", "oktober", 
                    "november", "desember","jan","feb","mar","apr",
                    "mei","jun","jul","ags","sep","okt","nov","des"]
            )
        ),
        salience=285)
    def rule_identifikasi_kata_bulan(self, fact_kata):
        self.modify(fact_kata, kelas_kata='bulan')
        



    #Urutan 4 - bulan
    #Rule ini mendeteksi kata yang termasuk bulan dalam bahasa Indonesia
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: kata in ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"])
        ),
        salience=285)
    def rule_identifikasi_kata_hari(self, fact_kata):
        self.modify(fact_kata, kelas_kata='hari')
        


    #Urutan 4 - tanggal
    #Rule ini mendeteksi token yang termasuk tanggal dalam format 
    # D/M/YYYY, D-M-YYYY, D/M/YY, D-M-YY, DD-MM-YYYY, DD/MM/YYYY
    # DD-MM-YY, DD/MM/YY
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: re.match(r"\b(0?[1-9]|[12][0-9]|3[01])[-/](0?[1-9]|1[0-2])[-/](\d{2}|\d{4})\b",kata) is not None)
        ),
        salience=285)
    def rule_identifikasi_literal_tanggal(self, fact_kata):
        self.modify(fact_kata, kelas_kata='tanggal')
        

    
    #Rule-rule berikut ini applicable untuk mendeteksi frase yang menunjukkan tanggal atau bulan+tahun
    # misalnya 20 oktober / 20 oktober 2025/ oktober 2020 
    #Rule-rule ini harus memiliki urutan sebelum rule-rule sebelum urutan 6 agar tidak terdeteksi oleh rule-rule urutan 6
    
    #Urutan 5 - frase tanggal + bulan + tahun
    #Misalnya 20 oktober 2020 / 1 oktober 2020 / 1 oktober 20 / 01 oktober 20
    @Rule(
        AND(
            AS.fact_tanggal << Fact(kata=MATCH.tanggal, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi1),
            AS.fact_bulan << Fact(kata=MATCH.bulan, kelas_kata='bulan', bagian_frase=False, posisi=MATCH.posisi2),
            AS.fact_tahun << Fact(kata=MATCH.tahun, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi3),
            TEST(lambda tanggal:re.fullmatch(r'[0-3]?[0-9]{1}',tanggal) is not None),
            TEST(lambda tahun:re.fullmatch(r'(?:\d{2})|(?:\d{4})',tahun) is not None),
            TEST(lambda posisi1,posisi2,posisi3:posisi1==posisi2-1 and posisi2==posisi3-1)
        ),
        salience=280
    )
    def rule_identifikasi_frase_tanggal_bulan_tahun(self, fact_tanggal, fact_bulan, fact_tahun):
        frase = f'{fact_tanggal['kata']} {fact_bulan['kata']} {fact_tahun['kata']}'
        
        self.declare(Fact(frase=frase, posisi=fact_tahun['posisi'],kuantitas=True))
        self.retract(fact_tanggal)
        self.retract(fact_bulan)
        self.retract(fact_tahun)
        



    #Urutan 6 - frase tanggal + bulan
    # Rule ini lebih bersifat general daripada rule urutan 5 sehingga harus dieksekusi setelah rule tanggal+bulan+tahun
    #Kombinasi yang dideteksi oleh rule ini misalnya, 20 oktober / 1 oktober / 01 oktober
    @Rule(
        AND(
            AS.fact_tanggal << Fact(kata=MATCH.tanggal, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi1),
            AS.fact_bulan << Fact(kata=MATCH.bulan, kelas_kata='bulan', bagian_frase=False, posisi=MATCH.posisi2),
            TEST(lambda tanggal:re.fullmatch(r'[0-3]{1,2}',tanggal) is not None),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        ),
        salience=275
    )
    def rule_identifikasi_kuantitas_dari_frase_tanggal_bulan(self, fact_tanggal, fact_bulan):
        frase = f'{fact_tanggal['kata']} {fact_bulan['kata']}'
        
        self.declare(Fact(frase=frase, posisi=fact_bulan['posisi'], kuantitas=True))
        self.retract(fact_tanggal)
        self.retract(fact_bulan)  
        
   
    
    #Urutan 6 - frase bulan+tahun
    #Rule ini lebih bersifat general daripada rule urutan 5 sehingga harus dieksekusi setelah rule tanggal+bulan+tahun
    #Rule ini tidak mungkin konflik dengan rule indetifikasi tanggal+bulan sehingga memiliki salience yang sama
    #Kombinasi yang dideteksi oleh rule ini misalnya, oktober 2025 / oktober 25
    @Rule(
        AND(
            AS.fact_kata1 << Fact(kata=MATCH.kata1, kelas_kata='bulan', bagian_frase=False, posisi=MATCH.posisi1),
            AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi2),
            TEST(lambda kata2:re.fullmatch(r'(\d{2})|(\d{4})',kata2) is not None),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        ),
        salience=275
    )
    def rule_identifikasi_kuantitas_dari_frase_bulan_tahun(self, fact_kata1, fact_kata2):
        frase = f'{fact_kata1['kata']} {fact_kata2['kata']}'
        
        self.declare(Fact(frase=frase, posisi=fact_kata2['posisi'], kuantitas=True))
        self.retract(fact_kata1)
        self.retract(fact_kata2) 
        


    #Rule-rule berikut ini applicable untuk mendeteksi frase (melibatkan kata sebelum dan sesudahnya) 
    
    #Urutan 6 - penggabungan 2 kata (bil bulat/urutan + kelipatan/bil bulat). 
    # Misalnya kedua puluh / keseratus dua/ lima belas/ dua puluh / seratus dua
    #Persayaratan utama adalah, 2 kata tersebut belum menjadi bagian sebuah frase dan 
    # kata yang awal/pertama haruslah didahului dengan kelas kata 'unknown' atau 'satuan' atau awal pembatas kalimat
    @Rule(
        AND(
            OR(
                Fact(kata=MATCH.kata0, kelas_kata='unknown', bagian_frase=False, posisi=MATCH.posisi0),
                Fact(kata=MATCH.kata0, kelas_kata='satuan', bagian_frase=False, posisi=MATCH.posisi0),
                Fact(pembatas_kalimat='awal')
            ),
            OR(
                AS.fact_kata1 << Fact(kata=MATCH.kata1, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi1),
                AS.fact_kata1 << Fact(kata=MATCH.kata1, kelas_kata='urutan', bagian_frase=False, posisi=MATCH.posisi1)
            ),
            OR(
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='kelipatan', bagian_frase=False, posisi=MATCH.posisi2),
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi2)
            ),
            TEST(lambda posisi0, posisi1, posisi2: posisi0==posisi1-1 and posisi1==posisi2-1)
        ),
        salience=270)
    def rule_penggabungan_bilangan_bulat_atau_urutan_dengan_kelipatan_atau_bilangan_bulat_ke_frase(self, fact_kata1, fact_kata2):
        frase = f'{fact_kata1['kata']} {fact_kata2['kata']}'

        self.declare(Fact(frase=frase, bagian_frase=False, posisi=fact_kata2['posisi'],kuantitas=False))
        self.retract(fact_kata1)
        self.retract(fact_kata2)
        
    
    
    #Urutan 7 - penggabungan frase dengan bilangan bulat/kelipatan
    #Rule ini membentuk frase bilangan bulat yang tersusun atas 3 kata atau lebih. 
    #Misalnya dua puluh lima / seratus dua puluh / lima ratus enam puluh dua ribu
    @Rule(
        AND(
            AS.fact_frase << Fact(frase=MATCH.frase, bagian_frase=False, posisi=MATCH.posisi1, kuantitas=False),
            OR(
                AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='bilangan_bulat', bagian_frase=False, posisi=MATCH.posisi2),
                AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='kelipatan', bagian_frase=False, posisi=MATCH.posisi2)
            ),
            TEST(lambda posisi1, posisi2: posisi1==posisi2-1)
        ),
        salience=265
        
    )
    def rule_penggabungan_frase_dengan_bilangan_bulat_atau_kelipatan_ke_frase(self, fact_frase,fact_kata):
        frase = f'{fact_frase['frase']} {fact_kata['kata']}'
        self.declare(Fact(frase=frase, bagian_frase=False, posisi=fact_kata['posisi'],kuantitas=False))
        self.retract(fact_kata)
        self.retract(fact_frase)
        
        
    #Urutan 8 -  penggabungan kata tunggal bilangan bulat + satuan
    #Rule ini harus dikerjakan setelah rule pada urutan 7 karena jika rule urutan 8 ini dikerjakan terlebih dahulu,
    #kata yang tunggal yang menjadi bagian frase akan digabung dengan kata satuan setelahnya. 
    #Misalnya, ...lebih dari dua biji...
    #Berbeda dengan dua puluh lima buah, seharusnya lima digabungkankan dengan dua puluh terlebih dahulu sebelum digabung dengan buah
    @Rule(
        AND(
            AS.fact_kata1 << Fact(kata=MATCH.kata1, kelas_kata='bilangan_bulat', posisi=MATCH.posisi1, kuantitas=False),
            AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='satuan', posisi=MATCH.posisi2, kuantitas=False),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        ),
        salience=260
    )
    def rule_identifikasi_kuantitas_dari_gabungan_kata_bilangan_bulat_dengan_satuan(self, fact_kata1, fact_kata2):
        frase = f'{fact_kata1['kata']} {fact_kata2['kata']}'
        
        self.declare(Fact(frase=frase, posisi=fact_kata2['posisi'], kuantitas=True))
        self.retract(fact_kata1)
        self.retract(fact_kata2)
        
    
    
    #Rule-rule berikut ini menyimpulkan kuantitas berdasarkan fakta-fakta yang ada.
    #Karena rule-rule berikut ini dijalankan yang terakhir, rule-rule ini memiliki salience default, yaitu 0
    
    #Urutan - terakhir
    #rule ini mendeteksi kata-kata yang telah jelas bahwa kata-kata tersebut adalah kuantitas, misalnya $10, Rp500.000,00 10%
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown', kuantitas=False),
            OR(
                TEST(lambda kata:re.match(r'^rp\d.*',kata) is not None),
                TEST(lambda kata:re.match(r'^\$\d.*',kata) is not None),
                TEST(lambda kata:re.fullmatch(r'^\d+[.,]?\d+%', kata) is not None)
            )
        )
    )
    def rule_identifikasi_kuantitas_dari_literal(self, fact_kata):
        self.modify(fact_kata, kuantitas=True)
        

        
    #Urutan - terakhir
    #Misalnya, rp 500.000,00
    @Rule(
        AND(
            AS.fact_kata1 << Fact(kata=MATCH.kata1, kelas_kata='satuan', posisi=MATCH.posisi1, kuantitas=False),
            OR(
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='bilangan_bulat', posisi=MATCH.posisi2, kuantitas=False),
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='bilangan_pecahan', posisi=MATCH.posisi2, kuantitas=False)
            ),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
    )
    def rule_identifikasi_kuantitas_dari_gabungan_satuan_dan_bilangan_bulat_atau_pecahan(self, fact_kata1, fact_kata2):
        frase = f'{fact_kata1['kata']} {fact_kata2['kata']}'
        
        self.declare(Fact(frase=frase, posisi=fact_kata2['posisi'], kuantitas=True))
        self.retract(fact_kata1)
        self.retract(fact_kata2)
        
        
    
    #Urutan - terakhir
    #Misalnya, ...sebanyak 50 beserta... | ...sejumlah 20 FULLSTOP 
    #Misalnya, ...terbanyak yang kedua FULLSTOP | ...terbanyak yang ketiga dari...
    #Misalnya, ...antara tanggal 5/2/25 hingga...| ...hingga 5/3/25 FULLSTOP  
    @Rule(
        AND(
            AS.fact_kata1 << Fact(kata=MATCH.kata1, kelas_kata='unknown', posisi=MATCH.posisi1, kuantitas=False),
            OR(
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='bilangan_bulat', posisi=MATCH.posisi2, kuantitas=False),
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='bilangan_pecahan', posisi=MATCH.posisi2, kuantitas=False),
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='tanggal', posisi=MATCH.posisi2, kuantitas=False),
                AS.fact_kata2 << Fact(kata=MATCH.kata2, kelas_kata='urutan', posisi=MATCH.posisi2, kuantitas=False)
            ),
            OR(
                AS.fact_kata3 << Fact(kata=MATCH.kata3, kelas_kata='unknown', posisi=MATCH.posisi3, kuantitas=False),
                AS.fact_kata3 << Fact(pembatas_kalimat='akhir', posisi=MATCH.posisi3)
            ),
            TEST(lambda posisi1,posisi2,posisi3:posisi1==posisi2-1 and posisi2==posisi3-1)
        )
    )
    def rule_identifikasi_kuantitas_dari_kata_tanpa_satuan(self, fact_kata2):
        self.modify(fact_kata2, kuantitas=True)
        
    
    #Urutan - terakhir
    #Rule ini mengidentifikasi gabungan frase dan satuan yang merupakan kuantitas 
    #Misalnya, seratus dua puluh lima rupiah
    @Rule(
        AND(
            AS.fact_frase << Fact(frase=MATCH.frase, posisi=MATCH.posisi1, bagian_frase=False, kuantitas=False),
            AS.fact_kata << Fact(kata=MATCH.kata, posisi=MATCH.posisi2, kelas_kata='satuan',  bagian_frase=False, kuantitas=False),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
    )
    def rule_identifikasi_kuantitas_dari_gabungan_frase_dan_satuan(self, fact_frase, fact_kata):
        frase = f'{fact_frase['frase']} {fact_kata['kata']}'
        
        self.declare(Fact(frase=frase, posisi=fact_kata['posisi'], kuantitas=True))
        self.retract(fact_frase)
        self.retract(fact_kata)        
        



    #Urutan - terakhir
    #Rule ini mengidentifikasi frase tanpa satuan yang merupakan kuantitas 
    #Misalnya, ...dari seratus dua puluh lima hingga ... | ...hingga seratus dua puluh lima FULLSTOP
    @Rule(
        AND(
            AS.fact_kata1 << Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, kelas_kata='unknown'),
            AS.fact_frase << Fact(frase=MATCH.frase, posisi=MATCH.posisi2, bagian_frase=False, kuantitas=False),
            OR(
                AS.fact_kata2 << Fact(kata=MATCH.kata2, posisi=MATCH.posisi3, kelas_kata='unknown'),
                AS.fact_kata2 << Fact(pembatas_kalimat='akhir', posisi=MATCH.posisi3),
            ),
            TEST(lambda fact_kata1,fact_frase,fact_kata2:
                fact_kata1['posisi']==fact_frase['posisi']-len(fact_frase['frase'].split()) and 
                fact_frase['posisi']==fact_kata2['posisi']-1)
        )
    )
    def rule_identifikasi_kuantitas_dari_frase_tanpa_satuan(self, fact_frase):
        self.modify(fact_frase, kuantitas=True)
        
    
    def detect(self, kalimat):
        
        self.reset()
        self.declare(Fact(kalimat=kalimat, ternormalisasi=False), Fact(database=self.database))
        self.run()

        facts_with_kuantitas = sorted(
            [fact for fact in self.facts.values() 
                if isinstance(fact, Fact) and 'kuantitas' in fact and fact['kuantitas'] is True
            ],
            key=lambda fact:fact['posisi']
        )
            
        return [fact.get('frase','') or fact.get('kata','') for fact in facts_with_kuantitas]
    