import json
import os

class ColumnDetector():
    def ekstraksi_semua_kolom_json(self, file_name_json):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, '..', 'databases/column_detector',file_name_json)

        with open(json_path,'r') as file:
            data = json.load(file)

        set_kolom = set()
        for tabel in data['entitas']:
            for kolom in data['entitas'][tabel]:
                set_kolom.add(kolom)

        daftar_kolom = list(set_kolom)
        return daftar_kolom

    def tokenisasi(kalimat_ternormalisasi):
        kumpulan_kata = kalimat_ternormalisasi.split()
        return kumpulan_kata

    def jaccard_coefficient(daftar_kata, daftar_kolom):
        pass

    def normalisasi(kalimat):
        pass

    def filter(daftar_kolom_simmilarity, threshold):
        daftar_kolom_select = []
        for kolom in daftar_kolom_simmilarity:
            if kolom['nilai_simmilarity']>threshold:
                daftar_kolom_select.append(kolom['nama_kolom'])
        return daftar_kolom_select

    def detektor_kolom(self, kalimat, file_database_json):
        daftar_kolom = self.ekstraksi_semua_kolom_json(file_json=file_database_json)
        kalimat_ternormalisasi = self.normalisasi(kalimat=kalimat)
        daftar_kata = self.tokenisasi(kalimat_ternormalisasi=kalimat_ternormalisasi)
        daftar_kolom_simmilarity = self.jaccard_coefficient(daftar_kata=daftar_kata, daftar_kolom=daftar_kolom)
        daftar_kolom_select = filter(daftar_kolom_simmilarity=daftar_kolom_simmilarity,threshold=0.55)
        return daftar_kolom_select

detector = ColumnDetector()
daftar_kolom = detector.ekstraksi_semua_kolom_json(file_name_json='inventori_1.json')
