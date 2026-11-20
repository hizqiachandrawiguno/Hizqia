#!/usr/bin/env python3
"""Mencocokkan naskah dengan potongan transkrip -> daftar "spoken" [[mulai, akhir, teks], ...].
Teks yang dipakai adalah teks NASKAH (bukan ejaan hasil Whisper), jadi subtitle selalu benar.

Pemakaian:
  python3 align_spoken.py naskah.txt segments.json spoken.json      # dari rekaman nyata (disarankan)
  python3 align_spoken.py naskah.txt --estimate spoken.json         # perkiraan kasar sebelum rekaman
naskah.txt: seluruh teks yang direkam (hook, cerita, penutup), paragraf dipisah baris kosong.
"""
import sys, re, json
from difflib import SequenceMatcher

def phrases(text):
    out = []
    for m in re.finditer(r"[^.,?!]+[.,?!]?[”\"]?", text.replace("\n", " ")):
        p = m.group(0).strip()
        if re.search(r"[A-Za-z0-9]", p):
            out.append(p)
    return out

def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()

def align(script, segs):
    ph = phrases(script); p = 0; out = []; warn = []
    for sg in segs:
        best = None
        for k in range(1, 5):
            if p + k > len(ph):
                break
            r = SequenceMatcher(None, norm(sg["text"]), norm(" ".join(ph[p:p + k]))).ratio()
            if best is None or r > best[0] + 0.02:
                best = (r, k)
        if best is None or best[0] < 0.35:
            warn.append("potongan %.2f-%.2f \"%s\" tidak cocok dengan naskah" % (sg["start"], sg["end"], sg["text"])); continue
        k = best[1]; chunk = ph[p:p + k]; tot = sum(len(c) for c in chunk); cur = sg["start"]
        for c in chunk:
            d = (sg["end"] - sg["start"]) * len(c) / tot
            out.append([round(cur, 2), round(cur + d, 2), c]); cur += d
        if best[0] < 0.6:
            warn.append("kecocokan rendah (%.2f) untuk \"%s\" ~ \"%s\"" % (best[0], sg["text"], " ".join(chunk)))
        p += k
    if p < len(ph):
        warn.append("kalimat naskah belum terpakai: " + " | ".join(ph[p:]))
    return out, warn

def estimate(script):
    ph = phrases(script); t = 0.3; out = []
    for c in ph:
        d = max(0.5, len(c) * 0.052)
        out.append([round(t, 2), round(t + d, 2), c])
        t += d + (0.45 if c[-1] in ".?!”\"" else 0.3)
    return out

if __name__ == "__main__":
    script = open(sys.argv[1], encoding="utf-8").read()
    if sys.argv[2] == "--estimate":
        out, warn = estimate(script), []
        dst = sys.argv[3]
    else:
        data = json.load(open(sys.argv[2], encoding="utf-8"))
        out, warn = align(script, data["segments"])
        dst = sys.argv[3]
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for w in warn:
        print("PERINGATAN:", w)
    print("%d baris ucapan ditulis ke %s%s" % (len(out), dst, "" if not warn else " (periksa peringatan)"))
