import json
import re

class ColumnDetector():

    def ekstraksi_semua_kolom_di_tabel_tertentu(self, database, tabel):
        set_kolom = set()
        
        for kolom in database['entitas'][tabel]:
            set_kolom.add(kolom)    

        daftar_kolom = list(set_kolom)
        return daftar_kolom
    
    
    def ekstraksi_semua_tabel_json(self, database):
        set_tabel = set()
        for tabel in database['entitas']:
            set_tabel.add(tabel)

        daftar_tabel = list(set_tabel)
        return daftar_tabel


    def tokenisasi(self, kalimat_ternormalisasi):
        daftar_kata = kalimat_ternormalisasi.split()
        return daftar_kata
    
    

    def normalisasi(self,kalimat):

        kalimat = kalimat.lower()
        kalimat = re.sub(r'[^a-z\s]', '', kalimat)        
        kalimat = re.sub(r'\s+', ' ', kalimat).strip()
        return kalimat
    
    
    
    def jaccard_coefficient(self, kolom, kata):
        irisan = set(kata) & set(kolom)
        gabungan = set(kata) | set(kolom)
        skor = len(irisan) / len(gabungan) if gabungan else 0
        return skor
    
    
    
    def set_daftar_kolom_simmilarity(self, daftar_kolom, daftar_kata):
        daftar_kolom_simmilarity = []

        for kolom in daftar_kolom:
            max_nilai = 0
            for kata in daftar_kata:
                nilai_jaccard_coefficient = self.jaccard_coefficient(kolom, kata)
                if nilai_jaccard_coefficient > max_nilai:
                    max_nilai = nilai_jaccard_coefficient
            data = {'nama_kolom': kolom, 'nilai_simmilarity': max_nilai}
            daftar_kolom_simmilarity.append(data)

        return daftar_kolom_simmilarity
    
    
    def set_daftar_tabel_simmilarity(self, daftar_tabel, daftar_kata):
        daftar_tabel_simmilarity = []

        for tabel in daftar_tabel:
            max_nilai = 0
            for kata in daftar_kata:
                nilai_jaccard_coefficient = self.jaccard_coefficient(tabel, kata)
                if nilai_jaccard_coefficient > max_nilai:
                    max_nilai = nilai_jaccard_coefficient
            data = {'nama_tabel': tabel, 'nilai_simmilarity': max_nilai}
            daftar_tabel_simmilarity.append(data)

        return daftar_tabel_simmilarity



    def filter_kolom(self, daftar_kolom_simmilarity, threshold):
        daftar_kolom_select = []
        for kolom in daftar_kolom_simmilarity:
            if kolom['nilai_simmilarity']>threshold:
                daftar_kolom_select.append(kolom['nama_kolom'])
        return daftar_kolom_select

    def filter_tabel(self, daftar_tabel_simmilarity, threshold):
        daftar_tabel_select = []
        for tabel in daftar_tabel_simmilarity:
            if tabel['nilai_simmilarity']>threshold:
                daftar_tabel_select.append(tabel['nama_tabel'])
        return daftar_tabel_select

    def detect(self, kalimat, filepath_database_json):
        with open(filepath_database_json, 'r') as file:
            database = json.load(file)
            
        kalimat_ternormalisasi = self.normalisasi(kalimat=kalimat)
        daftar_kata = self.tokenisasi(kalimat_ternormalisasi=kalimat_ternormalisasi)
        
        
        
        daftar_tabel = self.ekstraksi_semua_tabel_json(database)
        daftar_tabel_simmilarity = self.set_daftar_tabel_simmilarity(daftar_kata=daftar_kata, daftar_tabel=daftar_tabel)
        daftar_tabel_select = self.filter_tabel(daftar_tabel_simmilarity=daftar_tabel_simmilarity,threshold=0.8)
        
        daftar_kolom_teridentifikasi = []
        for tabel in daftar_tabel_select:
            daftar_kolom = self.ekstraksi_semua_kolom_di_tabel_tertentu(database, tabel) 
            daftar_kolom_simmilarity = self.set_daftar_kolom_simmilarity(daftar_kata=daftar_kata, daftar_kolom=daftar_kolom)
            daftar_kolom_select = self.filter_kolom(daftar_kolom_simmilarity=daftar_kolom_simmilarity,threshold=0.8)
            for kolom in daftar_kolom_select:
                daftar_kolom_teridentifikasi.append(kolom)
        
        if len(daftar_kolom_teridentifikasi)==0 and len(daftar_tabel_select)>0:
            return ['*']
        elif len(daftar_kolom_teridentifikasi)==0 and len(daftar_tabel_select)==0:
            return ['NOCOLUMN']
        else:
            return daftar_kolom_teridentifikasi

    
    
    
