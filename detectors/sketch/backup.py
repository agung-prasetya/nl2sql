
from experta import *
import json
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class SketchDetector(KnowledgeEngine):
    @Rule(
        AS.fact_kalimat << Fact(kalimat=MATCH.kalimat, ternormalisasi=False),
        salience=500
    )
    def rule_normalisasi_kalimat(self, fact_kalimat, kalimat):
        kalimat_ternormalisasi = kalimat.lower()
        kalimat_ternormalisasi = re.sub(r'[.,]$', '', kalimat_ternormalisasi)
        self.modify(fact_kalimat, kalimat=kalimat_ternormalisasi, ternormalisasi=True)

    @Rule(
        Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
        salience=495
    )
    def rule_stemming_kalimat(self, kalimat):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        kalimat_stemming = stemmer.stem(kalimat)
        self.declare(Fact(kalimat=kalimat_stemming, terstemming=True))

    @Rule(
        AND(
            Fact(kalimat=MATCH.kalimat1, ternormalisasi=True),
            Fact(kalimat=MATCH.kalimat2, terstemming=True)
        ),
        salience=490
    )
    def rule_ekstraksi_kata(self, kalimat1, kalimat2):
        daftar_kata_kalimat_ternormalisasi = kalimat1.split()
        for id, kata in enumerate(daftar_kata_kalimat_ternormalisasi):
            self.declare(Fact(kata=kata, posisi=id))

        daftar_kata_kalimat_terstemming = kalimat2.split()
        for id, kata in enumerate(daftar_kata_kalimat_terstemming):
            if kata not in daftar_kata_kalimat_ternormalisasi:
                self.declare(Fact(kata=kata, posisi=id))

    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_nama_tabel' not in fact_kata),
            Fact(database=MATCH.database),
            TEST(lambda kata, database: any(nama_tabel for nama_tabel in database['entitas'] if nama_tabel in kata))
        ),
        salience=485
    )
    def rule_identifikasi_kata_yang_merujuk_nama_tabel(self, fact_kata):
        self.modify(fact_kata, apakah_nama_tabel=True)

    @Rule(
        AND(
            Fact(kalimat=MATCH.kalimat, ternormalisasi=True),
            Fact(database=MATCH.database)
        ),
        salience=481
    )
    def rule_phrase_nama_tabel(self, kalimat, database):
        kata_kalimat = kalimat.split()
        for i in range(len(kata_kalimat)-1):
            gabung = kata_kalimat[i] + "_" + kata_kalimat[i+1]
            if gabung in database['entitas']:
                self.declare(Fact(kata=gabung, posisi=i, apakah_nama_tabel=True))

    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_select' not in fact_kata),
            TEST(lambda kata: kata in ['tampil', 'lihat', 'tunjuk', 'ambil', 'cari', 'dapat'])
        ),
        salience=480
    )
    def rule_identifikasi_kata_yang_merujuk_select(self, fact_kata):
        self.modify(fact_kata, apakah_select=True)

    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_semua_kolom' not in fact_kata),
            TEST(lambda kata: kata in ['semua', 'seluruh', 'lengkap', 'data', 'informasi', 'rekaman', 'entri', 'record', 'isi'])
        ),
        salience=480
    )
    def rule_identifikasi_kata_yang_merujuk_semua_kolom(self, fact_kata):
        self.modify(fact_kata, apakah_semua_kolom=True)

    @Rule(
        AND(
            AS.fact_kata << Fact(kata=MATCH.kata),
            TEST(lambda fact_kata: 'apakah_condition' not in fact_kata),
            TEST(lambda kata: kata in ['yang', 'dengan', 'dimana', 'berstatus', 'memiliki', 'bergelar', 'jurusannya', 'sks', 'kapasitas', 'harinya', 'id', 'nimnya', 'namanya', 'tanggal'])
        ),
        salience=480
    )
    def rule_identifikasi_kata_condition(self, fact_kata):
        self.modify(fact_kata, apakah_condition=True)

    @Rule(
        AND(
            Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, apakah_select=True),
            Fact(kata=MATCH.kata2, posisi=MATCH.posisi2, apakah_nama_tabel=True),
            Fact(kata=MATCH.kata3, posisi=MATCH.posisi3, apakah_condition=True),
            TEST(lambda posisi1, posisi2, posisi3: posisi1 < posisi2 < posisi3)
        ),
        salience=476
    )
    def rule_identifikasi_sketsa_select_where(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE WHERE $CONDITION"))

    @Rule(
        AND(
            Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, apakah_select=True),
            Fact(kata=MATCH.kata2, posisi=MATCH.posisi2, apakah_semua_kolom=True),
            Fact(kata=MATCH.kata3, posisi=MATCH.posisi3, apakah_nama_tabel=True),
            Fact(kata=MATCH.kata4, posisi=MATCH.posisi4, apakah_condition=True),
            TEST(lambda posisi1, posisi2, posisi3, posisi4: posisi1 < posisi2 < posisi3 < posisi4)
        ),
        salience=476
    )
    def rule_identifikasi_sketsa_select_all_where(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE WHERE $CONDITION"))

    @Rule(
        AND(
            Fact(kata=MATCH.kata1, posisi=MATCH.posisi1, apakah_select=True),
            Fact(kata=MATCH.kata2, posisi=MATCH.posisi2, apakah_semua_kolom=True),
            Fact(kata=MATCH.kata3, posisi=MATCH.posisi3, apakah_nama_tabel=True),
        NOT(Fact(condition=MATCH.anything)),
            NOT(Fact(condition=MATCH.anything))
        ),
        salience=475
    )
    def rule_identifikasi_sketsa_1(self):
        self.declare(Fact(jenis_sketsa="SELECT * FROM $TABLE"))

    @Rule(
        AND(
            Fact(kata=MATCH.kata, posisi=MATCH.posisi, apakah_condition=True),
            Fact(kalimat=MATCH.kalimat, ternormalisasi=True)
        ),
        salience=460
    )
    def rule_ekstraksi_condition(self, kata, posisi, kalimat):
        kata_kalimat = kalimat.split()
        if posisi + 1 < len(kata_kalimat):
            condition = ' '.join(kata_kalimat[posisi + 1:])
            self.declare(Fact(condition=condition))

    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)

        self.reset()
        self.declare(Fact(kalimat=kalimat, ternormalisasi=False), Fact(database=database))
        self.run()

        hasil = {'jenis_sketsa': 'NOSKETCH', 'condition': None}
        for fact in self.facts.values():
            if 'jenis_sketsa' in fact:
                hasil['jenis_sketsa'] = fact['jenis_sketsa']
            if 'condition' in fact:
                hasil['condition'] = fact['condition']
        return hasil
