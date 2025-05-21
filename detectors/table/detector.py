import json
import re

class TableDetector():

    def ekstraksi_semua_table_json(self, database):
        set_tabel = set()
        for table in database['entitas']:
            set_tabel.add(table)
            
        daftar_table = list(set_tabel)
        return daftar_table



    def tokenisasi(self, kalimat_ternormalisasi):
         daftar_kata = kalimat_ternormalisasi.split()
         return daftar_kata




    def normalisasi(self,kalimat):
        kalimat = kalimat.lower()
        kalimat = re.sub(r'[^a-z\s]', '', kalimat)        
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        return kalimat




    def filter(self, daftar_table_simmilarity, threshold):
        daftar_table_select = []
        for table in daftar_table_simmilarity:
            if table['nilai_simmilarity']>threshold:
                daftar_table_select.append(table['nama_table'])
        return daftar_table_select




    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)
            
        daftar_table = self.ekstraksi_semua_table_json(database)
        kalimat_ternormalisasi = self.normalisasi(kalimat=kalimat)
        daftar_kata = self.tokenisasi(kalimat_ternormalisasi=kalimat_ternormalisasi)
        daftar_table_simmilarity = self.set_daftar_table_simmilarity(daftar_kata=daftar_kata, daftar_table=daftar_table)
        daftar_table_select = self.filter(daftar_table_simmilarity=daftar_table_simmilarity,threshold=0.7)
        
        return daftar_table_select
    
    
    
    
    def set_daftar_table_simmilarity(self, daftar_table, daftar_kata):
        daftar_table_simmilarity = []
        for table in daftar_table:
            max_nilai = 0
            for kata in daftar_kata:
                nilai_jaccard_coefficient = self.jaccard_coefficient(table, kata)
                if nilai_jaccard_coefficient > max_nilai:
                    max_nilai = nilai_jaccard_coefficient
            data = {'nama_table': table, 'nilai_simmilarity': max_nilai}
            daftar_table_simmilarity.append(data)

            return daftar_table_simmilarity



    
    def jaccard_coefficient(self, kolom, kata):
        irisan = set(kata) & set(kolom)
        gabungan = set(kata) | set(kolom)
        skor = len(irisan) / len(gabungan) if gabungan else 0
        return skor