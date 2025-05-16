from experta import *
import json
import re

class QtyDetector(KnowledgeEngine):
    
    #Urutan 1
    @Rule(AS.fact_kalimat_tak_ternormalisasi << Fact(kalimat=MATCH.kalimat, ternormalisasi=False), salience=300)
    def rule_normalisasi_kalimat(self, fact_kalimat_tak_ternormalisasi):
        kalimat_tak_ternormalisasi = fact_kalimat_tak_ternormalisasi['kalimat']
        kalimat_ternormalisasi = kalimat_tak_ternormalisasi.lower().strip()
        kalimat_ternormalisasi = re.sub(r'\s+', ' ', kalimat_ternormalisasi).strip()

        self.modify(fact_kalimat_tak_ternormalisasi, kalimat=kalimat_ternormalisasi, ternormalisasi=True)



    #Urutan 2 : jika domain tidak cocok, proses tidak usah diteruskan. Cocok jika kalimat mengandung setidaknya satu nama tabel
    @Rule(
        AND(
            Fact(database=MATCH.database),
            Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
            TEST(lambda kalimat, database: 
                 not any(tabel for tabel in database['entitas'] if tabel.replace('_',' ') in kalimat)
            )
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
            self.declare(
                Fact(kata=kata, posisi=id, kelas_kata='unknown', bagian_frase=False, kuantitas=False))
        
        self.declare(Fact(pembatas_kalimat='awal', posisi=len(daftar_kata)))
        self.declare(Fact(pembatas_kalimat='akhir', posisi=-1))

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
            TEST(lambda kata: re.match(r'\b(?:\d{1,3}(?:[.,]\d{3})+)\b') is not None)
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

    
    #Urutan 4 - kelas kata urutan
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata:
                re.match('^ke-?') is not None 
                and 
                any(
                    token for token in ['satu','dua','tiga','empat','lima','enam','tujuh',
                                        'delapan','sembilan','sepuluh','sebelas','seratus',
                                        'seribu','sejuta','semilyar','setriliun']
                    if token in kata
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
            TEST(lambda kata: re.match('^ke-?\d+') is not None)
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
                TEST(lambda kata: re.match('^seper') is not None and 
                     any(token for token in ['dua','tiga','empat','lima','enam','tujuh','delapan','sembilan']
                         if token in kata)
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
    def rule_identifikasi_kata_hari(self, fact_kata):
        self.modify(fact_kata, kelas_kata='tanggal')

    
    #Rule-rule berikut ini applicable untuk mendeteksi frase yang menunjukkan tanggal atau bulan+tahun
    # misalnya 20 oktober / oktober 2020 / 20 oktober 2025
    #Rule-rule ini harus memiliki urutan sebelum rule-rule sebelum urutan 6 agar tidak terdeteksi oleh rule-rule urutan 6

    #Urutan 5 - 
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown'),
            TEST(lambda kata: re.match(r"\b(0?[1-9]|[12][0-9]|3[01])[-/](0?[1-9]|1[0-2])[-/](\d{2}|\d{4})\b") is not None)
        ),
        salience=285)
    def rule_identifikasi_kata_hari(self, fact_kata):
        self.modify(fact_kata, kelas_kata='tanggal')


    #Rule-rule berikut ini applicable untuk mendeteksi frase (melibatkan kata sebelum dan sesudahnya) 
    #Urutan rule-rule yang termasuk frase harus setelah rule yang aplicable untuk kata.

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
        salience=275)
    def rule_penggabungan_bilangan_bulat_atau_urutan_dengan_kelipatan_atau_bilangan_bulat_ke_frase(self, fact_kata1, fact_kata2):
        frase = f'{fact_kata1['kata']} {fact_kata2['kata']}'
        self.modify(fact_kata1, bagian_frase=True)
        self.modify(fact_kata2, bagian_frase=True)
        self.declare(Fact(frase=frase, bagian_frase=False, posisi=fact_kata2['posisi'],kuantitas=False))

    
    
    
    

    
    #deteksi frase "tahun 2025"
    #lima puluh ribu rupiah / lima puluh ribu dolar

    
    
    @Rule(
        AND(
            'fact_urutan' << Fact(kata=MATCH.kata1, kelas_kata='urutan',posisi=MATCH.posisi1, bagian_frase=False),
            'fact_bilangan_bulat' << Fact(kata=MATCH.kata2, kelas_kata='bilangan_bulat',posisi=MATCH.posisi2, bagian_frase=False),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
        ,salience=3)
    def rule11_join_kata_kelas_urutan_dengan_kata_bilangan_bulat_ke_frase_urutan(self, fact_urutan, fact_bilangan_bulat):
        frase = f"{fact_urutan['kata']} {fact_bilangan_bulat['kata']}"

        self.declare(Fact(frase=frase, kelas_kata='urutan', posisi=fact_bilangan_bulat['posisi'], bagian_frase=False, adalah_kuantitas=False))

        self.modify(fact_urutan, bagian_frase=True)
        self.modify(fact_bilangan_bulat, bagian_frase=True)
    

    #mendeteksi tampilkan data kedua puluh lima
    @Rule(
        AND(
            'fact_frase_urutan' << Fact(frase=MATCH.frase, kelas_kata='urutan',posisi=MATCH.posisi1, bagian_frase=False),
            'fact_bilangan_bulat' << Fact(kata=MATCH.kata, kelas_kata='bilangan_bulat',posisi=MATCH.posisi2, bagian_frase=False),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
        ,salience=3)
    def rule11_join_frase_kelas_urutan_dengan_kata_bilangan_bulat_ke_frase_urutan(self, fact_frase_urutan, fact_bilangan_bulat):
        frase = f"{fact_frase_urutan['frase']} {fact_bilangan_bulat['kata']}"

        self.declare(Fact(frase=frase, kelas_kata='urutan', posisi=fact_bilangan_bulat['posisi'], bagian_frase=False, adalah_kuantitas=False))

        self.retract(fact_frase_urutan)
        self.modify(fact_bilangan_bulat, bagian_frase=True)

        
    #semua rule harus dikelompokkan, kelompok mana yang didahulukan. set salience nya

    @Rule(
        AND(
            'fact_kata1' << Fact(kata=MATCH.kata1, kelas_kata='bilangan_bulat',posisi=MATCH.posisi1, bagian_frase=False),
            OR(
                'fact_kata2' << Fact(kata=MATCH.kata2, kelas_kata='bilangan_bulat',posisi=MATCH.posisi2, bagian_frase=False),
                'fact_kata2' << Fact(kata=MATCH.kata2, kelas_kata='satuan_kelipatan',posisi=MATCH.posisi2, bagian_frase=False),
            ),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
    )
    def rule10_join_pasangan_kata_ke_frase_bil_bulat(self, fact_kata1, fact_kata2):
        frase = f"{fact_kata1['kata']} {fact_kata2['kata']}"

        self.declare(Fact(frase=frase, kelas_kata='bilangan_bulat', posisi=fact_kata2['posisi'], bagian_frase=False, adalah_kuantitas=False))
        self.modify(fact_kata1, bagian_frase=True)
        self.modify(fact_kata2, bagian_frase=True)



    @Rule(
        AND(
            'fact_frase' << Fact(frase=MATCH.frase, kelas_kata='bilangan_bulat',posisi=MATCH.posisi1, bagian_frase=False, adalah_kuantitas=False),
            OR(
                'fact_kata' << Fact(kata=MATCH.kata, kelas_kata='bilangan_bulat',posisi=MATCH.posisi2, bagian_frase=False, adalah_kuantitas=False),
                'fact_kata' << Fact(kata=MATCH.kata, kelas_kata='satuan_kelipatan',posisi=MATCH.posisi2, bagian_frase=False, adalah_kuantitas=False),
            ),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
    )
    def rule11_join_frase_kata_ke_frase_bil_bulat(self, fact_frase, fact_kata):
        frase = f"{fact_frase['frase']} {fact_kata['kata']}"
        
        self.declare(Fact(frase=frase, kelas_kata='bilangan_bulat', posisi=fact_kata['posisi'], bagian_frase=False, adalah_kuantitas=False))
        self.retract(fact_frase)
        self.modify(fact_kata, bagian_frase=True)


    @Rule(
        AND(
            OR(
                'fact' << Fact(frase=MATCH.frase, kelas_kata='bilangan_bulat', posisi=MATCH.posisi1, bagian_frase=False, adalah_kuantitas=False),
                'fact' << Fact(frase=MATCH.frase, kelas_kata='urutan', posisi=MATCH.posisi1, bagian_frase=False, adalah_kuantitas=False),
                'fact' << Fact(kata=MATCH.kata, kelas_kata='bilangan_bulat', posisi=MATCH.posisi1, bagian_frase=False, adalah_kuantitas=False),
            ),
            OR(
                Fact(fullstop=True, posisi=MATCH.posisi2),
                Fact(kata=MATCH.kata, kelas_kata='unknown',posisi=MATCH.posisi2, bagian_frase=False, adalah_kuantitas=False),
                Fact(kata=MATCH.kata, kelas_kata='satuan',posisi=MATCH.posisi2, bagian_frase=False, adalah_kuantitas=False)
            ),
            TEST(lambda posisi1,posisi2:posisi1==posisi2-1)
        )
    )
    def rule12_penentuan_kuantitas_bil_bulat(self, fact):
        self.modify(fact, adalah_kuantitas=True)

 #rule ini mendeteksi kata-kata yang telah jelas bahwa kata-kata tersebut adalah kuantitas, misalnya $10, Rp500.000,00 10%
    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata, kelas_kata='unknown', kuantitas=False),
            OR(
                TEST(lambda kata:re.match(r'^rp\d.*',kata) is not None),
                TEST(lambda kata:re.match(r'^\$\d.*',kata) is not None)
            )
        )
    )
    def rule_eksplisit_literal_kuantitas(self, fact_kata):
        self.modify(fact_kata, kuantitas=True)

    #rule pembagi bilangan dan pecahan
    # tanggal
    # huruf romawi
    # urutan pertama, kedua, ketiga, keempat
    #letter angka
    #frase
    #% persen
    
    
    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(Fact(kalimat=kalimat, ternormalisasi=False), Fact(database=database))
        self.run()

        x = self.facts.items()
        for fact in self.facts.items():
            print(fact)

    