# Format storyboard (`spec.json`) untuk `scripts/storykit.py`

Satu berkas JSON mendeskripsikan seluruh video. Contoh teruji: `examples/contoh-gideon/spec.json` (detail, 17 adegan, waktu menempel ke ucapan) dan `examples/contoh-daud-spec.json` (waktu manual).

## Koordinat dan waktu
- Koordinat **layar akhir 1080x1920**. Zona aman TikTok untuk teks dan elemen penting: x 60 sampai 960, **y 150 sampai 1500**. Subtitle berpusat di y 1385 (maks 2 baris). **y 1500 ke bawah** diisi pemandangan latar depan oleh mesin (`foreground`), bukan teks.
- Waktu `start`, `end`, `spoken`, dan `audio` memakai **waktu global** (detik dari awal video = awal MP3; suara mulai di detik 0).
- Waktu di dalam lapisan (`t`, `show`, `anim`) memakai **waktu lokal adegan** (0 = awal adegan).
- Label yang keluar zona aman dijepit otomatis, tetapi `lint` tetap melaporkannya.
- **`meta.ground_shift`** (mis. 110) menggeser semua elemen latar (matahari, bukit, aktor, air) ke bawah tanpa menggeser label. Tulis adegan dengan garis tanah di y sekitar 1140, lalu `ground_shift: 110` membuat tanah ada di y sekitar 1250 sehingga tokoh lebih rendah dan bawah tidak kosong.

## Menempelkan waktu ke ucapan (disarankan)
Supaya setelah rekaman asli masuk tidak ada yang perlu disetel ulang, jangan tulis angka waktu. Tulis kata yang diucapkan:
- `scenes[i].start_at`: "awal frasa" yang menjadi awal adegan (boleh dengan `start_offset`).
- `label.at`: kata atau frasa saat label muncul (waktu diperkirakan dari posisi kata dalam kalimat). `at_offset` untuk koreksi.
- `anim[i].at` dengan `dt: [mulai, akhir]` (relatif terhadap kata itu), dan `flash`, `shake`, `starburst`, `confetti` boleh memakai `at`.
- `scenes[i].sfx: [{"at": "frasa", "type": "crack"}]` untuk efek suara.
- `meta.auto: true` menghitung `hook_end` (awal adegan pertama), `outro_start` (frasa "Mau tahu kisah", atau `meta.outro_at`), dan `total` (akhir suara + 1,3 detik).
Frasa dicari di `spoken` (huruf besar-kecil diabaikan). Jika tidak ditemukan, mesin berhenti dengan pesan galat yang menyebut frasanya.

## Struktur tingkat atas
```json
{
  "meta": {"tokoh":"Gideon","video_no":22,"tag":"TOKOH ALKITAB  ·  VIDEO 22","auto":true,"ground_shift":110},
  "spoken": [[0.3, 3.5, "kalimat"], ...],
  "hook": {"bg":[36,34,56], "foreground":{"color":[40,38,64],"kind":"rock","y":1520}, "layers":[ ... ]},
  "scenes": [ {"start_at":"Tujuh tahun lamanya","bg":[..],"layers":[ ... ], "intensity":0.4} ],
  "outro": {"bg":[126,40,34], "cues":{"question":0.2,"sentence":2.3,"follow":3.3,"share":3.9,"komen":4.5}},
  "sprites": { "kendi": {"w":200,"h":260,"shapes":[ ... ]} },
  "thumbnail": {"bg":[..], "foreground":{...}, "layers":[ ... ]},
  "audio": { ... }
}
```
- `spoken`: hasil `align_spoken.py` (`--estimate` sebelum rekaman, `segments.json` setelahnya). Subtitle dibuat dari sini (hanya antara `hook_end` dan `outro_start`) dan frasa panjang dipecah otomatis.
- `outro.cues` (detik sejak `outro_start`) mengatur kemunculan elemen penutup. Isi dari waktu ucapan kata "follow", "share", "komen".
- Kartu pembuka diberi tag otomatis dari `meta.tag`.

## Lapisan (`layers`, digambar dari belakang ke depan; label selalu di atas semuanya)
Semua lapisan boleh memakai `"show": [t0, t1]`.

| type | Bidang utama |
|---|---|
| `rays` | `center`, `colors` [c1, c2], `n`, `speed` |
| `sun` | `center`, `r`, `color`, `ray_color`, `n`, `speed` |
| `disc` | `center`, `r`, `color` (matahari, bulan, cahaya) |
| `hill` | `color`, `base` (y puncak), `amp`, `freq`, `phase`, `drift` |
| `water` | `y`, `colors`, `step` (pita air bergelombang) |
| `actor` | lihat di bawah |
| `label` | `text` ("\n" = baris baru), `x`, `y`, `t` atau `at`, `style`, `size`, `angle`, `wiggle`, `until`, `pop`, `scale`, `maxw`, `fixed` |
| `starburst` | `t`/`at`, `x`, `y`, `r`, `dur`, `static` |
| `confetti` | `t`/`at`, `origin`, `n`, `spread`, `colors`, `seed` |
| `flash`, `shake`, `darken` | `t`/`at`, `dur`, `alpha`/`amp`/`color` |

- **Latar depan otomatis:** setiap adegan yang memiliki lapisan `hill` mendapat 3 lapis pemandangan di y 1500 ke bawah (warna turunan dari bukit terakhir). Atur lewat `"foreground": {"color":[r,g,b],"kind":"grass|rock|sand","y":1500}` atau matikan dengan `"foreground": null`. Hook, thumbnail, dan adegan tanpa bukit perlu `foreground` eksplisit.
- **Satu teks pada satu waktu:** label yang lebih awal otomatis hilang saat label berikutnya muncul. Untuk menampilkan beberapa label bersamaan, beri `"stack": true` pada adegannya (hindari; `lint` akan memperingatkan).
- Gaya label: `paper`, `brick`, `dark`, `earth`, `gold`, `tag`. Teks label wajib kata yang sedang diucapkan.

## Aktor
```json
{"type":"actor","sprite":"person","opts":{"robe":[160,110,60],"beard":[200,200,200]},
 "x":500,"y":1160,"scale":1.35,"anchor":"bottom","rot":0,"alpha":1,"jitter":2,"wobble":0.6,"show":[0,99],"anim":[ ... ]}
```
- `anchor:"bottom"`: `y` = tepi bawah sprite (kaki). Dengan `ground_shift` 110, tokoh berdiri di `y` sekitar 1160 sampai 1190.
- `pivot` ([x,y] di sprite) dan `pivot_at` ([x,y] di layar) memutar sprite pada satu titik (benda roboh).
- Skala yang dianjurkan: tokoh utama 1.3 sampai 1.5 (sekitar sepertiga tinggi layar), kelompok kecil 0.6 sampai 1.0.

### Sprite bawaan
`person` (opsi: `robe`, `belt`, `skin`, `hair`, `beard`, `hat` = `crown|turban|helm|veil`, `hat_color`, `staff`, `dress`, `long_hair`, `flip`), `king`, `giant` (`black: true` untuk siluet), `soldier` (`col`, `helm`), `sheep`, `stone`, `crown`, `sack`, `armor`.

### Sprite kustom
Tambahkan di `sprites`. Bentuk: `{"poly":[[x,y],...],"fill":[r,g,b]}`, `{"ell":[x0,y0,x1,y1],"fill":..}`, `{"line":[[x,y],[x,y]],"width":8,"fill":..}`, `{"text":"..","xy":[x,y],"size":40}`; opsi `edge`, `amp`, `ew`. Contoh di `contoh-gideon/spec.json`: kendi, obor, kemah, gua, pemeras anggur, kitab.

## Animasi (`anim`)
- Tween: `{"t":[t0,t1], "x":[dari,ke], "ease":"io"}` untuk `x`, `y`, `scale`, `rot`, `alpha`. Ease: `lin`, `io`, `in`, `out`, `back`. Alternatif waktu: `{"at":"frasa","dt":[0,0.4], ...}`.
- Osilasi: `{"type":"osc","prop":"y","amp":-18,"freq":6.5,"abs":true,"phase":0,"t":[t0,t1]}`.
- Munculnya benda: tween `scale` dari 0.001 ke nilai akhir dengan `"ease":"back"`.

## Audio
Per adegan (disarankan, mengikuti `start_at` otomatis): `"intensity": 0.4` (kekuatan drone), `"drums": 0.7` (selang detik antar ketukan), `"oud": {"notes":["D4","F#4"],"step":0.6}`, `"sfx": [{"at":"frasa","type":"crack"}]`. Pad kemenangan di adegan terakhir dan penutup dibuat otomatis. Jenis sfx: `boom`, `hit`, `step`, `crack`, `impact`, `tink`, `pop`, `whoosh`, `riser`, `water`, `cheer`. Pengaturan global opsional di `audio` (`intensity`, `pad`, `oud`, `drums`, `sfx`, `auto_ticks`). Turunkan `intensity` ke 0 sebelum klimaks untuk jeda dramatis.

## Thumbnail
Bagian `thumbnail` memakai struktur adegan dan digambar dalam kondisi akhir. Label di sini memakai zona y 250 sampai 1650. Sebarkan elemen sampai y 1600 dan isi tepi bawah dengan `foreground`. `python3 scripts/storykit.py thumb spec.json out_dir`.

## `lint`
`python3 scripts/storykit.py lint spec.json` memeriksa: celah atau tumpang tindih antar adegan, adegan terlalu pendek atau lebih dari 10,5 detik, suara terlalu dekat akhir video, label di luar zona aman, label terlalu panjang (lebih dari 7 kata atau 3 baris), dua label tampil bersamaan atau saling menimpa, label menabrak area subtitle, dan label yang katanya tidak ada di ucapan sekitar. Keluarnya kode 0 bila bersih.
