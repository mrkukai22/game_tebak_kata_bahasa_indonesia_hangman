# Laporan Manual Acceptance Testing

## Game Tebak Kata Bahasa Indonesia — Release 3.1.0

## 1. Identitas Pengujian

- **Penguji:** Ariq
- **Tanggal:** 15–16 Juli 2026
- **Sistem operasi:** Windows
- **Versi Python:** 3.12.0
- **Folder pengujian:** salinan khusus `Tebak_Kata_Manual_Test`
- **Perintah:** `python main.py --no-clear`
- **Jenis pengujian:** manual acceptance test berbasis skenario

Folder pengujian dipisahkan dari folder distribusi bersih. Oleh karena itu,
leaderboard yang muncul pada screenshot merupakan data hasil manual testing dan
bukan isi awal `data/leaderboard.json` pada paket distribusi.

## 2. Tujuan

Pengujian dilakukan untuk memverifikasi alur yang benar-benar dilihat dan
dijalankan pengguna, meliputi kemenangan, kekalahan, menyerah, jawaban frasa,
validasi input, leaderboard, halaman informasi, pergantian nama, dan keluar
normal dari aplikasi.

## 3. Ringkasan Hasil

| No. | Kelompok skenario | Status |
|---:|---|:---:|
| 1 | Alur normal sampai menang dan leaderboard | **LULUS** |
| 2 | Menyerah | **LULUS** |
| 3 | Kalah karena kesempatan habis | **LULUS** |
| 4 | Jawaban frasa tiga kata | **LULUS** |
| 5 | Cara bermain, tentang proyek, dan ganti nama | **LULUS** |

**Hasil keseluruhan: 5 dari 5 kelompok skenario lulus.**

## 4. Hasil Per Skenario

### Skenario 1 — Alur Normal Sampai Menang

- **Nama pemain:** Ariq
- **Kategori:** Warna
- **Kesulitan:** Mudah / level 1
- **Jawaban:** `NILA`
- **Skor ronde:** `140`

Langkah dan hasil aktual:

1. Aplikasi menerima nama pemain dan menampilkan menu utama.
2. Input kategori berupa teks `warna` ditolak karena pilihan menu harus angka.
3. Kategori Warna dan level Mudah berhasil dipilih.
4. Tebakan benar membuka huruf pada posisi yang sesuai.
5. Tebakan salah mengurangi kesempatan.
6. Huruf `i` yang dimasukkan kembali tidak dihitung dua kali dan program
   menampilkan pesan bahwa huruf sudah pernah digunakan.
7. Setelah seluruh huruf ditemukan, program menampilkan jawaban `NILA` dan
   skor `140`.
8. Skor tersimpan pada leaderboard. Tampilan menunjukkan skor `155` dan `140`
   terurut menurun.
9. Menu `0. Keluar` menutup aplikasi secara normal tanpa traceback.

**Status: LULUS.**

Bukti: `menu_pemilihan01.png`, `proses_permainan_01.png` sampai
`proses_permainan_04.png`, `leaderboard.png`, dan `keluar_permainan.png`.

### Skenario 2 — Menyerah

- **Kategori:** Warna
- **Kesulitan:** Sedang / level 2
- **Jawaban:** `GADING`
- **Input menyerah:** `0`
- **Skor ronde:** `0`

Hasil aktual:

- ronde langsung selesai;
- Hangman menampilkan tahap penuh;
- kesempatan menjadi `0`;
- program menampilkan `Kamu menyerah. Jawabannya: GADING`;
- skor ronde `0`;
- leaderboard tetap hanya berisi skor kemenangan sebelumnya.

**Status: LULUS.**

Bukti: `proses_permainan_menyerah.png` dan
`leaderboard_setelah_menyerah.png`.

### Skenario 3 — Kalah Karena Kesempatan Habis

- **Kategori:** Warna
- **Kesulitan:** Sulit / level 3
- **Jawaban:** `TEMBAGA`
- **Skor ronde:** `0`

Hasil aktual:

- input angka `1` sebagai tebakan ditolak dengan pesan bahwa input harus tepat
  satu huruf alfabet;
- tebakan benar membuka huruf;
- tebakan salah mengurangi kesempatan sampai `0`;
- perkembangan gambar Hangman bertambah sampai tahap penuh;
- program menampilkan `Kesempatan habis. Jawabannya: TEMBAGA`;
- skor ronde `0`;
- leaderboard tidak memperoleh entri baru dari ronde kalah.

**Status: LULUS.**

Bukti: `proses_kesempatan_berkurang_01.png` sampai
`proses_kesempatan_berkurang_04.png`, `kalah_kesempatan_habis.png`, dan
`leaderboard_setelah_kalah.png`.

### Skenario 4 — Jawaban Frasa

- **Kategori:** Negara
- **Kesulitan:** Sulit / level 3
- **Jawaban:** `REPUBLIK AFRIKA TENGAH`
- **Jumlah huruf:** `20`
- **Jumlah kata:** `3`
- **Skor ronde:** `960`

Hasil aktual:

- sejak awal, tiga bagian jawaban dipisahkan dengan karakter `/`;
- pemain tidak perlu menebak spasi;
- tebakan benar membuka huruf pada seluruh posisi yang sesuai;
- tebakan salah tetap mengurangi kesempatan;
- jawaban dapat diselesaikan sampai menang;
- program menampilkan jawaban penuh dan skor `960`.

**Status: LULUS.**

Bukti: `frasa_muncul.png`, `frasa_proses_tebakan_01.png` sampai
`frasa_proses_tebakan_07.png`, dan `frasa_hasil_akhir.png`.

### Skenario 5 — Menu Informasi dan Ganti Nama

Hasil aktual:

- menu `Cara bermain` menampilkan aturan, cara menyerah, dan penjelasan skor;
- menu `Tentang proyek` menampilkan 24 kategori, 2.059 entri, 397 frasa,
  tiga tingkat kesulitan, sumber kandidat data, dan penyimpanan lokal;
- ketika mengganti nama, input kosong ditolak;
- nama berhasil diubah dari `Ariq` menjadi `Andri` dan langsung tampil pada
  menu utama;
- tidak terjadi crash atau traceback.

**Status: LULUS.**

Bukti: `cara_bermain.png`, `tentang_proyek.png`, dan
`ganti_nama_pemain.png`.

## 5. Matriks Bukti

| Kelompok | File bukti utama |
|---|---|
| Menang | `menu_pemilihan01.png`, `proses_permainan_*.png`, `leaderboard.png`, `keluar_permainan.png` |
| Menyerah | `proses_permainan_menyerah.png`, `leaderboard_setelah_menyerah.png` |
| Kalah | `proses_kesempatan_berkurang_*.png`, `kalah_kesempatan_habis.png`, `leaderboard_setelah_kalah.png` |
| Frasa | `frasa_muncul.png`, `frasa_proses_tebakan_*.png`, `frasa_hasil_akhir.png` |
| Menu dan nama | `cara_bermain.png`, `tentang_proyek.png`, `ganti_nama_pemain.png` |

Seluruh bukti berada pada direktori `evidence/manual_test/`.

## 6. Batasan Pengujian

- Pengujian manual dilakukan oleh satu penguji.
- Pencegahan pengulangan jawaban sampai seluruh pool habis tidak diuji dengan
  memainkan ribuan ronde; perilaku tersebut diverifikasi oleh automated test.
- Kerusakan JSON dan kegagalan file I/O diverifikasi oleh automated test,
  bukan dengan merusak file distribusi secara manual.
- Pengujian Google Colab dilakukan secara terpisah dan didokumentasikan pada `docs/COLAB_TEST_REPORT.md`.
- Hasil ini membuktikan skenario yang dijalankan, bukan menjamin perangkat
  lunak bebas dari seluruh kemungkinan bug.

## 7. Kesimpulan

Seluruh alur utama yang diujikan secara manual pada Windows dengan Python
3.12.0 berjalan sesuai harapan. Manual acceptance testing pada perangkat lokal
dinyatakan **LULUS**. Pengujian Google Colab juga telah dilakukan dan
didokumentasikan secara terpisah pada `docs/COLAB_TEST_REPORT.md`.
