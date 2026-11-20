#!/usr/bin/env python3
"""Memeriksa kutipan ayat di naskah terhadap teks Alkitab Terjemahan Baru (TB) yang SUDAH DIVERIFIKASI.

Aturan seri ini: kutipan ayat (teks di dalam tanda kutip) hanya boleh dipakai bila teksnya persis ada di
`ayat-tb.json`. Teks itu harus berasal dari Alkitab TB pengguna (ditempel pengguna) atau diambil dari
sumber Alkitab yang dapat dijangkau (catat sumbernya di bidang "_sumber"). Jangan menulis ayat dari ingatan.

Pemakaian:  python3 cek_ayat.py naskah.txt ayat-tb.json
Format ayat-tb.json:
  {"_sumber": "Alkitab TB (ditempel pengguna)", "Hak 7:20": "teks ayat persis ...", "Hak 6:12": "..."}
Keluaran: kode 0 bila semua kutipan terverifikasi. Kutipan yang tidak ditemukan dilaporkan.
"""
import sys, re, json

def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()

def main():
    naskah = open(sys.argv[1], encoding="utf-8").read()
    ayat = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {}
    verses = {k: norm(v) for k, v in ayat.items() if not k.startswith("_") and v.strip()}
    quotes = re.findall(r"[“\"]([^”\"]{12,})[”\"]", naskah)
    bad = []
    for q in quotes:
        nq = norm(q)
        if len(nq.split()) < 4:
            continue
        if not any(nq in v for v in verses.values()):
            bad.append(q)
    for q in bad:
        print("KUTIPAN TIDAK TERVERIFIKASI (tidak ada di ayat-tb.json): \"%s\"" % q)
    if not quotes:
        print("OK: naskah tidak memuat kutipan ayat (parafrase tanpa tanda kutip).")
    elif not bad:
        print("OK: semua %d kutipan cocok persis dengan ayat-tb.json." % len(quotes))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
