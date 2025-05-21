import json
import re

class ColumnDetector():
    def __init__(self, filepath_database_json):
        super().__init__()
        self.filepath_database_json = filepath_database_json
        with open(filepath_database_json, 'r') as file:
            self.database = json.load(file)

    def ekstraksi_semua_kolom_json(self):
        set_kolom = set()
        for tabel in self.database['entitas']:
            for kolom in self.database['entitas'][tabel]:
                set_kolom.add(kolom)

        daftar_kolom = list(set_kolom)
        return daftar_kolom

    def tokenisasi(self, kalimat_ternormalisasi):
        daftar_kata = kalimat_ternormalisasi.split()
        return daftar_kata


    def set_daftar_kolom_simmilarity(self, daftar_kata, daftar_kolom):
        hasil = []
        set_kata = set(daftar_kata)

        for kolom in daftar_kolom:
            
            tokens_kolom = kolom.lower().replace('_', ' ').split()
            set_kolom = set(tokens_kolom)

            irisan = set_kata & set_kolom
            gabungan = set_kata | set_kolom
            skor = len(irisan) / len(gabungan) if gabungan else 0

            hasil.append({
                'nama_kolom': kolom,
                'nilai_simmilarity': skor
            })

        return hasil

    def normalisasi(self,kalimat):

        kalimat = kalimat.lower()
        kalimat = re.sub(r'[^a-z\s]', '', kalimat)        
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        return kalimat

    def filter(self, daftar_kolom_simmilarity, threshold):
        daftar_kolom_select = []
        for kolom in daftar_kolom_simmilarity:
            if kolom['nilai_simmilarity']>threshold:
                daftar_kolom_select.append(kolom['nama_kolom'])
        return daftar_kolom_select

    def detect(self, kalimat):
        daftar_kolom = self.ekstraksi_semua_kolom_json(file_name_json=self.file_database_json)
        kalimat_ternormalisasi = self.normalisasi(kalimat=kalimat)
        daftar_kata = self.tokenisasi(kalimat_ternormalisasi=kalimat_ternormalisasi)
        daftar_kolom_simmilarity = self.set_daftar_kolom_simmilarity(daftar_kata=daftar_kata, daftar_kolom=daftar_kolom)
        daftar_kolom_select = self.filter(daftar_kolom_simmilarity=daftar_kolom_simmilarity,threshold=0.55)
        return daftar_kolom_select

def set_daftar_kolom_simmilarity(self, daftar_kolom, daftar_kata):
    daftar_kolom_simmilarity = []

    for kolom in daftar_kolom:
        max_nilai = 0
        for kata in daftar_kata:
            nilai_jaccard_coefficient = jaccard_coefficient(kolom, kata)
            if nilai_jaccard_coefficient > max_nilai:
                max_nilai = nilai_jaccard_coefficient
        data = {'nama_kolom': kolom, 'nilai_simmilarity': max_nilai}
        daftar_kolom_simmilarity.append(data)

    return daftar_kolom_simmilarity