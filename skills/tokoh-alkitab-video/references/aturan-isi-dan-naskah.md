# Aturan isi dan naskah

## Konteks seri
- Nama seri: "Tokoh Alkitab". Tujuan: mengajak orang belajar singkat tokoh-tokoh Alkitab dari Kejadian sampai Wahyu.
- Video 1 adalah pengantar seri, Video 2 adalah Daud (sudah tayang). Nomor ditentukan oleh `VIDEO_KE`.
- Terjemahan acuan: Alkitab Terjemahan Baru (LAI). Pakai ejaan nama LAI secara konsisten. Nama Allah/YHWH ditulis TUHAN (huruf kapital semua).

## Aturan isi (wajib)
1. **Setia pada teks.** Peristiwa, urutan, angka, dan ucapan kunci harus berasal dari bacaan. Jangan menambah usia, rupa, perasaan, atau dialog yang tidak ada. Hal dari tradisi atau tafsir hanya boleh dipakai dengan kata "menurut tradisi" dan ditandai "[tradisi]" di pemeriksaan akurasi.
2. **Satu pesan inti** yang bisa dipraktikkan penonton.
3. **Nada:** hangat, tidak menggurui, tidak menghakimi denominasi mana pun, tidak mengejek tokoh atau kelompok.
4. **Kisah sensitif** (kekerasan, pelecehan, bunuh diri, kematian anak): ceritakan singkat dan lembut, tanpa detail mengerikan. Jika kisah tidak pantas untuk video umum, usulkan sudut pandang lain dari tokoh yang sama. Contoh: kematian Yudas cukup disebut sebagai akhir yang tragis, tanpa rincian.
5. **Yesus, Allah, malaikat:** jangan menggambarkan wajah. Pakai siluet, cahaya, tangan, atau sudut dari belakang.
6. **Hook boleh clickbait, tetapi 100 persen benar** menurut Alkitab. Dilarang melebih-lebihkan atau menyesatkan.

## Struktur naskah suara
Bagian cerita sekitar 150 sampai 185 kata dalam 9 paragraf (satu paragraf menjadi satu atau lebih adegan):

| P | Isi |
|---|---|
| P1 | Situasi atau masalah (kalimat pertama harus menarik) |
| P2 | Pihak lawan atau tantangan |
| P3 | Pengenalan tokoh utama |
| P4 | Alasan atau pemicu tokoh bertindak |
| P5 | Keputusan dan persiapan |
| P6 | Ucapan atau momen kunci dari teks |
| P7 | Aksi puncak (2 sampai 3 kalimat sangat pendek) |
| P8 | Hasil |
| P9 | Pesan untuk penonton (3 sampai 4 kalimat; yang terakhir paling ringkas dan kuat) |

Sesuaikan isi dengan kisahnya, tetapi pertahankan 9 paragraf dan nadanya. Rekaman lengkap = hook + 9 paragraf + penutup tetap, durasi total sekitar 70 sampai 80 detik (hook 5 sampai 7 detik, cerita 55 sampai 65 detik, penutup 5 sampai 7 detik).

## Hook dan penutup
- **Hook suara:** 2 sampai 3 kalimat pendek (sekitar 12 sampai 22 kata), berupa teka-teki atau pertanyaan yang benar menurut Alkitab. Contoh: "Bocah gembala ini menjatuhkan raksasa tiga meter, hanya dengan satu batu. Bagaimana bisa?"
- **Tag kartu pembuka:** `TOKOH ALKITAB  ·  VIDEO <VIDEO_KE>` (mesin render menambahkannya otomatis dari `meta.tag`).
- **Teks pembuka di layar:** 3 sampai 4 label berurutan, tepat saat kalimat itu diucapkan.
- **Penutup suara (tetap, jangan diubah):** "Mau tahu kisah tokoh Alkitab lainnya? Jangan lupa untuk follow, share, dan komen konten ini!"
- **Kartu penutup di layar** dibuat otomatis oleh mesin render: pertanyaan, tombol FOLLOW, SHARE, KOMEN (muncul saat kata itu diucapkan), lalu kalimat ajakan.

## Aturan teks suara untuk ElevenLabs
- Satu paragraf = satu adegan atau lebih, dipisah satu baris kosong.
- Tanpa tag (`<break>`, `[pause]`, SSML). Jeda diatur dengan titik dan koma.
- Kalimat pendek (maksimal sekitar 18 kata). Tanpa tanda kurung dan singkatan. Angka kecil ditulis dengan huruf ("tiga meter", "empat puluh hari"). Angka besar yang umum boleh digit ("300 orang").
- Nama sesuai LAI; nama Allah ditulis TUHAN.
- Seluruh rekaman dalam satu generasi dan satu MP3.
- Pakai suara dan model yang sama setiap video supaya seri terasa konsisten.

## Storyboard 10 adegan
- Teks di layar HARUS sama dengan atau ringkasan langsung dari kata yang sedang diucapkan. Subtitle menampilkan kalimat apa adanya (dibuat otomatis dari `spoken`).
- Setiap adegan punya satu gerak utama (tokoh masuk, benda jatuh, matahari berputar).
- Adegan klimaks: beri jeda musik sebentar sebelum hantaman efek.
- Semua posisi dalam koordinat layar akhir dan berada di zona aman.

## Pemeriksaan mutu (lakukan sebelum menjawab)
- [ ] Semua fakta ada di bacaan (angka, urutan, ucapan).
- [ ] Tidak ada detail yang dikarang.
- [ ] Naskah 150 sampai 185 kata dan tanpa tag atau SSML.
- [ ] Setiap teks di layar sama dengan kata yang diucapkan saat itu (`lint` bersih).
- [ ] Semua elemen berada di zona aman.
- [ ] Hook benar menurut Alkitab dan tidak menyesatkan.
- [ ] Penutup persis seperti yang tetap di atas.
- [ ] Nama dan istilah sesuai LAI.
- [ ] Wajah Yesus, Allah, dan malaikat tidak digambarkan.

## Kamus nama (ejaan LAI)
Goliat, Daud, Isai, Betlehem, Filistin, Saul, Yonatan, Samuel, Salomo, Elia, Elisa, Naaman, Yunus, Yesaya, Yeremia, Yehezkiel, Daniel, Sadrakh, Mesakh, Abednego, Nebukadnezar, Ester, Nehemia, Ayub, Musa, Harun, Miryam, Firaun, Yosua, Kaleb, Rahab, Debora, Gideon, Simson, Rut, Boas, Hana, Yakub, Esau, Ishak, Ribka, Abraham, Sara, Hagar, Lot, Zakharia, Elisabet, Yohanes Pembaptis, Zakheus, Nikodemus, Lazarus, Marta, Maria, Maria Magdalena, Tomas, Stefanus, Filipus, Ananias, Barnabas, Kornelius, Lidia, Silas, Priskila, Akwila, Timotius, Onesimus, Lukas, Paulus, Petrus, Matius, Yudas Iskariot.
