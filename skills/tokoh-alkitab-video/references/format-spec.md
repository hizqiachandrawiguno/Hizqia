# Format storyboard (`spec.json`) untuk `scripts/storykit.py`

Satu berkas JSON mendeskripsikan seluruh video. Contoh lengkap yang sudah teruji: `examples/contoh-daud-spec.json`.

## Aturan koordinat dan waktu
- Semua koordinat memakai **layar akhir 1080x1920**. Zona aman TikTok: x 60 sampai 960, y 150 sampai 1440. Garis tanah ada di sekitar **y = 1140**. Di bawah y 1440 dibiarkan kosong (diisi warna tanah).
- Waktu `start`, `end`, `spoken`, dan `audio` memakai **waktu global** (detik dari awal video = awal MP3, karena suara dimulai di detik 0).
- Waktu di dalam lapisan (`t`, `show`, `anim`) memakai **waktu lokal adegan** (0 = awal adegan itu).
- Label yang keluar dari zona aman dijepit otomatis, tetapi `lint` tetap melaporkannya. Perbaiki posisinya.

## Struktur tingkat atas
```json
{
  "meta": {"tokoh": "Gideon", "video_no": 22, "tag": "TOKOH ALKITAB  ·  VIDEO 22",
           "hook_end": 6.55, "outro_start": 72.0, "total": 78.9},
  "spoken": [[0.0, 3.2, "kalimat"], ...],
  "hook": {"bg": [140,44,36], "layers": [ ... ], "auto_tag": true},
  "scenes": [ {"start": 6.55, "end": 12.11, "bg": [..], "layers": [ ... ]}, ... ],
  "outro": {"bg": [126,40,34], "cues": {"question":0.2,"sentence":2.3,"follow":3.3,"share":3.9,"komen":4.5}},
  "sprites": { "kendi": {"w":200,"h":240,"shapes":[ ... ]} },
  "thumbnail": {"bg": [..], "layers": [ ... ]},
  "audio": { ... }
}
```
- `spoken`: daftar `[mulai, akhir, teks]` hasil `align_spoken.py`. Subtitle dibuat dari sini (hanya di antara `hook_end` dan `outro_start`).
- `scenes[i].end` boleh dikosongkan (default = `start` adegan berikutnya; adegan terakhir berakhir di `outro_start`).
- `outro.cues` (detik sejak `outro_start`) mengatur kemunculan elemen penutup. Isi dari waktu ucapan kata "follow", "share", "komen".
- Kartu pembuka diberi tag otomatis dari `meta.tag`.
- `total` = akhir suara + sekitar 1,3 detik.

## Jenis lapisan (`layers`, digambar berurutan dari belakang ke depan)
Semua lapisan boleh memakai `"show": [t0, t1]` (hanya tampil dalam rentang itu).

| type | Bidang utama |
|---|---|
| `rays` | `center`, `colors` [c1, c2], `n`, `speed` (sinar berputar) |
| `sun` | `center`, `r`, `color`, `ray_color`, `n`, `speed` (matahari bersinar) |
| `disc` | `center`, `r`, `color` (lingkaran berbingkai) |
| `hill` | `color`, `base` (y puncak), `amp`, `freq`, `phase`, `drift` (px/detik) |
| `water` | `y`, `colors` (pita air bergelombang) |
| `actor` | lihat di bawah |
| `label` | `text` ("\n" = baris baru), `x`, `y`, `t` (waktu muncul), `style`, `size`, `angle`, `wiggle`, `until`, `pop`, `scale`, `maxw` |
| `starburst` | `t`, `x`, `y`, `r`, `dur`, `static` (bintang ledakan) |
| `confetti` | `t`, `origin` [x,y], `n`, `spread`, `colors`, `seed` (serpihan kertas) |
| `flash` | `t`, `dur`, `alpha`, `color` |
| `shake` | `t`, `dur`, `amp` (layar bergetar) |
| `darken` | `t`, `dur` (meredup ke gelap) |

Gaya label (`style`): `paper` (krem), `brick` (merah bata), `dark` (arang), `earth` (cokelat), `gold` (emas), `tag` (huruf sans emas di atas arang). **Teks label wajib kata yang sedang diucapkan** (lint memeriksa).

## Aktor
```json
{"type":"actor","sprite":"person","opts":{"robe":[60,90,140],"beard":[200,200,200]},
 "x":500,"y":1150,"scale":1.2,"anchor":"bottom","rot":0,"alpha":1,
 "jitter":2,"wobble":0.6,"show":[0,99],"anim":[ ... ]}
```
- `x`,`y` = pusat sprite. Dengan `"anchor":"bottom"`, `y` = tepi bawah sprite (kaki), cocok untuk menaruh tokoh di tanah (y sekitar 1140 sampai 1210).
- `pivot` ([x,y] di dalam sprite) dan `pivot_at` ([x,y] di layar) memutar sprite pada satu titik (untuk benda yang jatuh atau roboh); gerak lewat `anim` pada `rot`.

### Sprite bawaan
| sprite | Keterangan |
|---|---|
| `person` | Tokoh manusia. Opsi: `robe`, `belt`, `skin`, `hair`, `beard` (warna atau null), `hat` (`crown`, `turban`, `helm`, `veil`), `hat_color`, `staff` (true/false), `dress` (jubah panjang), `long_hair`, `flip` |
| `king` | Raja berjubah dengan mahkota dan janggut |
| `giant` | Prajurit raksasa berzirah; `opts: {"black": true}` untuk siluet |
| `soldier` | Prajurit kecil; opsi `col`, `helm` |
| `sheep`, `stone`, `crown`, `sack`, `armor` | Domba, batu emas, mahkota, karung, baju zirah |

### Sprite kustom dari bentuk dasar
Tambahkan di `sprites` lalu pakai namanya sebagai `sprite`. Bentuk: `{"poly":[[x,y],...],"fill":[r,g,b]}`, `{"ell":[x0,y0,x1,y1],"fill":..}`, `{"line":[[x,y],[x,y]],"width":8,"fill":..}`, `{"text":"..","xy":[x,y],"size":40}`. Pakai `"edge"` untuk warna tepi dan `"amp"` untuk kekasaran tepi robek. Cocok untuk bahtera, kendi, obor, tembok, singa, ikan, salib (tanpa wajah).

## Animasi (`anim`)
- **Tween:** `{"t":[t0,t1], "x":[dari,ke], "ease":"io"}`. Bidang yang bisa digerakkan: `x`, `y`, `scale`, `rot` (derajat), `alpha`. Sebelum `t0` nilai bertahan di "dari", setelah `t1` bertahan di "ke". Ease: `lin`, `io`, `in`, `out`, `back`.
- **Osilasi:** `{"type":"osc","prop":"y","amp":-18,"freq":6.5,"abs":true,"phase":0,"t":[t0,t1]}` menambah gerak naik-turun (langkah kaki, lompatan). Dua osilasi `x` dan `y` dengan beda fase 1,57 menghasilkan gerak melingkar (umban berputar).
- Muncul dengan "meletup": tween `scale` dari 0 ke nilai akhir dengan `"ease":"back"`.

## Audio (`audio`, semua opsional; waktu global)
```json
{"intensity": [[0,0.2],[6.5,0.5],...],   // kuat drone dari waktu ke waktu
 "pad": [[0,0],[60,0.4],[78,0]],           // lapisan akor kemenangan
 "oud": [{"t":20.5,"notes":["D4","F#4","G4"],"step":0.55,"amp":0.5}],
 "drums": [{"from":26,"to":43,"step":0.75,"amp":0.65}],
 "sfx": [{"t":55.0,"type":"impact","amp":1.0}],
 "auto_ticks": true}
```
Jenis `sfx`: `boom`, `hit`, `step`, `crack`, `impact`, `tink`, `pop`, `whoosh`, `riser`, `water`, `cheer`. Untuk jeda dramatis di klimaks, turunkan `intensity` ke 0 sebelum hantaman.

## Thumbnail
Bagian `thumbnail` memakai struktur adegan (`bg`, `layers`) yang digambar dalam kondisi akhir (semua label sudah muncul; pakai `"static": true` pada `starburst`). Perintah: `python3 scripts/storykit.py thumb spec.json out_dir`.

## Alur kerja `lint`
`python3 scripts/storykit.py lint spec.json` memeriksa: celah atau tumpang tindih antar adegan, adegan terlalu pendek, suara terlalu dekat dengan akhir video, label di luar zona aman, dan label yang katanya tidak ditemukan di ucapan sekitar. Keluarannya kode 0 bila bersih.
