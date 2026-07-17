# Security dan Data Integrity

Aplikasi ini bersifat lokal, tidak membuka port jaringan, tidak memakai API,
dan tidak memproses kredensial.

## Perlindungan yang Diterapkan

- Nama pemain menolak karakter kontrol dan escape sequence terminal.
- Jawaban bank data dibatasi pada huruf kecil `a-z` dan spasi tunggal.
- Leaderboard menolak schema, kategori, jawaban, skor, dan timestamp yang
  tidak valid.
- File leaderboard ditulis secara atomik agar kegagalan proses tidak mudah
  merusak file utama.
- Error tak terduga dicatat ke file log berotasi.
- Semua path data ditetapkan dari direktori proyek, bukan input pengguna.

## Batasan

- Leaderboard JSON dirancang untuk satu pengguna/proses pada satu perangkat,
  bukan penyimpanan multi-user bersamaan.
- File lokal tetap dapat diubah oleh pengguna yang memiliki akses sistem
  operasi; perubahan tidak valid akan ditolak saat dibaca.
