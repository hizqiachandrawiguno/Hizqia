#!/usr/bin/env bash
# Menggabungkan voice over (hasil ElevenLabs) ke video. Musik otomatis mengecil saat suara bicara.
# Pemakaian: ./add_voiceover.sh voiceover.mp3 [video-masuk.mp4] [video-keluar.mp4]
set -euo pipefail
VO="${1:?beri file voice over (mp3/wav)}"
IN="${2:-daud-vs-goliat-9x16.mp4}"
OUT="${3:-daud-vs-goliat-9x16-vo.mp4}"
VD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VO")
# Jika suara lebih panjang dari 65 dtk, dipercepat sedikit (maks 1.15x) agar muat.
TEMPO=$(python3 -c "d=float('$VD'); print(min(1.15, max(1.0, d/65.0)))")
echo "Durasi suara: ${VD}s, tempo: ${TEMPO}"
ffmpeg -y -loglevel error -i "$IN" -i "$VO" -filter_complex \
"[1:a]atempo=${TEMPO},adelay=300|300,highpass=f=70,loudnorm=I=-16:TP=-1.5,apad=whole_dur=66,asplit=2[vo][sc]; \
[0:a]volume=0.8[bg]; \
[bg][sc]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=400[duck]; \
[duck][vo]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t 66 "$OUT"
echo "Selesai: $OUT"
