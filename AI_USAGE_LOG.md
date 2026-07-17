# AI Usage Log — Proyek Akhir

## Game Tebak Kata Bahasa Indonesia

> Dokumen ini mencatat penggunaan AI secara jujur. Bagian yang belum memiliki
> bukti tidak ditulis seolah-olah sudah dilakukan. Refleksi pribadi tetap wajib
> dikonfirmasi sendiri oleh setiap anggota sebelum submission.

## 1. Identitas

- **Proyek:** Game Tebak Kata Bahasa Indonesia
- **Mata kuliah:** Algoritma dan Pemrograman
- **Tanggal mulai:** 16 Juni 2026
- **Tanggal pembaruan log:** 17 Juli 2026
- **Tanggal selesai final:** Belum selesai pada saat log ini dibuat
- **Anggota:**
  1. Ariq Gymnastiar Prabowo — 0102521704
  2. Andri — 0102520032
- **AI yang digunakan:** ChatGPT

## 2. Ringkasan Penggunaan AI

AI digunakan untuk membantu analisis requirement, penyusunan struktur bank
kata, implementasi dan refactor kode, debugging, validasi data, automated
testing, dokumentasi teknis, serta penyusunan test plan.

### Estimasi kontribusi

- **Kode yang dibuat, direfaktor, atau disarankan dengan bantuan AI:** sekitar 90%
- **Kode yang ditulis atau diubah langsung oleh anggota:** sekitar 10%

Angka tersebut merupakan estimasi berdasarkan riwayat pengerjaan, bukan
pengukuran otomatis dari Git. Mayoritas implementasi dan refactor dibuat
dengan bantuan AI. Kontribusi manusia terutama berada pada penentuan
requirement, pemilihan data, eksekusi program, pengujian, evaluasi hasil,
pelaporan bug, penolakan output yang tidak masuk akal, dan keputusan revisi.

## 3. Kontribusi yang Terverifikasi

### Ariq Gymnastiar Prabowo

- menentukan studi kasus dan arah fitur;
- memilih penggunaan bank data lokal tanpa API;
- menentukan kategori dan tingkat kesulitan;
- menjalankan script dan program pada Windows;
- melaporkan error dan traceback;
- memeriksa konsistensi jumlah data;
- menemukan inkonsistensi validator pada kategori Negara;
- meminta audit dan perbaikan ulang;
- menjalankan 52 automated test;
- menjalankan validator bank data;
- melakukan manual acceptance test;
- mengumpulkan bukti screenshot Windows;
- membuat dan mempublikasikan repository GitHub.

### Andri

- review tampilan dan kemudahan penggunaan;
- menguji alur permainan dan leaderboard;
- membantu memeriksa laporan dan slide;
- menyiapkan bagian presentasi tentang fitur dan demo;
- membantu menjawab pertanyaan dasar tentang alur game.
- menjalankan pengujian Google Colab;
- mengumpulkan bukti Colab;

## 4. Detail Interaksi dengan AI

### Interaksi 1 — Perancangan Bank Kata

- **Tujuan:** menentukan struktur kategori, tingkat kesulitan, dan format JSON.
- **Saran AI:** menggunakan struktur `kategori -> level -> list jawaban`.
- **Yang digunakan:** struktur tersebut digunakan pada bank data final.
- **Keputusan manusia:** memilih kategori, level, dan penggunaan data lokal.
- **Pelajaran:** struktur data harus dipilih sesuai pola akses program.

### Interaksi 2 — Sinkronisasi Sumber Kandidat

- **Tujuan:** mengambil kandidat kata A–Z.
- **Saran AI:** membuat script pengunduhan dan parsing.
- **Kesalahan AI:** parser awal mengasumsikan struktur JSON tertentu.
- **Temuan manusia:** script gagal dan traceback dilaporkan.
- **Perbaikan:** parser dibuat lebih fleksibel.
- **Pelajaran:** struktur data eksternal tidak boleh diasumsikan.

### Interaksi 3 — Kurasi Bank Data

- **Tujuan:** membuang kata salah kategori, fragmen, dan data ambigu.
- **Saran AI:** membuat validator dan aturan kurasi.
- **Keputusan manusia:** meminta perluasan kategori dan dukungan frasa.
- **Hasil:** 24 kategori, 2.059 entri, dan 397 frasa pada release 3.1.0.
- **Pelajaran:** jumlah data besar tidak otomatis berarti data berkualitas.

### Interaksi 4 — Implementasi Game

- **Tujuan:** membuat Hangman display, scoring, leaderboard, random selection,
  dan string matching.
- **Saran AI:** membuat struktur modular aplikasi.
- **Yang digunakan:** modul aplikasi, domain, UI, data manager, validator, dan
  leaderboard.
- **Verifikasi manusia:** program dijalankan dan diuji pada Windows.
- **Pelajaran:** kode AI tetap harus diperiksa dan dijalankan.

### Interaksi 5 — Perbaikan Menyerah dan Scoring

- **Tujuan:** memperbaiki kondisi menyerah dan penggunaan pengali skor.
- **Saran AI:** menambahkan `forfeit()` dan memakai `pengali_skor`.
- **Yang digunakan:** skor nol saat menyerah, kesempatan nol, Hangman penuh,
  dan pengali level digunakan.
- **Verifikasi manusia:** skenario menyerah diuji manual.
- **Pelajaran:** test harus memeriksa perilaku, bukan hanya program berjalan.

### Interaksi 6 — Refactor dan Hardening

- **Tujuan:** meningkatkan modularitas dan reliability.
- **Saran AI:** memisahkan application, domain, UI, validation, persistence,
  logging, dan CLI.
- **Yang digunakan:** release 3.0.0 dan hardening 3.1.0.
- **Temuan manusia:** validator masih memperlakukan Negara sebagai special case.
- **Perbaikan:** validator dibuat kategori-netral.
- **Pelajaran:** output yang benar secara data belum tentu konsisten secara desain.

### Interaksi 7 — Automated Testing

- **Tujuan:** menguji logika game, validator, leaderboard, UI, dan release.
- **Saran AI:** membuat unit test dan integration test.
- **Yang digunakan:** 52 automated test.
- **Verifikasi manusia:** test dijalankan pada Windows dan Google Colab.
- **Hasil:** seluruh test lulus.
- **Pelajaran:** test harus dijalankan pada paket final.

### Interaksi 8 — Manual Acceptance Testing

- **Tujuan:** membuktikan fitur utama dari sisi pengguna.
- **Saran AI:** menyusun skenario menang, kalah, menyerah, frasa, menu
  informasi, dan ganti nama.
- **Yang digunakan:** lima kelompok skenario manual.
- **Verifikasi manusia:** Ariq menjalankan dan mengumpulkan screenshot.
- **Hasil:** seluruh skenario lulus.
- **Pelajaran:** automated test tidak menggantikan pengujian langsung.

### Interaksi 9 — Pengujian Google Colab

- **Tujuan:** memastikan aplikasi berjalan pada lingkungan Google Colab.
- **Saran AI:** membuat notebook pengujian.
- **Kesalahan AI:** cell laporan awal lupa mengimpor modul `platform`.
- **Temuan manusia:** muncul `NameError`.
- **Perbaikan:** notebook v2 mengimpor dependensi pada cell terkait.
- **Hasil:** Python 3.12.13, automated test, validator, smoke test, dan keluar
  normal seluruhnya lulus.
- **Pelajaran:** notebook juga perlu diuji seperti source code biasa.

### Interaksi 10 — Dokumentasi dan GitHub

- **Tujuan:** menyiapkan repository dan dokumentasi submission.
- **Saran AI:** menyusun README, test report, audit report, dan panduan Git.
- **Yang digunakan:** repository publik versi 3.1.0.
- **Verifikasi manusia:** Ariq melakukan commit dan publish ke GitHub.
- **Pelajaran:** dokumentasi harus mengikuti kondisi release aktual.

## 5. Kesalahan atau Kelemahan AI yang Ditemukan

1. Parser awal salah mengasumsikan struktur JSON sumber.
2. Klaim awal kategorisasi data sempat lebih luas daripada proses sebenarnya.
3. Penambahan data pertama terlalu sedikit.
4. Kategori negara sempat hanya memiliki sedikit entri.
5. Test dan README sempat memakai jumlah data versi lama.
6. Validator sempat menampilkan kategori Negara sebagai special case.
7. Istilah *production-grade* sempat digunakan terlalu absolut.
8. Notebook Colab awal lupa mengimpor modul `platform`.
9. Beberapa dokumen sempat belum sinkron dengan paket terakhir.

## 6. Cara Anggota Memverifikasi Kode

- menjalankan aplikasi secara langsung;
- menjalankan 52 automated test;
- menjalankan validator bank data;
- memeriksa leaderboard;
- menguji menang, kalah, dan menyerah;
- menguji jawaban frasa;
- menguji menu informasi dan ganti nama;
- menjalankan aplikasi pada Windows;
- menjalankan aplikasi pada Google Colab;
- memeriksa repository GitHub;
- membandingkan output dengan requirement dosen.

## 7. Pembagian Tugas Final

Pembagian berikut merupakan pembagian tanggung jawab untuk penyelesaian akhir,
bukan klaim bahwa seluruhnya sudah selesai.

### Ariq Gymnastiar Prabowo

- koordinator proyek;
- integrasi source code dan bank data;
- pengujian Windows dan Google Colab;
- dokumentasi teknis;
- pengelolaan repository GitHub;
- penyusunan laporan dan bukti submission.

### Andri

- review antarmuka dan kemudahan penggunaan;
- pengujian alur permainan dan leaderboard;
- review isi laporan;
- menyiapkan bagian demo presentasi;
- membantu Q&A fitur utama.

## 8. Refleksi Pribadi

Bagian ini **wajib ditulis atau dikonfirmasi sendiri oleh masing-masing
anggota**, karena refleksi pribadi tidak boleh dikarang oleh AI.

### Ariq Gymnastiar Prabowo

- Bagian tersulit:
- Bagian kode yang paling dipahami:
- Kesalahan AI yang berhasil ditemukan:
- Hal yang akan dilakukan berbeda pada proyek berikutnya:

### Andri

- Bagian tersulit:
- Bagian kode yang paling dipahami:
- Kesalahan AI yang berhasil ditemukan:
- Hal yang akan dilakukan berbeda pada proyek berikutnya:

## 9. Pernyataan Integritas

Kami menyatakan bahwa penggunaan AI pada proyek ini dicatat secara transparan.
Kami tidak mengklaim bahwa seluruh kode ditulis secara mandiri. Kami memahami
bahwa mayoritas implementasi menggunakan bantuan AI, sedangkan anggota
bertanggung jawab atas requirement, keputusan akhir, pengujian, review,
perbaikan, dokumentasi, dan pemahaman kode yang dikumpulkan.

Sebelum submission, setiap anggota wajib membaca kembali source code,
mengonfirmasi pembagian tugas, mengisi refleksi pribadi, mampu menjelaskan
fitur dan algoritma, serta menyetujui isi AI Usage Log.
