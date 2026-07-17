# Test Plan — Release 3.1.0

## 1. Automated Test

Jalankan:

```powershell
python -m unittest discover -s tests -v
python tools\validate_bank.py
```

Cakupan utama:

- validasi metadata generik dan jumlah per kategori;
- format, urutan A–Z, duplikat, dan jawaban tautologis;
- file bank hilang, rusak, tidak dapat dibaca, atau akses ditolak;
- pemilihan acak, exclusion set, dan reset siklus pool;
- state Hangman, frasa, scoring, kalah, menyerah, dan progres gambar;
- karakter kontrol pada nama pemain;
- schema, timestamp, kategori, skor, dan atomic write leaderboard;
- seluruh jalur menu utama dan error persistence;
- CLI, logging fallback, validator text/details/JSON;
- konsistensi versi dan leaderboard distribusi awal.

Hasil verifikasi release bersih: **52/52 test lulus** dan validator berstatus
**VALID**.

## 2. Coverage

Pengukuran internal:

```powershell
coverage run --branch -m unittest discover -s tests
coverage report -m
```

Hasil release: **99% branch coverage** pada package `game`, dengan seluruh
baris kode package tersentuh pengujian.

## 3. Manual Acceptance Test

- **Penguji:** Ariq
- **Tanggal:** 15–16 Juli 2026
- **Sistem operasi:** Windows
- **Python:** 3.12.0
- **Perintah:** `python main.py --no-clear`

| No | Skenario/Input | Hasil yang Diharapkan | Hasil Aktual | Status |
|---:|---|---|---|:---:|
| 1 | Jalankan aplikasi | Menu utama tampil tanpa error | Menu tampil dan menerima nama pemain | LULUS |
| 2 | Masukkan pilihan kategori berupa teks `warna` | Input ditolak, program meminta angka | Pesan input angka tidak valid tampil, program tetap berjalan | LULUS |
| 3 | Ganti nama dengan input kosong, lalu `Andri` | Input kosong ditolak; nama valid diterima | Input kosong ditolak dan nama berubah dari Ariq menjadi Andri | LULUS |
| 4 | Main level 1 | Maksimal salah 8 dan pengali x1 | Level Mudah dapat dimainkan sampai menang | LULUS |
| 5 | Main level 2 lalu ketik `0` | Maksimal salah 7, pengali x2, menyerah menghasilkan skor 0 | Jawaban GADING tampil, kesempatan 0, skor 0 | LULUS |
| 6 | Main level 3 | Maksimal salah 6 dan pengali x3 | Level Sulit diuji pada skenario kalah dan frasa | LULUS |
| 7 | Tebak benar, salah, dan huruf berulang | State diperbarui dengan benar dan duplikat tidak dihitung dua kali | Seluruh perilaku tampil sesuai aturan | LULUS |
| 8 | Selesaikan jawaban `NILA` | Pesan menang dan skor positif | Menang dengan skor 140 | LULUS |
| 9 | Habiskan kesempatan pada jawaban `TEMBAGA` | Jawaban tampil dan skor 0 | Kesempatan 0, jawaban tampil, skor 0 | LULUS |
| 10 | Menyerah pada jawaban `GADING` | Hangman penuh, kesempatan 0, skor 0 | Seluruh kondisi muncul dan leaderboard tidak bertambah | LULUS |
| 11 | Mainkan frasa `REPUBLIK AFRIKA TENGAH` | Spasi terbuka otomatis; frasa dapat diselesaikan | Pemisah `/` tampil otomatis dan ronde menang dengan skor 960 | LULUS |
| 12 | Buka leaderboard | Skor menang tersimpan dan diurutkan terbesar | Skor 155 dan 140 tampil menurun; kalah/menyerah tidak menambah skor | LULUS |
| 13 | Buka Cara Bermain dan Tentang Proyek | Informasi tampil dan dapat kembali ke menu | Kedua halaman tampil tanpa error | LULUS |
| 14 | Pilih menu `0. Keluar` | Program berhenti normal | Terminal kembali ke PowerShell tanpa traceback | LULUS |
| 15 | Jalankan validator default, `--details`, dan `--json` | Struktur valid dan keluaran konsisten | 24 kategori, 2.059 entri, 397 frasa, versi 3.1.0 | LULUS |
| 16 | Pool jawaban habis lalu reset | Jawaban tidak berulang sebelum pool habis | Diverifikasi melalui automated test, tidak diulang manual karena ukuran pool besar | OTOMATIS |
| 17 | Jalankan pada Google Colab | Program, test, validator, dan fitur utama berjalan | Python 3.12.13; 52 test OK; validator VALID; smoke test dan keluar normal berhasil | LULUS |

## 4. Pengujian Google Colab

- **Penguji:** Ariq
- **Tanggal:** 17 Juli 2026
- **Python:** 3.12.13
- **Platform:** Linux-6.6.122+-x86_64-with-glibc2.35
- **Automated test:** 52/52 LULUS
- **Validator data:** LULUS
- **Smoke test:** LULUS
- **Keluar normal:** LULUS

Smoke test menggunakan kategori Warna, kesulitan Mudah, jawaban `MERAH`,
dan menghasilkan skor `175`.

## 5. Referensi Bukti

Laporan dan screenshot tersedia pada:

```text
docs/MANUAL_TEST_REPORT.md
docs/COLAB_TEST_REPORT.md
evidence/manual_test/
evidence/colab/
```

## 6. Kesimpulan

Automated regression test, validator data, manual acceptance test pada
Windows, dan pengujian Google Colab seluruhnya dinyatakan **LULUS**.
