# Aturan isi dan naskah

## Konteks seri
- Nama seri: "Tokoh Alkitab". Tujuan: mengajak orang belajar tokoh-tokoh Alkitab dari Kejadian sampai Wahyu.
- Video 1 adalah pengantar seri, Video 2 adalah Adam & Hawa; urutan selanjutnya mengikuti `references/kalender-6-bulan.md` (Daud ada di Video 28). Nomor ditentukan oleh `VIDEO_KE`.
- Terjemahan acuan: **Alkitab Terjemahan Baru (TB, LAI)**, dipakai di Gereja Bethel Indonesia. Nama Allah (YHWH) ditulis TUHAN (huruf kapital semua). Ejaan nama mengikuti TB.

## Aturan isi (wajib)
1. **Setia pada teks.** Peristiwa, urutan, angka, dan ucapan kunci harus berasal dari bacaan. Jangan menambah usia, rupa, perasaan, atau dialog yang tidak ada. Hal dari tradisi atau tafsir hanya boleh dengan kata "menurut tradisi" dan ditandai "[tradisi]".
2. **Kutipan ayat hanya dari teks TB yang terverifikasi** (lihat "Kebijakan ayat" di `SKILL.md`). Cerita ditulis sebagai parafrase tanpa tanda kutip.
3. **Satu pesan inti** yang bisa dipraktikkan penonton.
4. **Nada:** hangat, tidak menggurui, tidak menghakimi denominasi mana pun, tidak mengejek tokoh atau kelompok.
5. **Kisah sensitif** (kekerasan, pelecehan, bunuh diri, kematian anak): ceritakan singkat dan lembut, tanpa detail mengerikan. Jika tidak pantas untuk video umum, usulkan sudut pandang lain dari tokoh yang sama.
6. **Yesus, Allah, malaikat:** jangan menggambarkan wajah. Pakai siluet, cahaya, tangan, atau sudut dari belakang.
7. **Hook boleh clickbait, tetapi 100 persen benar** menurut Alkitab. Dilarang melebih-lebihkan atau menyesatkan.

## Mode naskah

| | detail (bawaan) | ringkas |
|---|---|---|
| Kata cerita | 240 sampai 300 | 150 sampai 185 |
| Paragraf cerita | 12 sampai 15 | 9 |
| Adegan | 14 sampai 17 | 10 |
| Durasi total sekitar | 2 sampai 2,5 menit | 75 sampai 80 detik |

### Struktur naskah detail (12 sampai 15 paragraf)
1. Latar: kapan, di mana, keadaan bangsanya.
2. Masalah atau ancaman (boleh dua paragraf).
3. Pengenalan tokoh: siapa dia, sedang apa.
4. Panggilan atau pemicu, termasuk keraguan tokoh.
5. Janji atau penguatan dari Tuhan.
6. Proses atau keputusan, dengan sedikitnya dua langkah (persiapan, ujian).
7. Puncak (beberapa kalimat sangat pendek).
8. Hasil.
9. Rujukan: satu kalimat pendek "Kisah ini ada di kitab ..., pasal ...". Aman karena hanya rujukan pasal.
10. Pesan untuk penonton (3 sampai 4 kalimat; yang terakhir paling ringkas dan kuat).
Pisahkan paragraf panjang menjadi dua paragraf agar tiap adegan tidak lebih dari sekitar 9 detik.

### Struktur ringkas (9 paragraf)
Situasi, lawan, pengenalan tokoh, pemicu, keputusan, momen kunci, puncak, hasil, pesan.

## Hook dan penutup
- **Hook suara:** 2 sampai 3 kalimat pendek (12 sampai 22 kata), berupa teka-teki atau pertanyaan yang benar menurut Alkitab. Contoh: "Tiga ratus orang melawan pasukan yang tak terhitung banyaknya. Senjata mereka hanya obor, kendi, dan sangkakala. Bagaimana bisa?"
- **Tag kartu pembuka:** `TOKOH ALKITAB  ·  VIDEO <VIDEO_KE>` (otomatis dari `meta.tag`).
- **Teks hook di layar:** satu label pada satu waktu, mengikuti kalimat yang diucapkan. Seni berada di bawah teks, tidak menimpanya.
- **Penutup suara (tetap):** "Mau tahu kisah tokoh Alkitab lainnya? Jangan lupa untuk follow, share, dan komen konten ini!"
- Kartu penutup di layar dibuat otomatis oleh mesin render.

## Aturan teks suara untuk ElevenLabs
- Paragraf dipisah satu baris kosong. Tanpa tag (`<break>`, `[pause]`, SSML). Jeda diatur dengan titik dan koma.
- Kalimat pendek (maksimal sekitar 18 kata). Tanpa tanda kurung dan singkatan. Angka kecil ditulis dengan huruf ("tiga ratus orang"); label di layar boleh memakai angka.
- Nama sesuai TB; nama Allah ditulis TUHAN.
- Seluruh rekaman dalam satu generasi dan satu MP3. Pakai suara dan model yang sama setiap video.

## Aturan tata letak (agar tidak sumpek dan tidak kosong)
- **Satu teks pada satu waktu.** Label baru menggantikan label lama (bawaan). Maksimal 6 sampai 7 kata dan 2 baris per label. Label menekankan kata kunci; jangan mengulang seluruh kalimat yang sudah tampil sebagai subtitle.
- **Subtitle** maksimal 2 baris (sekitar 44 huruf per potongan); frasa panjang dipecah otomatis.
- **Label tidak boleh menimpa tokoh atau subtitle.** Label di bagian atas (y sekitar 250 sampai 500), subtitle di y 1385.
- **Isi layar:** tokoh utama cukup besar (sekitar sepertiga tinggi layar atau lebih), langit diberi matahari, bulan, awan, atau elemen kisah. Latar depan (y 1500 ke bawah) diisi mesin render.
- **Gerak:** tiap adegan punya satu gerak utama. Adegan lebih dari sekitar 10 detik dipecah.

## Pemeriksaan mutu (sebelum menjawab)
- [ ] Semua fakta ada di bacaan dan punya rujukan ayat.
- [ ] Tidak ada kutipan ayat selain dari `ayat-tb.json` (`cek_ayat.py` lolos).
- [ ] Jumlah kata sesuai mode; tanpa tag atau SSML.
- [ ] `lint` bersih (teks sama dengan suara, tidak bertumpuk, di zona aman).
- [ ] Bagian bawah dan langit tidak kosong pada gambar contoh.
- [ ] Hook benar; penutup tetap persis; nama sesuai TB.
- [ ] Wajah Yesus, Allah, dan malaikat tidak digambarkan.

## Kamus nama (ejaan TB)
Goliat, Daud, Isai, Betlehem, Filistin, Saul, Yonatan, Samuel, Salomo, Elia, Elisa, Naaman, Yunus, Yesaya, Yeremia, Yehezkiel, Daniel, Sadrakh, Mesakh, Abednego, Nebukadnezar, Ester, Nehemia, Ayub, Musa, Harun, Miryam, Firaun, Yosua, Kaleb, Rahab, Debora, Gideon, Simson, Rut, Boas, Hana, Yakub, Esau, Ishak, Ribka, Abraham, Sara, Hagar, Lot, Zakharia, Elisabet, Yohanes Pembaptis, Zakheus, Nikodemus, Lazarus, Marta, Maria, Maria Magdalena, Tomas, Stefanus, Filipus, Ananias, Barnabas, Kornelius, Lidia, Silas, Priskila, Akwila, Timotius, Onesimus, Lukas, Paulus, Petrus, Matius, Yudas Iskariot. Cocokkan ejaan dengan Alkitab TB pengguna bila ragu.
