#!/usr/bin/env bash
# Menggabungkan rekaman suara lengkap (hook + cerita + penutup) ke video tanpa suara.
# Musik mengecil otomatis saat suara bicara.
# Pemakaian:  ./add_voiceover.sh voiceover.mp3 [video.mp4] [hasil.mp4]   (jalankan di folder yang berisi timeline.env)
set -euo pipefail
. ./timeline.env   # VO_DELAY, TOTAL
VO="${1:?beri file voiceover.mp3}"
IN="${2:-video-tanpa-suara.mp4}"
OUT="${3:-video-final.mp4}"
D=$(python3 -c "print(int(round($VO_DELAY*1000)))")
ffmpeg -y -loglevel error -i "$IN" -i "$VO" -filter_complex \
"[1:a]adelay=${D}|${D},highpass=f=70,loudnorm=I=-16:TP=-1.5,apad=whole_dur=${TOTAL},asplit=2[vo][sc]; \
[0:a]volume=0.8[bg]; \
[bg][sc]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=400[duck]; \
[duck][vo]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$TOTAL" "$OUT"
echo "Selesai: $OUT"
