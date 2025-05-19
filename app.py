kata = 'abc'
tabel = ['karyawan','pembayaran','transaksi','produk']

cek = False
for nama_tabel in tabel:
    if nama_tabel in kata:
        cek = True
        break
    
cek2 = any(nama_tabel for nama_tabel in tabel if nama_tabel in kata)


print(cek2)