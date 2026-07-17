# Arsitektur Aplikasi

## Lapisan

1. **Entry point (`main.py`)**
   Menangani CLI, logging, exit code, dan error tingkat aplikasi.
2. **Application service (`game/application.py`)**
   Mengatur menu, sesi pemain, siklus jawaban, dan koordinasi antar modul.
3. **Domain (`game/hangman.py`)**
   Menyimpan aturan Hangman tanpa membaca terminal atau file.
4. **Validation (`game/validation.py`)**
   Menormalisasi nama pemain dan format jawaban secara terpusat.
5. **Persistence (`data_manager.py`, `leaderboard.py`)**
   Memvalidasi bank data dan menyimpan leaderboard secara atomik.
6. **Presentation (`game/ui.py`)**
   Mengisolasi input/output terminal agar dapat diuji.

## Alur Ronde

```text
Pilih kategori
    ↓
Pilih kesulitan
    ↓
Ambil pool kategori + level
    ↓
Hindari jawaban yang sudah muncul dalam siklus aktif
    ↓
random selection dari list jawaban
    ↓
Tebak huruf → string matching
    ↓
set menyimpan huruf unik
    ↓
Menang / kalah / menyerah
    ↓
Hitung skor → simpan dict skor → sorting leaderboard
```

## Keputusan Desain

- Domain Hangman tidak mengetahui file atau terminal.
- UI menerima fungsi input/output sehingga dapat diuji tanpa terminal nyata.
- `GuessStatus` menggantikan magic string pada logika inti.
- Konfigurasi kesulitan bersifat immutable.
- Statistik bank data generik dan tidak bergantung pada satu kategori khusus.
- Error yang diperkirakan memakai exception khusus.
- Leaderboard ditulis melalui file sementara lalu `os.replace()`.
- Riwayat jawaban dipisah per pasangan kategori dan kesulitan.
