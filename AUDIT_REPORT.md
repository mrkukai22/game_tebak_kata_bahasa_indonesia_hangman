# Audit Report — Release 3.1.0

## Latar Belakang

Audit ulang dilakukan karena validator release sebelumnya menampilkan
`Negara: 195` pada ringkasan default. Baris tersebut tidak salah secara data,
tetapi desainnya tidak konsisten: satu kategori diperlakukan khusus, sedangkan
23 kategori lain tidak. Release ini menghapus special case tersebut dan
mengaudit komponen lain dengan prinsip yang sama.

## Temuan dan Perbaikan

### 1. Validator dan Metadata

- Output default sekarang hanya menampilkan statistik struktural umum:
  kategori, entri, frasa, dan versi.
- Rincian kategori dipindahkan ke opsi `--details`.
- Output mesin tersedia melalui `--json`.
- Metadata `jumlah_negara` dihapus.
- Metadata `jumlah_kata` diganti menjadi `jumlah_entri` karena bank juga
  memuat frasa.
- Ditambahkan `jumlah_per_kategori` agar semua kategori divalidasi setara.

### 2. Integritas Dataset

- Menghapus tujuh jawaban yang sama persis dengan nama kategorinya sendiri.
- Menambahkan aturan validator agar tautologi tersebut tidak kembali masuk.
- Menormalkan istilah seperti `email` → `surel`, `browser` → `peramban`,
  `badminton` → `bulu tangkis`, dan `pingpong` → `tenis meja`.
- Melengkapi fragmen mata pelajaran menjadi nama yang lebih jelas.
- Seluruh daftar wajib terurut A–Z dan unik di dalam kategori.

### 3. Keamanan Input Lokal

- Nama pemain menolak karakter kontrol dan escape sequence ANSI.
- Nama dinormalisasi sebelum ditampilkan atau disimpan.
- Leaderboard menolak kategori tidak dikenal, jawaban tidak valid, skor nol
  atau negatif, boolean yang menyamar sebagai integer, dan timestamp tanpa
  zona waktu.

### 4. Random Selection

- Riwayat jawaban sekarang dipisahkan per kategori dan tingkat kesulitan.
- Jawaban tidak berulang sampai seluruh pool terkait telah digunakan.
- Setelah pool habis, siklus baru dimulai secara eksplisit.

### 5. Domain Hangman

- State awal set huruf divalidasi secara menyeluruh.
- State menang dan kalah bersamaan ditolak.
- Progres gambar Hangman bersifat monoton dan mencapai tahap akhir tepat saat
  kesempatan habis.
- Input bukan string diperlakukan sebagai tebakan tidak valid, bukan crash.

### 6. Persistence

- Leaderboard tetap memakai atomic write.
- File sementara dibersihkan baik saat sukses maupun gagal.
- Distribusi release dimulai dengan leaderboard kosong.

## Hasil Verifikasi

- Automated tests: **52/52 lulus**.
- Package `game`: **99% branch coverage**.
- Seluruh **601 statement package teruji**; tidak ada baris yang miss.
- Compile seluruh file Python: **lulus**.
- Validator text, details, dan JSON: **lulus**.
- Smoke test aplikasi: **lulus**.
- Version consistency (`pyproject`, package, aplikasi, dataset): **lulus**.
- Artefak stale (`__pycache__`, `.pyc`, `.coverage`, log runtime): dihapus
  dari ZIP final.

## Batas Produksi

Release ini production-grade untuk aplikasi konsol akademik lokal. Ia bukan
layanan multi-user, tidak memiliki locking antarbanyak proses, dan belum
menggantikan acceptance test manual di perangkat presentasi. Tidak ada klaim
bahwa perangkat lunak dapat dijamin 100% bebas bug.
