import json
import re

class TableDetector():
    def __init__(self, filepath_database_json):
        super().__init__()
        self.filepath_database_json = filepath_database_json
        with open(filepath_database_json, 'r') as file:
            self.database = json.load(file)

    def ekstraksi_semua_table_json(self):
        set_tabel = set()
        for table in self.database['entitas']:
            for table in self.database['entitas'][table]:
                set_table.add(table)

        daftar_table = list(set_table)
        return daftar_table

    def tokenisasi(self, kalimat_ternormalisasi):
         daftar_kata = kalimat_ternormalisasi.split()
         return daftar_kata



    def set_daftar_table_simmilarity(self, daftar_kata, daftar_table):
         hasil = []
         set_kata = set(daftar_kata)
         for table in daftar_table:
            
            tokens_kolom = table.lower().replace('_', ' ').split()
            set_table = set(token_table)

            irisan = set_kata & set_table
            gabungan = set_kata | set_table
            skor = len(irisan) / len(gabungan) if gabungan else 0

            hasil.append({
                'nama_table': table,
                'nilai_simmilarity': skor
            })
            return hasil

    def normalisasi(self,kalimat):
       
        kalimat = kalimat.lower()
        kalimat = re.sub(r'[^a-z\s]', '', kalimat)        
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        return kalimat


    def filter(self, daftar_kolom_simmilarity, threshold):
        daftar_table_select = []
        for table in daftar_table_simmilarity:
            if table['nilai_simmilarity']>threshold:
                daftar_table_select.append(table['nama_table'])
        return daftar_table_select

    def detect(self, kalimat):
        daftar_table = self.ekstraksi_semua_table_json(file_name_json=self.file_database_json)
        kalimat_ternormalisasi = self.normalisasi(kalimat=kalimat)
        daftar_kata = self.tokenisasi(kalimat_ternormalisasi=kalimat_ternormalisasi)
        daftar_table_simmilarity = self.set_daftar_table_simmilarity(daftar_kata=daftar_kata, daftar_table=daftar_table)
        daftar_table_select = self.filter(daftar_table_simmilarity=daftar_table_simmilarity,threshold=0.55)
        return daftar_table_select
    def set_daftar_table_simmilarity(daftar_table, daftar_kata):
    daftar_table_simmilarity = []

    for table in daftar_table:
        max_nilai = 0
        for kata in daftar_kata:
            nilai_jaccard_coefficient = jaccard_coefficient(table, kata)
            if nilai_jaccard_coefficient > max_nilai:
                max_nilai = nilai_jaccard_coefficient
        data = {'nama_table': table, 'nilai_simmilarity': max_nilai}
        daftar_table_simmilarity.append(data)

        return daftar_table_simmilarity
