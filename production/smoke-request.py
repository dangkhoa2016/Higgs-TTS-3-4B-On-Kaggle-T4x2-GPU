#!/usr/bin/env python3
import hashlib
import json
import os
import urllib.request
import wave
from pathlib import Path

url = os.environ.get("HIGGS_SMOKE_URL", "http://127.0.0.1:8000/v1/audio/speech")
out = Path(os.environ.get("HIGGS_SMOKE_OUTPUT", "outputs/production-smoke.wav"))
payload = {
    "input": "Hello from the Higgs TTS T4x2 production smoke test.",
    "seed": 12345,
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 384,
}
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=120) as response:
    body = response.read()
    status = response.status
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(body)
with wave.open(str(out), "rb") as wav:
    meta = {
        "http_status": status,
        "sample_rate": wav.getframerate(),
        "channels": wav.getnchannels(),
        "duration_s": wav.getnframes() / wav.getframerate(),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "path": str(out),
    }
assert status==200 and meta['sample_rate']==24000 and meta['channels']==1 and meta['duration_s']>0, meta
print(json.dumps(meta, indent=2))
