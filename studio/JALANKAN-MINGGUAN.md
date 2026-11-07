# Menjalankan siklus mingguan

Tempel salah satu perintah ini ke sesi Claude Code di repositori ini. Sesi utama memanggil agen satu per satu memakai alat Agent dan berhenti di setiap gerbang pengguna.

## Senin: laporan dan keputusan
```
Jalankan siklus Senin untuk studio agen "Tokoh Alkitab". Panggil agen marketing-analyst untuk membuat laporan dari studio/state/metrik.csv, lalu panggil head-of-marketing untuk membaca laporan itu dan menulis keputusan. Tunjukkan ringkasan keduanya dan berhenti.
```

## Selasa: naskah
```
Panggil agen trend-copywriter untuk menyiapkan paket 3 video berikutnya dari studio/state/kalender.json. Setelah selesai, tunjukkan daftar paket dan ayat kunci yang perlu saya tempel dari Bible.com TB. Berhenti di Gerbang 1.
```

## Setelah saya mengunggah MP3
```
MP3 untuk video NN sudah ada di studio/antrian/NN-<tokoh>/voiceover.mp3. Panggil agen production untuk merender video dan thumbnail. Lalu berhenti di Gerbang 2 dan beri tahu apa yang belum diperiksa.
```

## Setelah saya menyetujui video
```
Video NN sudah saya setujui. Ubah statusnya menjadi video-disetujui lalu panggil agen social-media-specialist untuk membuat paket unggah dan jadwal 7 hari.
```

Catatan: agen tidak bisa memanggil agen lain, jadi sesi utama yang mengatur urutan. Karena sesi cloud bersifat sementara, selalu minta agen men-commit hasilnya ke repositori.
