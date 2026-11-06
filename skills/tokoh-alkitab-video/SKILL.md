---
name: tokoh-alkitab-video
description: >-
  Membuat konten video pendek seri "Tokoh Alkitab" (TikTok dan Instagram Reels, vertikal 9:16) dari satu baris perintah. Menghasilkan naskah suara detail siap ElevenLabs, hook clickbait, storyboard, thumbnail, caption TikTok dan Instagram, lalu merender video kolase potongan kertas dari rekaman MP3 (transkrip Whisper, subtitle sinkron otomatis, tata letak tidak sumpek, area bawah terisi, zona aman TikTok, hook dan penutup tetap). Kutipan ayat hanya dari teks Alkitab Terjemahan Baru (TB) yang terverifikasi. Gunakan skill ini setiap kali pengguna menyebut tokoh Alkitab, kisah Alkitab, renungan video pendek, kalender konten Alkitab, format "TOKOH: ... | BACAAN: ... | VIDEO_KE: ...", thumbnail atau caption untuk konten rohani Kristen, atau mengirim MP3 voice over untuk video Alkitab, walaupun pengguna tidak menyebut kata skill.
---

# Tokoh Alkitab Video

Pengguna (jemaat GBI, memakai Alkitab Terjemahan Baru) cukup mengirim satu baris:

```
TOKOH: Gideon | BACAAN: Hakim-hakim 6–7 | VIDEO_KE: 22 | MODE: detail | CATATAN: (opsional)
```

`BACAAN` boleh kosong (pilih bacaan utama sendiri, lihat `references/kalender-6-bulan.md`). `MODE` bawaan `detail`; `ringkas` untuk versi pendek. Jangan bertanya balik: pakai nilai bawaan lalu tulis di bagian "Asumsi". Alasannya, pengguna membuat puluhan video dan tiap pertanyaan balik memperlambat seluruh rangkaian.

Pekerjaan dibagi dua. Tahap A dikerjakan untuk setiap baris perintah. Tahap B dikerjakan setelah pengguna mengirim MP3 rekaman suara.

## Tiga pelajaran dari umpan balik pengguna (jangan diulang)

1. **Ayat harus benar menurut TB.** Pengguna meminta ayat dipastikan di Alkitab. Anda tidak boleh menulis kutipan dari ingatan. Aturannya ada di bagian "Kebijakan ayat".
2. **Layar tidak boleh sumpek.** Satu teks pada satu waktu, pendek, dan tidak menumpuk. Ada pemeriksa otomatis (`lint`).
3. **Tidak ada ruang kosong yang besar**, baik di bawah maupun di langit. Bagian bawah (y 1500 ke bawah) diisi pemandangan latar depan oleh mesin render. Tokoh dibuat cukup besar dan langit diberi matahari, bulan, atau awan.

## Kebijakan ayat (wajib)

- Cerita ditulis sebagai **parafrase tanpa tanda kutip**. Tanda kutip hanya dipakai untuk kutipan yang teksnya ada persis di `ayat-tb.json`.
- Sumber teks ayat, berurutan: (1) teks TB yang ditempel pengguna; (2) teks dari situs Alkitab yang berhasil dijangkau dari sesi ini (misalnya alkitab.sabda.org), dengan mencatat sumbernya di `_sumber`. Jika keduanya tidak ada, **jangan menulis ayat dari ingatan**.
- Jalankan `python3 scripts/cek_ayat.py naskah.txt ayat-tb.json` sebelum menjawab. Kutipan yang tidak ada di `ayat-tb.json` menggagalkan pemeriksaan.
- Jika ayat belum terverifikasi, tulis rujukan (kitab pasal:ayat) dan tandai di pemeriksaan akurasi: "BELUM diverifikasi dengan TB". Lalu minta pengguna menempelkan teks TB ayat kunci, atau mengizinkan akses ke situs Alkitab.
- Rujukan pasal pada ucapan ("ada di kitab Hakim-hakim, pasal enam dan tujuh") aman dan dianjurkan.
- Angka dan fakta (usia, jumlah, lama hari) tetap harus ada rujukan ayatnya di pemeriksaan akurasi.

## Tahap A: Paket naskah dan storyboard

1. Baca `references/aturan-isi-dan-naskah.md` (akurasi, struktur naskah detail, teks suara, kamus nama) dan `references/caption-dan-thumbnail.md`. Untuk menulis `spec.json` baca `references/format-spec.md`. Contoh lengkap: `examples/contoh-gideon/` (detail) dan `examples/contoh-daud-paket.md`.
2. Tulis paket dengan urutan tetap di bawah, lalu simpan di folder `NN-<tokoh>/` (NN = VIDEO_KE): `paket.md`, `naskah.txt` (hanya teks yang direkam: hook, paragraf cerita, penutup tetap, tanpa tag), dan `spec.json`.
3. `python3 scripts/align_spoken.py NN-tokoh/naskah.txt --estimate NN-tokoh/spoken.json`, masukkan ke `spoken` di `spec.json`. Di `spec.json`, tempelkan waktu ke kata yang diucapkan (`start_at`, `at`, dan `meta.auto`, lihat `format-spec.md`). Dengan begitu Tahap B tidak perlu menyetel waktu lagi.
4. `python3 scripts/storykit.py lint NN-tokoh/spec.json` sampai bersih. Lalu `stills` dan **lihat gambarnya** (hook, adegan tengah, klimaks, penutup). Periksa bagian bawah tidak kosong dan teks tidak menumpuk.
5. Jawab pengguna singkat dan arahkan satu langkah: "Rekam `naskah.txt` di ElevenLabs sekali jalan (satu generasi, tanpa tag), lalu unggah MP3-nya."

### Format paket (urutan tetap, jangan menambah bagian)
1. Ringkasan satu baris: tokoh, bacaan, pesan inti.
2. Hook: teks di layar dan kalimat suara.
3. Naskah suara lengkap, jumlah kata, perkiraan durasi.
4. Storyboard (tabel: adegan, paragraf, visual, teks di layar, efek).
5. Thumbnail: rancangan, teks sampul, alt text.
6. Caption TikTok dan Instagram, hashtag, komentar sematan.
7. Pemeriksaan akurasi: tiap fakta dan angka beserta rujukan ayatnya, status verifikasi (terverifikasi TB atau BELUM), dan tanda "[tradisi]" untuk yang bukan dari teks.
8. Asumsi.

### Hal yang paling sering salah (dan alasannya)
- **Teks di layar harus sama dengan kata yang sedang diucapkan.** `lint` memeriksanya.
- **Jangan pakai tag `<break>`, `[pause]`, atau SSML.** Model suara tidak mendukungnya dan tag bisa terbaca. Atur jeda dengan titik dan koma.
- **Seluruh rekaman dalam satu berkas**: hook, cerita, lalu penutup tetap. Satu generasi, satu MP3.
- **Penutup suara tetap:** "Mau tahu kisah tokoh Alkitab lainnya? Jangan lupa untuk follow, share, dan komen konten ini!"
- **Kepadatan teks:** satu label pada satu waktu (selain tag seri), maksimal 6 sampai 7 kata dan 2 baris; subtitle maksimal 2 baris. Label hanya untuk penekanan kata kunci dan jangan mengulang seluruh kalimat.
- **Zona aman:** teks dan elemen penting di x 60 sampai 960 dan y 150 sampai 1500. Subtitle berpusat di y 1385. Bagian y 1500 ke bawah adalah pemandangan latar depan.
- **Setia pada teks Alkitab.** Jangan mengarang detail.

## Tahap B: Produksi dari MP3

1. `bash scripts/setup_asr.sh` sekali (mencetak folder model). Berjalan lokal, audio tidak dikirim ke layanan luar. Jika jaringan tidak mengizinkan unduhan model, katakan terus terang dan jangan menebak waktu tanpa memberi tahu pengguna.
2. `python3 -I scripts/transcribe_vo.py voiceover.mp3 <folder_model> segments.json`
3. `python3 scripts/align_spoken.py naskah.txt segments.json spoken.json`. Baca semua PERINGATAN. Teks subtitle diambil dari naskah, bukan ejaan Whisper.
4. Ganti isi `spoken` di `spec.json` dengan hasilnya. Karena waktu menempel ke kata (`start_at`, `at`, `meta.auto`), semua adegan, label, dan efek ikut bergeser. Jalankan `lint`; jika ada adegan terlalu lama, pecah adegannya.
5. `python3 scripts/storykit.py stills spec.json out` dan periksa momen penting.
6. Render: `python3 scripts/storykit.py render spec.json work video-tanpa-suara.mp4`, lalu di folder berisi `timeline.env`: `bash scripts/add_voiceover.sh voiceover.mp3 video-tanpa-suara.mp4 video-final.mp4`.
7. `python3 scripts/storykit.py thumb spec.json out` (9:16 dan potongan 3:4).
8. Periksa durasi, resolusi 1080x1920, level audio, dan gambar contoh dari video akhir. Laporkan jujur apa yang sudah dan belum diperiksa (Anda tidak bisa mendengarkan audio).

## Perintah revisi singkat
Keluarkan hanya bagian yang berubah: `/ganti-hook` (3 pilihan), `/pendekkan`, `/hangat`, `/tegas`, `/caption-lain` (2 variasi), `/sampul-lain` (2 rancangan), `/kurangi-teks` (kurangi label dan perpendek).

## Berkas dalam skill
- `references/aturan-isi-dan-naskah.md`, `references/format-spec.md`, `references/caption-dan-thumbnail.md`, `references/kalender-6-bulan.md`, `references/ayat-tb.json` (tempat ayat TB terverifikasi).
- `examples/`: Daud (`contoh-daud-*`) dan Gideon detail (`contoh-gideon/`).
- `scripts/`: `storykit.py` (render, lint, thumbnail), `cek_ayat.py`, `setup_asr.sh`, `transcribe_vo.py`, `align_spoken.py`, `add_voiceover.sh`.

## Batasan yang perlu dikatakan terus terang
- Benda khusus (bahtera, tembok, singa) dibuat dari bentuk dasar di JSON; hasilnya kolase sederhana.
- Musik dan efek suara sintetis. Skill ini tidak membuat suara; pengguna merekam di ElevenLabs.
- Sesi cloud sering tidak bisa menjangkau situs Alkitab. Jika begitu, ayat tidak bisa diverifikasi otomatis dan harus ditempel pengguna.
