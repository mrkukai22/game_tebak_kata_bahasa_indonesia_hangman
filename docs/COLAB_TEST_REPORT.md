# Laporan Pengujian Google Colab

## Game Tebak Kata Bahasa Indonesia — Release 3.1.0

## 1. Identitas Pengujian

- **Penguji:** Ariq
- **Tanggal:** 17 Juli 2026
- **Tanggal UTC pada environment:** 17 Juli 2026
- **Python:** 3.12.13
- **Platform:** Linux-6.6.122+-x86_64-with-glibc2.35
- **Runtime:** Google Colab, CPU standar
- **Versi aplikasi:** 3.1.0
- **Notebook:** `evidence/colab/PENGUJIAN_GOOGLE_COLAB.ipynb`

## 2. Tujuan

Pengujian ini memverifikasi bahwa ZIP release bersih dapat diunggah,
diekstrak, divalidasi, diuji, dan dijalankan secara interaktif pada Google
Colab tanpa modifikasi kode aplikasi.

## 3. Hasil Pengujian

| No. | Pengujian | Hasil Aktual | Status |
|---:|---|---|:---:|
| 1 | Pemeriksaan environment | Python 3.12.13 pada platform Linux Colab | LULUS |
| 2 | Preflight release | Leaderboard awal kosong dan artefak runtime tidak ditemukan | LULUS |
| 3 | Pemeriksaan versi | Aplikasi melaporkan versi 3.1.0 | LULUS |
| 4 | Automated regression test | `Ran 52 tests in 0.773s` dan `OK` | LULUS |
| 5 | Validator bank data | 24 kategori, 2.059 entri, 397 frasa, versi 3.1.0 | LULUS |
| 6 | Smoke test interaktif | Kategori Warna, level Mudah, jawaban MERAH, skor 175 | LULUS |
| 7 | Keluar normal | Pesan `Terima kasih sudah bermain.` muncul tanpa traceback | LULUS |

## 4. Bukti

Seluruh bukti berada pada `evidence/colab/`:

- `17_colab_environment.png`
- `18_colab_automated_test.png`
- `19_colab_validator.png`
- `20_colab_smoke_test.png`
- `21_colab_keluar_normal.png`
- `HASIL_TEST_GOOGLE_COLAB.txt`
- `PENGUJIAN_GOOGLE_COLAB.ipynb`

## 5. Kesimpulan

Release 3.1.0 dapat dijalankan pada Google Colab dengan Python 3.12.13.
Automated test, validator data, smoke test interaktif, dan alur keluar normal
seluruhnya **LULUS**. Tidak ditemukan masalah selama pengujian.
