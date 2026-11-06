# Caption dan thumbnail

## Caption TikTok
1. Baris pertama: hook ringkas + satu emoji.
2. Satu sampai dua kalimat inti beserta rujukan ayat.
3. Satu pertanyaan pemicu komentar.
4. "Seri Tokoh Alkitab, Video <VIDEO_KE>. Follow supaya tidak ketinggalan tokoh berikutnya!"
5. 8 sampai 10 hashtag.

## Caption Instagram (Reels)
Lebih panjang dan berparagraf: pembuka berupa rangkaian gambaran singkat, rujukan ayat kunci (kitab pasal:ayat). Kutip teks ayatnya hanya jika ada di `ayat-tb.json`; jika tidak, tulis rujukannya saja, pesan inti, pertanyaan komentar, ajakan simpan dan bagikan, lalu 8 sampai 10 hashtag.

## Hashtag
Tetap: `#TokohAlkitab #KisahAlkitab #RenunganHarian #Alkitab`. Tambah 2 sampai 3 hashtag khusus tokoh (mis. `#Gideon #Hakim_hakim` atau `#DaudDanGoliat #1Samuel17`), lalu `#Iman #Kristen`. TikTok tambah `#FYP`, Instagram tambah `#ReelsIndonesia`.

## Komentar sematan (opsional)
"Mau tau kisah Tokoh Alkitab lainnya? Follow dan tulis di komentar: siapa tokoh yang mau dibahas berikutnya? 👇"

## Thumbnail
- Format 9:16, 1080x1920. Sampul tidak tertutup tombol TikTok, jadi seluruh area 3:4 (y 240 sampai 1680) boleh dipakai: sebarkan elemen dari y sekitar 300 sampai 1600 supaya tidak ada bagian bawah yang kosong. Latar depan (`foreground`) mengisi tepi bawah.
- Tetap utuh bila dipotong 3:4 (area y 240 sampai 1680) untuk grid Instagram. Label sampul memakai zona y 250 sampai 1650 (otomatis).
- Jangan menumpuk lebih dari tiga blok teks; tokoh harus terlihat jelas dan tidak tertutup label.
- Susunan: tag seri di atas ("TOKOH ALKITAB · VIDEO N"), nama tokoh sebagai teks terbesar, satu baris pemicu rasa penasaran (maksimal 4 kata), siluet lawan atau elemen utama, tokoh utama berwarna hangat (emas).
- Buat dengan `storykit.py thumb spec.json out` dari bagian `thumbnail` di `spec.json`. Tulis juga teks sampul dan alt text.
- Cara pasang: TikTok "Edit sampul" lalu "Dari album"; Reels pilih sampul dari galeri.

## Format contoh (Daud)
Lihat `examples/contoh-daud-paket.md`.
