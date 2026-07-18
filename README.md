# Game Tebak Kata Bahasa Indonesia

Aplikasi konsol Python berbasis Hangman untuk proyek akhir mata kuliah
Algoritma dan Pemrograman. Aplikasi berjalan sepenuhnya secara lokal tanpa
API dan tanpa dependensi pihak ketiga.

## Fitur Utama

- Bank jawaban Bahasa Indonesia: **24 kategori dan 2.059 entri**.
- Dukungan kata tunggal dan frasa; spasi terbuka otomatis.
- Hangman display yang berkembang saat tebakan salah.
- Tiga tingkat kesulitan dengan batas kesalahan dan pengali skor berbeda.
- Scoring berdasarkan panjang jawaban, akurasi, sisa kesempatan, dan level.
- Leaderboard lokal yang divalidasi, diurutkan, dan ditulis secara atomik.
- Perlindungan terhadap karakter kontrol pada nama pemain.
- Siklus pemilihan acak yang mencegah pengulangan sebelum satu pool habis.
- Validasi ketat terhadap bank data dan metadata.

## Struktur Data dan Algoritma

- `list`: daftar jawaban, tahap Hangman, dan kumpulan leaderboard.
- `dict`: kategori, level, konfigurasi, dan setiap entri skor.
- `set`: huruf tebakan, huruf salah, dan jawaban yang sudah dipakai.
- `random.choice()`: pemilihan jawaban acak.
- String matching: pengecekan huruf dengan operator `in`.
- Set matching: kondisi menang dengan `issubset()`.
- Sorting: leaderboard dari skor terbesar.

## Persyaratan

- Python **3.11 atau lebih baru**.
- Tidak memerlukan `pip install` untuk menjalankan aplikasi.

## Menjalankan Aplikasi

```powershell
python main.py
```

Windows juga dapat memakai `run_game.bat`. Linux/macOS dapat memakai:

```bash
./run_game.sh
```

Opsi CLI:

```powershell
python main.py --no-clear
python main.py --validate-bank
python main.py --version
```

## Menjalankan Pengujian

```powershell
python -m unittest discover -s tests -v
python tools\validate_bank.py
```

atau jalankan `run_tests.bat`.

## Validator Bank Data

Output default hanya menampilkan statistik struktural umum:

```text
VALID: Struktur dan metadata bank kata konsisten.
Kategori : 24
Entri    : 2059
Frasa    : 397
Versi    : 3.1.0
```

Rincian seluruh kategori hanya ditampilkan saat diminta:

```powershell
python tools\validate_bank.py --details
python tools\validate_bank.py --json
```

## Struktur Proyek

```text
game_tebak_kata_bahasa_indonesia/
├── main.py
├── game/
│   ├── application.py
│   ├── config.py
│   ├── data_manager.py
│   ├── exceptions.py
│   ├── hangman.py
│   ├── leaderboard.py
│   ├── types.py
│   ├── ui.py
│   └── validation.py
├── data/
│   ├── bank_kata.json
│   └── leaderboard.json
├── tests/
├── tools/validate_bank.py
├── docs/
├── TEST_PLAN.md
├── AI_USAGE_LOG.md
└── pyproject.toml
```

## Reliability dan Keamanan Lokal

- Bank data selalu divalidasi sebelum permainan dimulai.
- Metadata menggunakan statistik umum dan jumlah per kategori, bukan satu
  kategori khusus.
- Daftar jawaban harus terurut, unik dalam kategori, dan sesuai format.
- Jawaban yang identik dengan nama kategorinya sendiri ditolak.
- Nama pemain dinormalisasi dan karakter kontrol terminal ditolak.
- Leaderboard memvalidasi schema, kategori, jawaban, skor, dan timestamp.
- Penulisan leaderboard menggunakan file sementara, `fsync`, dan
  `os.replace()`.
- Error terduga ditampilkan secara ramah; error tak terduga dicatat ke log.

## Sumber Data

Kandidat kata bersumber dari **Contek Sambung Kata** dengan atribusi:
**By MizuuDev Tim NepuhSoft**. Data kemudian dikurasi dan dinormalisasi untuk
kebutuhan permainan. Detail tersedia pada `docs/DATASET.md`.

## Catatan Akademik

Semua anggota wajib memahami alur kode, menjalankan pengujian pada perangkat
demo, dan melengkapi `AI_USAGE_LOG.md` secara jujur sebelum pengumpulan.


## Hasil Manual Acceptance Testing

Manual acceptance testing dilakukan oleh Ariq pada Windows dengan Python
3.12.0 tanggal 15–16 Juli 2026. Lima kelompok skenario utama dinyatakan
**LULUS**: menang, menyerah, kalah, frasa, serta menu informasi/ganti nama.

Dokumentasi dan bukti:

- `docs/MANUAL_TEST_REPORT.md`
- `TEST_PLAN.md`
- `HASIL_TEST.txt`
- `evidence/manual_test/`

Pengujian Google Colab pada Python 3.12.13 telah dinyatakan **LULUS**:
52 automated test, validator data, smoke test interaktif, dan keluar normal.

Dokumentasi dan bukti:

- `docs/COLAB_TEST_REPORT.md`
- `evidence/colab/`

## COLAB :
https://colab.research.google.com/drive/1uY7mJD_JyrACA-2S2SmUE_enucweNPPr?usp=sharing
