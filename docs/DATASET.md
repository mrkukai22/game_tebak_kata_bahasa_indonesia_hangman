# Ringkasan Dataset

## Statistik Struktural

- Versi dataset: **3.1.0**
- Kategori: **24**
- Entri: **2.059**
- Frasa: **397**
- Format: huruf kecil `a-z`; satu spasi dipakai sebagai pemisah frasa
- Struktur: `kategori -> level 1/2/3 -> list jawaban`

Validator default sengaja hanya menampilkan statistik umum. Rincian jumlah
setiap kategori tersedia melalui:

```powershell
python tools\validate_bank.py --details
```

## Aturan Integritas

- Semua kategori wajib memiliki level 1, 2, dan 3.
- Setiap level wajib berisi minimal satu jawaban.
- Daftar jawaban wajib terurut A–Z.
- Jawaban tidak boleh duplikat di dalam kategori, termasuk lintas level.
- Jawaban dapat muncul pada kategori berbeda jika konteksnya relevan.
- Jawaban tidak boleh sama persis dengan nama kategorinya sendiri.
- Metadata versi, total, frasa, dan jumlah per kategori harus cocok dengan
  hasil perhitungan aktual.

## Normalisasi Release 3.1.0

- Menghapus jawaban tautologis seperti nama kategori yang menjadi jawabannya
  sendiri.
- Mengganti beberapa istilah dengan bentuk Bahasa Indonesia yang lebih jelas,
  misalnya `email` menjadi `surel` dan `browser` menjadi `peramban`.
- Mengganti nama olahraga yang lebih baku, seperti `badminton` menjadi
  `bulu tangkis` dan `pingpong` menjadi `tenis meja`.
- Melengkapi nama mata pelajaran yang sebelumnya hanya berupa fragmen, seperti
  `arab` menjadi `bahasa arab`.

## Sumber dan Atribusi

Kandidat awal berasal dari Contek Sambung Kata. Atribusi yang dipertahankan:

**By MizuuDev Tim NepuhSoft**

Data tambahan dikurasi untuk kategori permainan dan tidak diklaim sebagai
salinan basis data resmi KBBI.
