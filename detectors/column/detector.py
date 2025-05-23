import json

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
        #Tujuan: mengubah kalimat menjadi daftar kata. 
        #Misalnya, kalimat "tambahkan data baru di produk", daftar kata nya adalah ['tambahkan','data','baru','di','produk']
        #Gunakan function split()
        #Tugas: tambahkan code untuk tokenisasi. Jangan lupa mengapus pass
        pass

    def set_daftar_kolom_simmilarity(self, daftar_kata, daftar_kolom):
        #Tujuan: memberikan nilai ke setiap kolom database. Nilai ini merepresentasikan nilai maksimal jaccard coefficient 
        #Tugas: tambahkan code untuk set_daftar_kolom_simmilarity. Lihat di catatan tentang set_daftar_kolom_simmilarity (di googleclassroom).
        #Jangan lupa mengapus pass
        pass

    def normalisasi(self,kalimat):
        #Tujuan: menormalisasi kalimat. Normalisasi disini maksudnya :
        # 1. menyeragamkan huruf menjadi lowercase, Misal: kalimat "Tambahkan data Produk" menjadi "tambahkan data produk"
        # 2. menghapus karakter non abjad dan non spasi, Misal: kalimat "tambahkan data produk!" menjadi "tambahkan data produk" 
        # 3. menjadikan dua spasi atau lebih menjadi 1 spasi. Misal: kalimat "tambahkan    data produk" menjadi "tambahkan data produk" 
        #Tugas: tambahkan code untuk normalisasi. Jangan lupa mengapus pass
        pass

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
