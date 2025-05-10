class ColumnDetector():
    def ekstraksi_semua_kolom_json(file_json):
        pass

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