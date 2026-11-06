---
name: tokoh-alkitab-video
description: >-
  Membuat konten video pendek seri "Tokoh Alkitab" (TikTok dan Instagram Reels, vertikal 9:16) dari satu baris perintah. Menghasilkan naskah suara siap ElevenLabs, hook clickbait, storyboard 10 adegan, thumbnail, caption TikTok dan Instagram, lalu merender video kolase potongan kertas dari rekaman MP3 (transkrip Whisper, subtitle sinkron, zona aman TikTok, hook dan penutup tetap). Gunakan skill ini setiap kali pengguna menyebut tokoh Alkitab, kisah Alkitab, renungan video pendek, kalender konten Alkitab, format "TOKOH: ... | BACAAN: ... | VIDEO_KE: ...", thumbnail atau caption untuk konten rohani Kristen, atau mengirim MP3 voice over untuk video Alkitab, walaupun pengguna tidak menyebut kata skill.
---

# Tokoh Alkitab Video

Skill ini menggantikan prompt panjang yang dulu harus ditempel tiap membuat konten. Pengguna hanya perlu mengirim satu baris:

```
TOKOH: Gideon | BACAAN: Hakim-hakim 6–7 | VIDEO_KE: 22 | CATATAN: (opsional)
```

`BACAAN` boleh kosong (pilih bacaan utama sendiri, lihat `references/kalender-6-bulan.md`). Jangan bertanya balik. Jika ada yang kurang, pakai nilai bawaan lalu tulis di bagian "Asumsi". Alasannya: pengguna membuat puluhan video, dan tiap pertanyaan balik memperlambat seluruh rangkaian.

Pekerjaan dibagi dua tahap. Tahap A dikerjakan setiap ada baris perintah. Tahap B dikerjakan setelah pengguna mengirim MP3 rekaman suara.

## Tahap A: Paket naskah dan storyboard

1. Baca `references/aturan-isi-dan-naskah.md` (akurasi Alkitab, struktur 9 paragraf, aturan teks suara, kamus nama). Baca `references/caption-dan-thumbnail.md` untuk caption dan sampul.
2. Tulis paket dengan urutan tetap di bawah. Contoh lengkap ada di `examples/contoh-daud-paket.md`.
3. Simpan berkas di folder kerja `NN-<tokoh>/` (NN = VIDEO_KE):
   - `paket.md`: seluruh bagian 1 sampai 8.
   - `naskah.txt`: hanya teks yang akan direkam (hook, 9 paragraf, penutup tetap), paragraf dipisah baris kosong, tanpa tag. Ini yang disalin pengguna ke ElevenLabs.
   - `spec.json`: storyboard dalam format mesin render (`references/format-spec.md`), dengan waktu perkiraan.
4. Buat waktu perkiraan: `python3 scripts/align_spoken.py NN-tokoh/naskah.txt --estimate NN-tokoh/spoken.json`, masukkan ke `spoken` di `spec.json`, lalu jalankan `python3 scripts/storykit.py lint NN-tokoh/spec.json`. Perbaiki semua temuan. Lalu `python3 scripts/storykit.py stills NN-tokoh/spec.json NN-tokoh/preview` dan lihat gambarnya sebelum melapor.
5. Jawab pengguna dengan ringkasan pendek dan arahan satu langkah: "Rekam `naskah.txt` di ElevenLabs sekali jalan (satu generasi, tanpa tag), lalu unggah MP3-nya."

### Format paket (urutan tetap, jangan menambah bagian)

1. Ringkasan satu baris: tokoh, bacaan utama, pesan inti.
2. Hook: teks di layar dan kalimat suara.
3. Naskah suara lengkap (hook, 9 paragraf, penutup tetap), jumlah kata, perkiraan durasi.
4. Storyboard 10 adegan (tabel: adegan, paragraf VO, visual, teks di layar, efek).
5. Thumbnail: rancangan, teks sampul, alt text.
6. Caption TikTok dan Instagram, hashtag, komentar sematan.
7. Pemeriksaan akurasi: fakta dari teks beserta ayatnya, tanda "[tradisi]" untuk yang bukan dari teks.
8. Asumsi.

### Hal yang paling sering salah (dan alasannya)

- **Teks di layar harus sama dengan kata yang sedang diucapkan.** Pengguna sudah pernah mengeluh teks tidak cocok dengan suara. `storykit.py lint` memeriksanya, jadi jangan menulis label yang tidak diucapkan (misalnya judul pesan yang tidak ada di naskah).
- **Jangan pakai tag `<break>`, `[pause]`, atau SSML** di naskah. Model suara yang dipakai tidak mendukungnya dan tag bisa terbaca. Atur jeda dengan titik dan koma.
- **Seluruh rekaman dibuat dalam satu berkas**: hook, cerita, lalu penutup tetap. Satu generasi, satu MP3. Percobaan sebelumnya membuktikan cara ini menghasilkan jeda yang wajar.
- **Kalimat penutup suara tetap**: "Mau tahu kisah tokoh Alkitab lainnya? Jangan lupa untuk follow, share, dan komen konten ini!" Jangan diubah.
- **Setia pada teks Alkitab.** Jangan mengarang detail. Tandai "[tradisi]" bila perlu. Hook boleh clickbait tetapi harus benar.
- **Zona aman TikTok:** semua elemen penting di x 60 sampai 960 dan y 150 sampai 1440. Area bawah (y lebih dari 1440) dibiarkan kosong. Mesin render menjepit label otomatis dan `lint` melaporkannya.

## Tahap B: Produksi dari MP3

Mulai tahap ini ketika pengguna mengirim MP3. Kerjakan berurutan dan jangan menebak waktu.

1. Pasang mesin transkrip sekali: `bash scripts/setup_asr.sh` (mencetak folder model). Mesin berjalan lokal, audio tidak dikirim ke layanan luar. Jika jaringan tidak mengizinkan unduhan model, katakan terus terang dan jangan beralih ke tebakan waktu tanpa memberi tahu pengguna.
2. Transkrip: `python3 -I scripts/transcribe_vo.py voiceover.mp3 <folder_model> segments.json`.
3. Cocokkan dengan naskah: `python3 scripts/align_spoken.py naskah.txt segments.json spoken.json`. Baca semua PERINGATAN. Teks subtitle diambil dari naskah, bukan dari ejaan Whisper.
4. Perbarui `spec.json`: isi `spoken`, atur `hook_end` (sedikit sebelum kalimat cerita pertama), `outro_start` (awal kalimat penutup), `total` (akhir suara + sekitar 1,3 detik), dan `start` tiap adegan = awal kalimat pertama paragraf adegan itu. Sesuaikan waktu `t` label dan animasi di dalam adegan dengan kalimat yang diucapkan (waktu adegan dihitung dari awal adegan).
5. `python3 scripts/storykit.py lint spec.json` sampai bersih, lalu `stills` dan periksa gambar contoh di momen penting (hook, klimaks, penutup).
6. Render: `python3 scripts/storykit.py render spec.json work video-tanpa-suara.mp4`, lalu di folder berisi `timeline.env`: `bash scripts/add_voiceover.sh voiceover.mp3 video-tanpa-suara.mp4 video-final.mp4`.
7. Thumbnail: `python3 scripts/storykit.py thumb spec.json out` (menghasilkan versi 9:16 dan potongan 3:4 untuk grid Instagram).
8. Periksa: durasi, resolusi 1080x1920, level audio, dan gambar contoh dari video akhir. Laporkan jujur apa yang sudah dan belum diperiksa (Anda tidak bisa mendengarkan audio).

## Perintah revisi singkat

Jika pengguna membalas satu perintah, keluarkan hanya bagian yang berubah:
`/ganti-hook` (3 pilihan hook baru), `/pendekkan` (sekitar 130 kata), `/hangat`, `/tegas`, `/caption-lain` (2 variasi), `/sampul-lain` (2 rancangan).

## Berkas dalam skill

- `references/aturan-isi-dan-naskah.md`: aturan isi, struktur 9 paragraf, teks suara, kamus nama LAI.
- `references/format-spec.md`: format JSON storyboard untuk `storykit.py` (lapisan, animasi, sprite, audio).
- `references/caption-dan-thumbnail.md`: templat caption dan aturan sampul.
- `references/kalender-6-bulan.md`: 78 tokoh, urutan Kejadian sampai Wahyu, tanggal tayang.
- `examples/`: contoh Daud lengkap (naskah, paket, spec, waktu ucapan).
- `scripts/`: `storykit.py` (render, lint, thumbnail), `setup_asr.sh`, `transcribe_vo.py`, `align_spoken.py`, `add_voiceover.sh`.

## Batasan yang perlu dikatakan terus terang

- Kisah dengan adegan yang sangat khusus (efek yang tidak ada di sprite bawaan) memerlukan sprite kustom dari bentuk dasar (lihat `format-spec.md`). Tampilannya tetap kolase sederhana, bukan ilustrasi detail.
- Audio musik dan efek dibuat sintetis, jadi sederhana.
- Skill ini tidak membuat suara. Pengguna merekam sendiri di ElevenLabs.
- Kutipan ayat berasal dari ingatan model. Minta pengguna mencocokkan dengan Alkitab mereka.
