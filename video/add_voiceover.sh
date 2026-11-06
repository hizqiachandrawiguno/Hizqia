#!/usr/bin/env bash
# Menggabungkan voice over ke video. Musik otomatis mengecil saat suara bicara.
# Pemakaian:  ./add_voiceover.sh [voiceover.mp3] [video.mp4] [hasil.mp4]
# Opsional: jika ada hook.mp3 (kalimat pembuka) dan/atau outro.mp3 (kalimat penutup)
# di folder ini, keduanya ikut dimasukkan di kartu pembuka dan penutup.
set -euo pipefail
cd "$(dirname "$0")"
. ./timeline.env   # HOOK, VO_DELAY, OUTRO_START, TOTAL (dibuat otomatis oleh make_video.py)
VO="${1:-voiceover.mp3}"
IN="${2:-daud-vs-goliat-9x16.mp4}"
OUT="${3:-daud-vs-goliat-9x16-vo.mp4}"
ms() { python3 -c "print(int(round($1*1000)))"; }
inputs=(-i "$IN" -i "$VO")
chains="[1:a]adelay=$(ms $VO_DELAY)|$(ms $VO_DELAY)[v1];"
mix="[v1]"; n=1; idx=2
if [ -f hook.mp3 ]; then
  inputs+=(-i hook.mp3); chains+="[${idx}:a]adelay=150|150[v${idx}];"; mix+="[v${idx}]"; n=$((n+1)); idx=$((idx+1))
fi
if [ -f outro.mp3 ]; then
  O=$(ms "$OUTRO_START+0.3")
  inputs+=(-i outro.mp3); chains+="[${idx}:a]adelay=${O}|${O}[v${idx}];"; mix+="[v${idx}]"; n=$((n+1)); idx=$((idx+1))
fi
ffmpeg -y -loglevel error "${inputs[@]}" -filter_complex \
"${chains}${mix}amix=inputs=${n}:normalize=0,highpass=f=70,loudnorm=I=-16:TP=-1.5,apad=whole_dur=${TOTAL},asplit=2[vo][sc]; \
[0:a]volume=0.8[bg]; \
[bg][sc]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=400[duck]; \
[duck][vo]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$TOTAL" "$OUT"
echo "Selesai: $OUT"
