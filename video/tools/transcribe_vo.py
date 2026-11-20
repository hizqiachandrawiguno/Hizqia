import sys, re, subprocess, wave, json
import numpy as np
import sherpa_onnx
mp3, model_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
wav = out + ".16k.wav"
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",mp3,"-ac","1","-ar","16000",wav])
w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
dur = len(x)/sr
r = subprocess.run(["ffmpeg","-hide_banner","-i",wav,"-af","silencedetect=noise=-38dB:d=0.2","-f","null","-"],capture_output=True,text=True).stderr
starts=[float(m) for m in re.findall(r"silence_start: ([\d.]+)",r)]
ends=[float(m) for m in re.findall(r"silence_end: ([\d.]+)",r)]
# segmen bicara = di antara akhir hening dan awal hening berikutnya
segs=[]; cur=0.0
for s,e in zip(starts,ends):
    if s-cur>0.12: segs.append((cur,s))
    cur=e
if dur-cur>0.12: segs.append((cur,dur))
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{model_dir}/small-encoder.int8.onnx", decoder=f"{model_dir}/small-decoder.int8.onnx",
    tokens=f"{model_dir}/small-tokens.txt", language="id", task="transcribe", num_threads=4)
res=[]
for a,b in segs:
    pa=max(0,a-0.15); pb=min(dur,b+0.15)
    st=rec.create_stream(); st.accept_waveform(sr, x[int(pa*sr):int(pb*sr)])
    rec.decode_stream(st)
    res.append({"start":round(a,2),"end":round(b,2),"text":st.result.text.strip()})
    print(f"{a:6.2f} {b:6.2f}  {st.result.text.strip()}", flush=True)
json.dump(res,open(out,"w"),ensure_ascii=False,indent=1)
