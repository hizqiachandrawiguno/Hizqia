# Protokol Studio Agen: Seri "Tokoh Alkitab"

Lima agen bekerja untuk satu akun konten. Semua agen membaca dan menulis berkas di folder `studio/`. Tidak ada agen yang mengunggah atau menyetujui sesuatu sendiri pada Fase 1.

## Lima agen
| Agen | Berkas | Tugas ringkas |
|---|---|---|
| Head of Marketing | `.claude/agents/head-of-marketing.md` | Menetapkan target, membaca laporan Analyst, memutuskan perubahan kalender dan prioritas |
| Marketing Analyst | `.claude/agents/marketing-analyst.md` | Menghitung engagement rate dan mengulas performa serta komentar |
| Trend & Copywriter | `.claude/agents/trend-copywriter.md` | Riset tren, hook, naskah suara, rujukan ayat |
| Production | `.claude/agents/production.md` | Storyboard, render video, thumbnail (memakai skill `tokoh-alkitab-video`) |
| Social Media Specialist | `.claude/agents/social-media-specialist.md` | Caption, hashtag, jadwal, paket unggah, balasan komentar |

## Berkas bersama
- `studio/state/kalender.json`: 78 video, status tiap video (`rencana`, `naskah`, `naskah-disetujui`, `rekaman`, `render`, `video-disetujui`, `dijadwalkan`, `tayang`).
- `studio/state/metrik.csv`: data performa (diisi pengguna dari ekspor TikTok dan Instagram, lihat kolom di berkasnya).
- `studio/state/keputusan.md`: catatan keputusan Head of Marketing (baru di atas).
- `studio/antrian/NN-tokoh/`: hasil kerja per video: `paket.md`, `naskah.txt`, `spec.json`, `unggah.md`, dan hasil render.
- `studio/laporan/AAAA-MM-DD-laporan.md`: laporan mingguan Analyst.

## Siklus mingguan
| Hari | Agen | Hasil |
|---|---|---|
| Senin | Marketing Analyst | `laporan/…-laporan.md` dari `metrik.csv` |
| Senin | Head of Marketing | Entri baru di `keputusan.md` dan perubahan `kalender.json` bila perlu |
| Selasa | Trend & Copywriter | Paket naskah 3 video berikutnya (status `naskah`) |
| Rabu | **Pengguna** | Gerbang 1: periksa naskah dan ayat TB, setujui (`naskah-disetujui`) |
| Rabu–Kamis | **Pengguna** | Rekam suara di ElevenLabs, unggah MP3 (`rekaman`) |
| Kamis | Production | Render video dan thumbnail (status `render`) |
| Jumat | **Pengguna** | Gerbang 2: tonton video final, setujui (`video-disetujui`) |
| Jumat | Social Media Specialist | `unggah.md` (caption, hashtag, jam tayang) dan jadwal (`dijadwalkan`) |
| Sesuai jadwal | **Pengguna** (Fase 1) | Mengunggah, lalu mengisi `metrik.csv` seminggu kemudian |

## Gerbang persetujuan (tidak boleh dilewati)
1. **G1: Naskah dan ayat.** Hanya pengguna yang menyetujui isi ajaran dan ayat. Ayat hanya dikutip dari teks TB yang ditempel pengguna (Bible.com TB sebagai patokan). Tanpa itu: parafrase tanpa tanda kutip dan status "BELUM diverifikasi".
2. **G2: Video final.** Pengguna menonton dan mendengarkan sebelum jadwal dibuat.
3. **G3: Unggah.** Fase 1 dan 2: pengguna yang mengunggah. Fase 3 (otomatis) hanya bila pengguna sudah memberi izin tertulis dan akun terhubung.

## Fase
- **Fase 1 (sekarang):** agen membuat semua paket. Pengguna menyetujui dan mengunggah. Data performa lewat ekspor CSV.
- **Fase 2:** data dan akun terhubung (API atau konektor). Specialist menyiapkan unggahan terjadwal.
- **Fase 3:** unggah otomatis setelah persetujuan G2, dan studio 3D sebagai tampilan status.

## Aturan umum semua agen
- Kerjakan hanya bagian perannya. Jangan mengubah berkas milik agen lain kecuali status di `kalender.json` sesuai tabel.
- Jangan mengarang data. Jika data tidak ada, tulis "data belum ada".
- Jangan menulis ayat dari ingatan. Rujukan boleh; kutipan hanya dari `skills/tokoh-alkitab-video/references/ayat-tb.json`.
- Tulis hasil dalam bahasa Indonesia, singkat, dengan temuan dulu.
- Akhiri setiap pekerjaan dengan laporan: apa yang dikerjakan, berkas yang diubah, hal yang belum bisa dan alasannya.
- Jangan menyentuh akun, kata sandi, atau token. Jangan mengirim data pribadi ke layanan luar.


## Ritme harian (mulai 7 Nov 2026): 7 video per minggu
- **Kerja per batch mingguan.** Tiap Minggu atau Senin, kirim 7 bacaan TB sekaligus ke Claude. Satu sesi: Trend & Copywriter menulis 7 naskah, Anda setujui (G1), rekam 7 MP3 sekali duduk, Production merender 7 video (sekitar 3 menit per video), Anda tonton (G2), lalu Social Media Specialist menyusun caption dan jadwal 7 hari (G3).
- **Penyangga:** usahakan selalu 5 sampai 7 video siap tayang di depan. Jangan bekerja hari-H.
- **Hari longgar:** boleh ganti 1 sampai 2 video per minggu ke mode ringkas (75 sampai 80 detik, tetap di atas 1 menit untuk syarat monetisasi) bila beban terlalu berat.
- Tanggal ada di `state/kalender.json` dan `panduan/jadwal-harian.md`.
