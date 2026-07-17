# Changelog

## 3.1.0 — Full Hardening Audit

- Mengubah validator menjadi kategori-netral pada output default.
- Menambahkan mode validator `--details` dan `--json`.
- Mengganti metadata `jumlah_kata` menjadi `jumlah_entri`.
- Mengganti metadata kategori khusus dengan `jumlah_per_kategori`.
- Menambahkan validasi urutan A–Z dan jawaban tautologis.
- Menambahkan normalisasi dan keamanan nama pemain.
- Memperketat schema leaderboard dan atomic write cleanup.
- Memisahkan riwayat random per kategori dan tingkat kesulitan.
- Memperketat validasi state domain Hangman.
- Menormalkan sejumlah istilah dataset.
- Meningkatkan test suite menjadi 52 test dan 99% branch coverage.

## 3.0.0 — Production Cleanup

- Memisahkan lapisan domain, aplikasi, UI, konfigurasi, dan persistence.
- Menambahkan validasi bank data, atomic leaderboard write, logging, dan CLI.


## Documentation Update — 16 Juli 2026

- Menambahkan laporan manual acceptance testing berbasis bukti screenshot.
- Memperbarui `TEST_PLAN.md` dengan expected output, actual output, dan status.
- Memperbarui `HASIL_TEST.txt` dengan hasil manual Windows Python 3.12.0.
- Menambahkan folder `evidence/manual_test/`.
- Tidak ada perubahan pada logika aplikasi atau dataset.


## Dokumentasi Pengujian — 17 Juli 2026

- Menambahkan bukti Google Colab pada `evidence/colab/`.
- Menambahkan `docs/COLAB_TEST_REPORT.md`.
- Memperbarui `TEST_PLAN.md`, `HASIL_TEST.txt`, `README.md`, dan laporan
  manual testing.
- Tidak ada perubahan pada kode aplikasi, dataset, atau versi release.
