#!/usr/bin/env bash
# Memasang mesin transkrip Whisper (offline, via sherpa-onnx) sekali saja.
# Hasil: model di $ASR_DIR (bawaan ~/.cache/tokoh-alkitab/whisper-small).
# Butuh akses ke github.com (rilis model) dan PyPI. Tidak mengirim audio ke mana pun.
set -euo pipefail
ASR_DIR="${ASR_DIR:-$HOME/.cache/tokoh-alkitab}"
mkdir -p "$ASR_DIR"
python3 -c "import sherpa_onnx" 2>/dev/null || pip install -q sherpa-onnx
if [ ! -f "$ASR_DIR/sherpa-onnx-whisper-small/small-encoder.int8.onnx" ]; then
  cd "$ASR_DIR"
  curl -sS -L -o whisper-small.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2"
  tar -xjf whisper-small.tar.bz2 && rm -f whisper-small.tar.bz2
fi
echo "$ASR_DIR/sherpa-onnx-whisper-small"
