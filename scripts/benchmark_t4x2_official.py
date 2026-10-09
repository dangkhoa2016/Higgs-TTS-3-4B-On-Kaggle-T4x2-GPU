#!/usr/bin/env python3
import argparse
import hashlib
import json
import statistics
import subprocess
import threading
import time
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_AUTHORITY_DIR = ROOT / "benchmarks" / "t4x2-official-2026-10-09"
URL = "http://127.0.0.1:8000/v1/audio/speech"
HEALTH = "http://127.0.0.1:8000/health"
REPETITIONS = 3
TOP_K = 50
MAX_NEW_TOKENS = 384
CASES = [
    ("en01", "Hello. This is a Higgs TTS test running on an NVIDIA Tesla T4.", 12345, 0.8),
    ("en02", "The quick brown fox jumps over the lazy dog while the system records timing and memory usage.", 12345, 0.8),
    ("en03", "Please read this sentence naturally, clearly, and at a comfortable conversational pace.", 12345, 0.8),
    ("vi01", "Xin chào. Đây là phép thử Higgs TTS đang chạy trên GPU NVIDIA Tesla T4.", 12345, 0.8),
    ("vi02", "Hệ thống đang ghi lại thời gian tạo âm thanh, mức sử dụng bộ nhớ và độ dài tệp kết quả.", 12345, 0.8),
    ("vi03", "Hãy đọc câu này tự nhiên, rõ ràng và với tốc độ hội thoại thoải mái.", 12345, 0.8),
    ("mix01", "Xin chào, welcome to our Higgs TTS demonstration on NVIDIA Tesla T4.", 12345, 0.8),
    ("mix02", "Hôm nay chúng ta sẽ benchmark latency, memory usage, và chất lượng audio của hệ thống.", 12345, 0.8),
    ("mix03", "Please listen carefully: mô hình này có thể chuyển từ English sang tiếng Việt trong cùng một câu.", 12345, 0.8),
    ("mix04", "The system is ready. Bây giờ chúng ta bắt đầu kiểm tra khả năng code-switching giữa hai ngôn ngữ.", 12346, 0.65),
    ("mix05", "Good morning mọi người, cảm ơn bạn đã tham gia buổi thử nghiệm Higgs TTS hôm nay.", 12345, 0.8),
]


def prepare_output_dir(path: Path, allow_overwrite: bool, allow_authority_overwrite: bool) -> Path:
    path = path.resolve()
    canonical = CANONICAL_AUTHORITY_DIR.resolve()
    if path == canonical and not allow_authority_overwrite:
        raise SystemExit("Refusing canonical authority directory without --allow-authority-overwrite")
    if path.exists() and any(path.iterdir()) and not allow_overwrite:
        raise SystemExit(f"Refusing non-empty output directory without --allow-overwrite: {path}")
    path.mkdir(parents=True, exist_ok=True)
    return path


def gpu_line():
    exe = "/opt/bin/nvidia-smi"
    command = [exe, "--query-gpu=index,memory.used,memory.free,utilization.gpu", "--format=csv,noheader,nounits"]
    proc = subprocess.run(command, capture_output=True, text=True, check=True)
    rows = []
    for line in proc.stdout.strip().splitlines():
        fields = [part.strip() for part in line.split(",")]
        rows.append({"gpu": int(fields[0]), "used_mib": int(fields[1]), "free_mib": int(fields[2]), "util_pct": int(fields[3])})
    return rows


def wav_info(path: Path):
    with wave.open(str(path), "rb") as wav:
        return {
            "duration_s": wav.getnframes() / wav.getframerate(),
            "sample_rate": wav.getframerate(),
            "channels": wav.getnchannels(),
            "frames": wav.getnframes(),
        }


def request_case(out_dir: Path, case_id: str, text: str, seed: int, temp: float, rep: int):
    payload = {"input": text, "seed": seed, "temperature": temp, "top_k": TOP_K, "max_new_tokens": MAX_NEW_TOKENS}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"}, method="POST")
    samples = []
    stop = threading.Event()

    def monitor():
        while not stop.is_set():
            try:
                samples.append({"t": time.time(), "gpus": gpu_line()})
            except Exception as exc:
                samples.append({"t": time.time(), "error": str(exc)})
            stop.wait(0.20)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    started = time.perf_counter()
    status = None
    body = b""
    error = None
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            status = response.status
            body = response.read()
    except Exception as exc:
        error = repr(exc)
    wall = time.perf_counter() - started
    stop.set()
    thread.join(timeout=2)
    wav_path = out_dir / f"{case_id}-r{rep}.wav"
    if body:
        wav_path.write_bytes(body)
    record = {
        "case": case_id, "rep": rep, "seed": seed, "temperature": temp,
        "top_k": TOP_K, "max_new_tokens": MAX_NEW_TOKENS,
        "http_status": status, "wall_s": wall, "error": error, "gpu_samples": samples,
    }
    if body and status == 200:
        info = wav_info(wav_path)
        record.update(info)
        record["rtf"] = wall / info["duration_s"]
        record["audio_per_wall"] = info["duration_s"] / wall
        record["size_bytes"] = len(body)
        record["sha256"] = hashlib.sha256(body).hexdigest()
    peaks = {0: {"used_mib": 0, "util_pct": 0}, 1: {"used_mib": 0, "util_pct": 0}}
    for sample in samples:
        for gpu in sample.get("gpus", []):
            peak = peaks[gpu["gpu"]]
            peak["used_mib"] = max(peak["used_mib"], gpu["used_mib"])
            peak["util_pct"] = max(peak["util_pct"], gpu["util_pct"])
    record["gpu_peak"] = peaks
    return record


def summarize(rows):
    ok = [row for row in rows if row.get("http_status") == 200]
    by_case = {}
    for row in ok:
        by_case.setdefault(row["case"], []).append(row)
    case_summary = {}
    for case_id, values in by_case.items():
        hashes = [row["sha256"] for row in values]
        case_summary[case_id] = {
            "n": len(values),
            "latency_mean_s": statistics.mean(row["wall_s"] for row in values),
            "latency_median_s": statistics.median(row["wall_s"] for row in values),
            "duration_mean_s": statistics.mean(row["duration_s"] for row in values),
            "rtf_mean": statistics.mean(row["rtf"] for row in values),
            "gpu0_peak_used_mib": max(row["gpu_peak"][0]["used_mib"] for row in values),
            "gpu1_peak_used_mib": max(row["gpu_peak"][1]["used_mib"] for row in values),
            "hash_reproducible": len(set(hashes)) == 1,
            "hashes": hashes,
        }
    return {
        "status": "PASS" if len(ok) == len(rows) else "PARTIAL",
        "requests_total": len(rows), "requests_http200": len(ok), "cases": len(CASES), "repetitions": REPETITIONS,
        "overall": {
            "latency_mean_s": statistics.mean(row["wall_s"] for row in ok),
            "latency_median_s": statistics.median(row["wall_s"] for row in ok),
            "rtf_mean": statistics.mean(row["rtf"] for row in ok),
            "gpu0_peak_used_mib": max(row["gpu_peak"][0]["used_mib"] for row in ok),
            "gpu1_peak_used_mib": max(row["gpu_peak"][1]["used_mib"] for row in ok),
            "aggregate_audio_s": sum(row["duration_s"] for row in ok),
            "aggregate_wall_s": sum(row["wall_s"] for row in ok),
        },
        "case_summary": case_summary,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--allow-overwrite", action="store_true")
    parser.add_argument("--allow-authority-overwrite", action="store_true")
    args = parser.parse_args()
    out_dir = prepare_output_dir(args.output_dir, args.allow_overwrite, args.allow_authority_overwrite)
    with urllib.request.urlopen(HEALTH, timeout=10) as response:
        health = json.loads(response.read())
    meta = {
        "started_at_epoch": time.time(), "health": health, "gpu_idle_before": gpu_line(),
        "repetitions": REPETITIONS, "sampling_interval_s": 0.20,
        "profile": "T4x2 stage placement; GPU0 tts_engine; GPU1 audio_encoder+vocoder; sequential; fixed seed per case",
        "cold_start_policy": "Cold FlashInfer JIT excluded from warm benchmark; preserved separately in prior evidence.",
    }
    (out_dir / "benchmark-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    warm = request_case(out_dir, "warmup", "Warm benchmark initialization.", 424242, 0.8, 0)
    (out_dir / "warmup.json").write_text(json.dumps(warm, ensure_ascii=False, indent=2))
    rows = []
    for rep in range(1, REPETITIONS + 1):
        for case_id, text, seed, temp in CASES:
            record = request_case(out_dir, case_id, text, seed, temp, rep)
            rows.append(record)
            (out_dir / "results.partial.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    summary = summarize(rows)
    summary["overall"]["aggregate_rtf"] = summary["overall"]["aggregate_wall_s"] / summary["overall"]["aggregate_audio_s"]
    (out_dir / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary["overall"], indent=2))


if __name__ == "__main__":
    main()
