# Troubleshooting

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](troubleshooting.vi.md)

## FlashInfer JIT cannot find `-lcuda`

Observed symptom: a fresh environment fails while linking FlashInfer JIT operators because the linker cannot find `-lcuda`.

Use:

```bash
export LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}
```

Then restart the qualified server path. A retry may still take longer while cold JIT completes; the official benchmark excludes this cold compilation interval.

## Single-T4 CUDA OOM after warmup/reference use

This is a known qualified failure, not an installation mystery. Phase 5 recorded only about 65 MiB free on GPU0 after voice-clone use, followed by MIX02 failing when an additional allocation was required.

Do not treat one T4 as the production baseline. Use the accepted T4x2 stage placement from `production/serve-t4x2.sh`.

## Readiness fails

`production/readiness.sh` verifies two GPUs, the mounted model, the service health payload, and required pipeline stages. Resolve the specific printed failure before sending inference traffic.

Common checks:

```bash
nvidia-smi
ls /kaggle/input/models/dangkhoa2016/bosonai-higgs-tts-3-4b/transformers/default/1/model.safetensors
curl -fsS http://127.0.0.1:8000/health
```

## Benchmark refuses the output directory

This is intentional. The harness refuses a non-empty destination unless overwrite is explicitly enabled, and it applies an additional protection to the retained official authority directory.

For normal reruns, choose a new directory or use `production/run-official-benchmark.sh` without an output argument.

## Optional FlashInfer cache is missing

The Git repository does not carry the cache tarball. `production/restore-flashinfer-cache.sh` treats absence as non-fatal and exits successfully after reporting that cold JIT may run.

## Audio content differs despite a fixed seed

Do not immediately classify this as corruption. EN02 demonstrated one first-observation divergence followed by four byte-identical outputs. Compare runtime/model authority first, preserve the differing artifact, and do not claim a cause without evidence.

## Voice clone sounds too low or regionally colored

Runtime transport passing does not make the clone production-approved. The original KAL synthetic reference was judged too low/heavy, while the SLT-conditioned diagnostic introduced undesirable Vietnamese regional/tone characteristics. Current policy keeps voice-clone production acceptance pending.
