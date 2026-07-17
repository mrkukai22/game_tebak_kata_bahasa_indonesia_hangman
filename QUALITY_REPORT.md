# Quality Report — Release 3.1.0

## Ringkasan Audit

Release ini merupakan hasil audit ulang menyeluruh terhadap kode, data,
validator, test suite, dokumentasi, keamanan input terminal, dan konsistensi
versi. Istilah *production grade* digunakan sesuai ruang lingkup aplikasi
konsol akademik lokal, bukan layanan internet multi-user.

## Perbaikan Utama

- Validator default tidak lagi menampilkan statistik satu kategori tertentu.
- Metadata kategori khusus diganti dengan `jumlah_per_kategori` yang generik.
- Nama pemain menolak karakter kontrol/ANSI dan dinormalisasi konsisten.
- Leaderboard hanya menerima kategori resmi, jawaban valid, skor positif,
  dan timestamp berzona waktu.
- Siklus random dipisahkan berdasarkan kategori dan kesulitan.
- Jawaban tidak diulang sebelum pool kategori-level selesai.
- Domain Hangman memvalidasi state awal, set huruf, dan progres gambar.
- Jawaban yang sama dengan nama kategorinya sendiri dihapus dan ditolak.
- Sejumlah istilah data dinormalisasi ke Bahasa Indonesia yang lebih jelas.
- Instruksi dan halaman Tentang mengambil statistik aktual, bukan angka tetap.

## Hasil Verifikasi

- **52 automated tests lulus.**
- **99% branch coverage** pada package `game` dengan 0 statement tidak teruji.
- Validator bank data lulus.
- Compile seluruh file Python lulus.
- Smoke test CLI dan aplikasi lulus.
- Leaderboard distribusi awal kosong.
- Tidak ada validator lama, `__pycache__`, atau `.pyc` pada paket ZIP final.

## Catatan Kejujuran

Tidak ada perangkat lunak yang dapat dijamin “100% bebas bug”. Release ini
sudah memenuhi standar kuat untuk proyek konsol akademik: validasi ketat,
pemisahan tanggung jawab, persistence atomik, pengujian luas, dokumentasi,
dan hasil audit yang dapat direproduksi.


## Verifikasi Lintas Lingkungan

- Windows, Python 3.12.0: automated test, validator, dan manual test lulus.
- Google Colab, Python 3.12.13: 52 automated test, validator, smoke test,
  dan keluar normal lulus.
