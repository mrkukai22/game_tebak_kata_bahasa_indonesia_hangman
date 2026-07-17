# AI Usage Log — Proyek Akhir

## Game Tebak Kata Bahasa Indonesia

> Dokumen ini mencatat penggunaan AI secara jujur, transparan, dan dapat ditelusuri.
> Informasi yang ditulis sebagai fakta didasarkan pada proses pengerjaan, hasil pengujian,
> dokumentasi proyek, dan repository GitHub. Refleksi pribadi tidak ditulis oleh AI dan
> wajib diisi atau dikonfirmasi sendiri oleh setiap anggota sebelum submission.

---

## 1. Identitas Proyek

- **Nama proyek:** Game Tebak Kata Bahasa Indonesia
- **Mata kuliah:** Algoritma dan Pemrograman
- **Dosen pengampu:** Tri Aji Nugroho, S.T., M.T.
- **Program studi:** Informatika
- **Universitas:** Universitas Al Azhar Indonesia
- **Tanggal mulai:** 16 Juni 2026
- **Tanggal selesai dokumentasi final:** 17 Juli 2026
- **Versi aplikasi:** 3.1.0
- **Repository:** https://github.com/mrkukai22/game_tebak_kata_bahasa_indonesia_hangman

### Anggota

1. **Ariq Gymnastiar Prabowo** — 0102521704
2. **Andri** — 0102520032

### AI yang Digunakan

- **Platform:** ChatGPT
- **Bentuk penggunaan:** analisis kebutuhan, perancangan, implementasi, pemfaktoran ulang kode, pelacakan kesalahan, validasi data, pengujian, audit, dan dokumentasi
- **Jumlah interaksi utama yang didokumentasikan:** 10 interaksi

---

## 2. Ringkasan Penggunaan AI

AI digunakan sebagai mitra pengembangan untuk membantu:

1. menyusun struktur bank kata;
2. merancang arsitektur modular;
3. mengimplementasikan fitur inti permainan;
4. memperbaiki bug dan kondisi batas;
5. memperkuat validasi data dan input;
6. menyusun pengujian otomatis;
7. menyiapkan pengujian manual;
8. menyiapkan pengujian Google Colab;
9. menyusun dokumentasi teknis;
10. menyiapkan repository GitHub.

### Estimasi Kontribusi

- **Kode yang dibuat, direfaktor, atau disarankan dengan bantuan AI:** sekitar 90%
- **Kode yang ditulis atau diubah langsung oleh anggota:** sekitar 10%

Persentase tersebut merupakan estimasi berdasarkan riwayat pengerjaan, bukan pengukuran
otomatis dari Git. Mayoritas implementasi dan pemfaktoran ulang kode dilakukan dengan
bantuan AI. Kontribusi manusia terutama berada pada:

- penentuan studi kasus;
- pemilihan requirement;
- keputusan fitur;
- pemilihan dan kurasi data;
- eksekusi program;
- pengujian Windows;
- pengujian Google Colab;
- pemeriksaan hasil;
- pelaporan bug;
- penolakan output yang tidak masuk akal;
- keputusan revisi;
- publikasi repository.

---

## 3. Kontribusi Anggota yang Telah Dikonfirmasi

### 3.1 Ariq Gymnastiar Prabowo

- menentukan studi kasus dan arah fitur;
- memilih penggunaan bank data lokal tanpa API;
- menentukan kategori dan tingkat kesulitan;
- menjalankan script dan program pada Windows;
- melaporkan error dan traceback;
- memeriksa konsistensi jumlah data;
- menemukan inkonsistensi validator pada kategori Negara;
- meminta audit dan perbaikan ulang;
- menjalankan 52 pengujian otomatis;
- menjalankan validator bank data;
- melakukan pengujian penerimaan manual;
- mengumpulkan bukti screenshot Windows;
- menjalankan pengujian Google Colab;
- mengelola dokumentasi teknis;
- membuat dan mempublikasikan repository GitHub;
- menyusun laporan dan bukti submission.

### 3.2 Andri

- meninjau tampilan dan kemudahan penggunaan;
- menguji alur permainan dan leaderboard;
- membantu meninjau isi laporan dan slide;
- menyiapkan bagian presentasi tentang fitur dan demo;
- membantu menyiapkan jawaban untuk pertanyaan dasar mengenai alur permainan;
- mengumpulkan dan merapikan bukti pengujian Google Colab.

> **Catatan integritas:** Setiap poin kontribusi Andri harus dibaca dan dikonfirmasi
> oleh Andri sebelum submission. Poin yang tidak benar-benar dilakukan harus dihapus
> atau diperbaiki.

---

## 4. Detail Interaksi dengan AI

### Interaksi 1 — Perancangan Struktur Bank Kata

- **Periode:** Juni 2026
- **Ringkasan prompt:** Meminta rekomendasi struktur data untuk bank kata yang memiliki kategori dan tiga tingkat kesulitan.
- **Respons AI:** Menyarankan struktur `kategori -> level -> list jawaban`.
- **Yang digunakan:** Struktur tersebut digunakan pada `data/bank_kata.json`.
- **Modifikasi/keputusan anggota:** Anggota menentukan kategori, tingkat kesulitan, penggunaan data lokal, dan keputusan untuk tidak menggunakan API.
- **Verifikasi:** Struktur diperiksa menggunakan validator bank data.
- **Pelajaran:** Struktur data harus dipilih berdasarkan pola akses program.
- **Bukti:** `data/bank_kata.json`, `tools/validate_bank.py`.

### Interaksi 2 — Sinkronisasi Sumber Kandidat Kata

- **Periode:** Juni 2026
- **Ringkasan prompt:** Meminta bantuan membuat script untuk mengambil dan memproses kandidat kata dari sumber eksternal.
- **Respons AI:** Menyarankan script pengunduhan dan parsing.
- **Masalah yang ditemukan:** Parser awal mengasumsikan struktur JSON tertentu sehingga script gagal.
- **Modifikasi/perbaikan anggota:** Traceback dilaporkan, struktur sumber diperiksa kembali, dan parser dibuat lebih fleksibel.
- **Verifikasi:** Script dijalankan ulang dan hasilnya diperiksa.
- **Pelajaran:** Struktur sumber eksternal tidak boleh diasumsikan tanpa pemeriksaan.
- **Bukti:** riwayat debugging dan dokumentasi dataset.

### Interaksi 3 — Kurasi dan Validasi Bank Data

- **Periode:** Juni–Juli 2026
- **Ringkasan prompt:** Meminta bantuan menyusun aturan kurasi dan validator untuk membuang fragmen, duplikat, dan data salah kategori.
- **Respons AI:** Menyarankan aturan validasi struktur, format, urutan A–Z, duplikasi, dan metadata.
- **Yang digunakan:** Validator bank data dan aturan kurasi.
- **Modifikasi/keputusan anggota:** Anggota meminta perluasan kategori, penambahan frasa, dan perbaikan distribusi data.
- **Hasil akhir:** 24 kategori, 2.059 entri, dan 397 frasa pada versi 3.1.0.
- **Verifikasi:** `python tools/validate_bank.py`.
- **Pelajaran:** Jumlah data besar tidak otomatis berarti data berkualitas.
- **Bukti:** `data/bank_kata.json`, `tools/validate_bank.py`, `docs/DATASET.md`.

### Interaksi 4 — Implementasi Fitur Inti Permainan

- **Periode:** Juni–Juli 2026
- **Ringkasan prompt:** Meminta implementasi permainan Hangman dengan scoring, leaderboard, pemilihan acak, dan pencocokan huruf.
- **Respons AI:** Menyarankan pemisahan modul aplikasi, domain permainan, antarmuka, pengelola data, validator, dan leaderboard.
- **Yang digunakan:** Arsitektur modular pada folder `game/`.
- **Modifikasi/keputusan anggota:** Anggota menentukan requirement akhir, tingkat kesulitan, dukungan frasa, dan perilaku menyerah.
- **Verifikasi:** Program dijalankan langsung pada Windows.
- **Pelajaran:** Kode yang dihasilkan AI tetap harus diperiksa dan dijalankan.
- **Bukti:** `main.py`, `game/`, `README.md`.

### Interaksi 5 — Perbaikan Kondisi Menyerah dan Perhitungan Skor

- **Periode:** Juli 2026
- **Ringkasan prompt:** Meminta perbaikan logika ketika pemain menyerah dan memastikan pengali tingkat kesulitan digunakan.
- **Respons AI:** Menyarankan method `forfeit()` dan penggunaan `pengali_skor`.
- **Yang digunakan:** Menyerah menghasilkan skor nol, kesempatan menjadi nol, dan tampilan Hangman selesai.
- **Modifikasi/keputusan anggota:** Anggota meminta agar skor hanya disimpan ketika pemain menang.
- **Verifikasi:** Skenario menyerah diuji secara manual dan melalui pengujian otomatis.
- **Pelajaran:** Pengujian harus memeriksa perilaku sistem, bukan hanya memastikan program dapat berjalan.
- **Bukti:** `game/hangman.py`, `tests/test_hangman.py`, bukti pengujian manual.

### Interaksi 6 — Pemfaktoran Ulang dan Penguatan Keandalan

- **Periode:** Juli 2026
- **Ringkasan prompt:** Meminta audit arsitektur dan penguatan kualitas kode sebelum release.
- **Respons AI:** Menyarankan pemisahan application, domain, UI, validation, persistence, logging, dan CLI.
- **Yang digunakan:** Versi 3.0.0 dan penguatan versi 3.1.0.
- **Masalah yang ditemukan:** Validator masih memperlakukan kategori Negara sebagai perlakuan khusus.
- **Modifikasi/perbaikan anggota:** Validator diperbaiki agar kategori-netral.
- **Verifikasi:** Validator dan seluruh test dijalankan ulang.
- **Pelajaran:** Output yang benar secara data belum tentu konsisten secara desain.
- **Bukti:** `game/`, `tools/validate_bank.py`, `CHANGELOG.md`.

### Interaksi 7 — Pengujian Otomatis

- **Periode:** Juli 2026
- **Ringkasan prompt:** Meminta unit test dan integration test untuk logika permainan, validator, leaderboard, UI, dan CLI.
- **Respons AI:** Menyarankan rangkaian pengujian untuk kondisi normal, error, dan edge case.
- **Yang digunakan:** 52 pengujian otomatis.
- **Modifikasi/keputusan anggota:** Anggota menjalankan test pada paket release bersih dan meminta perbaikan ketika ada ketidakkonsistenan.
- **Verifikasi:** Test dijalankan pada Windows dan Google Colab.
- **Hasil:** 52/52 pengujian lulus.
- **Pelajaran:** Hasil pengujian harus berasal dari paket final yang benar-benar dijalankan.
- **Bukti:** `tests/`, `HASIL_TEST.txt`, `QUALITY_REPORT.md`.

### Interaksi 8 — Pengujian Penerimaan Manual

- **Periode:** 15–16 Juli 2026
- **Ringkasan prompt:** Meminta skenario manual untuk menang, kalah, menyerah, frasa, leaderboard, bantuan, dan ganti nama.
- **Respons AI:** Menyarankan test case dan expected output.
- **Yang digunakan:** Lima kelompok skenario manual.
- **Modifikasi/keputusan anggota:** Ariq menjalankan skenario pada perangkat Windows dan mengumpulkan screenshot.
- **Hasil:** Seluruh skenario utama lulus.
- **Pelajaran:** Pengujian otomatis tidak menggantikan pengujian langsung dari sisi pengguna.
- **Bukti:** `evidence/manual_test/`, `docs/MANUAL_TEST_REPORT.md`.

### Interaksi 9 — Pengujian Google Colab

- **Periode:** 17 Juli 2026
- **Ringkasan prompt:** Meminta notebook untuk memastikan aplikasi dapat dijalankan pada Google Colab.
- **Respons AI:** Menyarankan notebook pengujian environment, automated test, validator, smoke test, dan keluar normal.
- **Masalah yang ditemukan:** Cell awal lupa mengimpor modul `platform`, sehingga muncul `NameError`.
- **Modifikasi/perbaikan anggota:** Notebook diperbaiki agar setiap cell mengimpor dependensi yang dibutuhkan.
- **Verifikasi:** Seluruh cell dijalankan ulang pada Python 3.12.13.
- **Hasil:** Automated test, validator, smoke test, dan keluar normal dinyatakan lulus.
- **Pelajaran:** Notebook harus diuji seperti kode sumber biasa.
- **Bukti:** `evidence/colab/`, `docs/COLAB_TEST_REPORT.md`.

### Interaksi 10 — Dokumentasi dan Publikasi GitHub

- **Periode:** 17 Juli 2026
- **Ringkasan prompt:** Meminta bantuan menyiapkan README, laporan pengujian, audit, `.gitignore`, dan langkah publikasi GitHub.
- **Respons AI:** Menyarankan struktur dokumentasi, pemeriksaan file runtime, commit, dan publikasi repository.
- **Yang digunakan:** Repository publik versi 3.1.0.
- **Modifikasi/keputusan anggota:** Ariq memilih repository publik, melakukan commit, dan memeriksa struktur root.
- **Verifikasi:** Repository dibuka ulang dan struktur file diperiksa.
- **Pelajaran:** Dokumentasi harus mengikuti kondisi release aktual.
- **Bukti:** repository GitHub, `README.md`, `AUDIT_REPORT.md`, `TEST_PLAN.md`.

---

## 5. Kesalahan atau Kelemahan AI yang Ditemukan

1. Parser awal salah mengasumsikan struktur JSON sumber.
2. Klaim awal kategorisasi data sempat lebih luas daripada proses yang sebenarnya.
3. Penambahan data tahap awal terlalu sedikit.
4. Kategori Negara sempat hanya memiliki sedikit entri.
5. Test dan README sempat memakai jumlah data versi lama.
6. Validator sempat menampilkan kategori Negara sebagai perlakuan khusus.
7. Istilah *production-grade* sempat digunakan terlalu absolut.
8. Notebook Google Colab awal lupa mengimpor modul `platform`.
9. Beberapa dokumen sempat tidak sinkron dengan paket release terakhir.
10. Beberapa saran AI harus diperbaiki setelah diuji pada lingkungan nyata.

---

## 6. Cara Anggota Memverifikasi Kode dan Output AI

Anggota tidak langsung menerima output AI. Verifikasi dilakukan dengan:

- menjalankan aplikasi secara langsung;
- menjalankan 52 pengujian otomatis;
- menjalankan validator bank data;
- memeriksa file leaderboard;
- menguji kondisi menang, kalah, dan menyerah;
- menguji jawaban frasa;
- menguji input kosong dan tidak valid;
- menguji menu informasi dan ganti nama;
- menjalankan aplikasi pada Windows;
- menjalankan aplikasi pada Google Colab;
- membandingkan hasil dengan requirement dosen;
- memeriksa dokumentasi dan versi release;
- membuka repository GitHub setelah publikasi;
- menjalankan ulang pengujian setelah setiap perbaikan penting.

---

## 7. Pembagian Tugas Final

Pembagian tugas berikut mencatat pekerjaan yang telah dilakukan dan harus dikonfirmasi
oleh masing-masing anggota sebelum submission.

### Ariq Gymnastiar Prabowo

- koordinator proyek;
- penentuan requirement dan fitur;
- integrasi kode sumber dan bank data;
- pengujian Windows;
- pengujian Google Colab;
- pengujian penerimaan manual;
- dokumentasi teknis;
- pengelolaan repository GitHub;
- penyusunan laporan;
- pengumpulan bukti pengujian dan submission.

### Andri

- peninjauan antarmuka dan kemudahan penggunaan;
- pengujian alur permainan dan leaderboard;
- peninjauan isi laporan;
- peninjauan slide presentasi;
- persiapan bagian demo;
- persiapan tanya jawab fitur utama;
- pengumpulan dan perapian bukti Google Colab.

> **Konfirmasi wajib:** Andri harus memastikan seluruh tugas di atas benar-benar dilakukan.
> Poin yang tidak sesuai harus diubah atau dihapus.

---

## 8. Refleksi Pribadi

> **Bagian ini wajib diisi atau dikonfirmasi sendiri oleh masing-masing anggota.**
> AI tidak menulis refleksi pribadi anggota. Gunakan pengalaman nyata selama pengerjaan
> dan hindari jawaban yang terlalu umum.

### 8.1 Ariq Gymnastiar Prabowo

- **Bagian tersulit:**  
  Bagian tersulit bagi saya adalah menjaga konsistensi antara bank kata, validator, source code, hasil pengujian, dan dokumentasi ketika proyek terus mengalami perubahan. Setiap penambahan kategori atau revisi fitur dapat memengaruhi jumlah data, metadata, test, dan isi README, sehingga seluruh bagian harus diperiksa ulang agar tetap sinkron.

- **Bagian kode yang paling dipahami:**  
  Bagian kode yang paling saya pahami adalah alur utama permainan Hangman, mulai dari pemilihan kategori dan tingkat kesulitan, pemrosesan tebakan, pembaruan status permainan, perhitungan skor, hingga penyimpanan skor kemenangan ke leaderboard. Saya juga memahami bagaimana set digunakan untuk menyimpan huruf tebakan dan memeriksa kondisi kemenangan.

- **Kesalahan AI yang berhasil ditemukan sendiri:**  
  Kesalahan AI yang paling jelas saya temukan adalah asumsi struktur JSON yang tidak sesuai dengan sumber data, validator yang sempat memberikan perlakuan khusus pada kategori Negara, serta notebook Google Colab yang lupa mengimpor modul platform. Kesalahan tersebut baru terlihat setelah kode benar-benar dijalankan dan hasilnya dibandingkan dengan requirement proyek.

- **Hal yang akan dilakukan berbeda pada proyek berikutnya:**  
  Pada proyek berikutnya, saya akan menetapkan requirement, struktur data, aturan validasi, dan pembagian tugas secara lebih rinci sejak awal. Saya juga akan menggunakan Git dan commit kecil sejak tahap pertama, menjalankan test setiap selesai menambahkan fitur, serta memperbarui dokumentasi bersamaan dengan perubahan kode agar tidak terjadi ketidaksinkronan.

- **Pelajaran utama dari proyek ini:**  
  Pelajaran utama yang saya peroleh adalah bahwa hasil dari AI tidak dapat langsung dianggap benar. AI dapat mempercepat implementasi, tetapi manusia tetap harus memahami requirement, menjalankan kode, membaca error, memeriksa data, dan mengambil keputusan akhir.

### 8.2 Andri

- **Bagian tersulit:**  
  Bagian tersulit bagi saya adalah menguji alur permainan dari sudut pandang pengguna dan memastikan setiap kondisi menghasilkan output yang sesuai. Saya perlu mencoba kondisi menang, kalah, menyerah, tebakan berulang, input tidak valid, serta memeriksa apakah leaderboard hanya menyimpan skor kemenangan.

- **Bagian kode yang paling dipahami:**  
  Bagian kode yang paling saya pahami adalah alur menu dan interaksi pengguna, termasuk proses memasukkan nama, memilih kategori dan tingkat kesulitan, memberikan tebakan, menampilkan hasil permainan, serta membuka leaderboard. Saya memahami hubungan antara input pengguna, validasi, dan perubahan status permainan.

- **Kesalahan AI yang berhasil ditemukan sendiri:**  
  Saya tidak menemukan kesalahan teknis secara langsung pada source code, tetapi saya melihat bahwa beberapa penjelasan AI menggunakan istilah yang terlalu berlebihan dan belum tentu sesuai dengan kondisi aplikasi. Karena itu, saya ikut memeriksa kembali tampilan, alur permainan, dan isi dokumentasi agar lebih realistis.

- **Hal yang akan dilakukan berbeda pada proyek berikutnya:**  
  Pada proyek berikutnya, saya akan terlibat dalam pengujian sejak tahap awal, bukan hanya ketika program hampir selesai. Saya juga akan mencatat setiap test case, hasil aktual, dan masalah yang ditemukan secara langsung agar kontribusi pengujian lebih mudah dibuktikan dan proses perbaikan menjadi lebih terstruktur.

- **Pelajaran utama dari proyek ini:**  
  Pelajaran utama yang saya peroleh adalah bahwa pengujian dari sisi pengguna sama pentingnya dengan pembuatan kode. Program yang dapat dijalankan belum tentu sudah benar apabila kondisi khusus, input tidak valid, atau alur pengguna belum diuji secara menyeluruh.

---

## 9. Pernyataan Integritas

Kami menyatakan bahwa penggunaan AI pada proyek ini dicatat secara transparan.
Kami tidak mengklaim bahwa seluruh kode ditulis secara mandiri. Kami memahami
bahwa mayoritas implementasi menggunakan bantuan AI, sedangkan anggota tetap
bertanggung jawab atas:

- requirement;
- keputusan desain;
- pengujian;
- pemeriksaan output;
- perbaikan;
- dokumentasi;
- pemahaman terhadap kode yang dikumpulkan.

Sebelum submission, setiap anggota wajib:

1. membaca kembali kode sumber;
2. membaca AI Usage Log ini;
3. mengonfirmasi pembagian tugas;
4. mengisi refleksi pribadi;
5. memahami fitur dan algoritma;
6. siap menjelaskan keputusan teknis;
7. menyetujui isi dokumen.

---

## 10. Checklist Final AI Usage Log

- [x] Identitas proyek dan anggota lengkap
- [x] Tanggal mulai dan selesai tercantum
- [x] AI yang digunakan tercantum
- [x] Persentase kontribusi AI dan anggota tercantum
- [x] Jumlah interaksi utama tercantum
- [x] Detail 10 interaksi terdokumentasi
- [x] Respons/saran AI dijelaskan
- [x] Modifikasi dan keputusan anggota dijelaskan
- [x] Kesalahan AI dicatat
- [x] Cara verifikasi dicatat
- [x] Bukti keterlacakan dicantumkan
- [x] Pembagian tugas dicantumkan
- [x] Refleksi pribadi Ariq telah diisi dan dikonfirmasi
- [x] Refleksi pribadi Andri telah diisi dan dikonfirmasi
- [x] Seluruh pembagian tugas telah dikonfirmasi
- [x] Seluruh anggota menyetujui isi AI Usage Log

---

## 11. Persetujuan Anggota

- **Ariq Gymnastiar Prabowo:** ______________________________
- **Andri:** ________________________________________________
- **Tanggal persetujuan:** 17-07-2026
