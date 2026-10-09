# Kaggle Production Showcase

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

The canonical public notebook is [`kaggle-production-showcase.ipynb`](kaggle-production-showcase.ipynb). It is a **reviewer-facing bilingual guided demo** for the qualified Higgs TTS 3 4B deployment on Kaggle NVIDIA Tesla T4 x2.

The notebook is intentionally structured like the recent public production notebooks in this project family: each major phase has a short English/Vietnamese explanation, observable code output, explicit evidence gates, and a final machine-readable acceptance record.

## Before you run

1. Create or open a Kaggle Notebook.
2. Choose **File → Import Notebook → GitHub**.
3. Select `dangkhoa2016/Kaggle-T4x2-Qualification-for-Higgs-TTS-3-4B` and `notebooks/kaggle-production-showcase.ipynb`.
4. Set the accelerator to **GPU T4 x2**.
5. Turn **Internet ON** so the notebook can clone the immutable release tag.
6. Use **Add Input → Models** and attach:
   - model: `dangkhoa2016/bosonai-higgs-tts-3-4b`
   - variation: `transformers/default`
   - version: `1`
7. Start from a fresh session and use **Run All**.

Model weights are read only from the attached Kaggle Model mount. The notebook does not download the model from Hugging Face, does not use GGUF, and does not perform real-person voice cloning.

## Guided flow

The notebook currently contains 44 cells: 24 Markdown cells and 20 code cells. The flow is deliberately reviewer-oriented rather than a compact automation script.

1. **Release + architecture overview** — states the release, hardware, model input, stage placement, and acceptance boundaries.
2. **Immutable release bootstrap** — clones annotated tag `v1.0.0`, verifies the tag object type, and proves its peeled target equals the checked-out commit.
3. **T4 x2 + model preflight** — checks Kaggle, Python 3.12, `uv`, two Tesla T4 GPUs, and the attached Version 1 safetensors mount before runtime installation.
4. **Qualified runtime creation** — builds the Python 3.12 virtual environment from `production/requirements-runtime-lock.txt`.
5. **Runtime provenance** — prints Python, PyTorch/CUDA, SGLang, SGLang-Omni, FlashInfer, and GPU memory state.
6. **Real service launch** — starts the production T4x2 helper with the retained FlashInfer cold-JIT linker requirement.
7. **Readiness + smoke** — waits for real `/health`, runs the public readiness script, then performs an actual WAV smoke request.
8. **Reviewer-facing voice showcase** — generates four synthetic reference voice candidates A–D, previews them, then runs eight longer listening cases separately so each case has its own explanation, conditioning metadata, metrics, and inline audio player.
9. **Showcase evidence table** — writes `synthetic-reference-voices.json` and `showcase-suite.json`, displays request/audio metadata for all eight main cases, and adds RMS-based activity metrics that fail closed on long silent tails.
10. **Official warm benchmark rerun** — invokes the repository's official benchmark entrypoint in a fresh evidence directory.
11. **Final machine-readable acceptance** — writes `FINAL-ACCEPTANCE.json` and prints `ACCEPTANCE=PASS` only after the executable gates succeed.
12. **Optional cleanup + limitations** — keeps the service alive by default for review, then documents exactly what the notebook does and does not prove.

## Reviewer-facing listening cases

The eight main showcase cases are not hidden inside one batch cell. Each is executed and displayed independently after the four synthetic reference voice previews:

| Case | Conditioning | Voice profile | Focus |
| --- | --- | --- | --- |
| `EN01` | zero-shot | `ZERO_SHOT` | Long English baseline |
| `VI01` | zero-shot | `ZERO_SHOT` | Long Vietnamese baseline |
| `MIX01` | synthetic reference | `VOICE_B` | Vietnamese → English code-switch |
| `ONSET01` | synthetic reference | `VOICE_A` | Vietnamese onset retention |
| `EN02` | synthetic reference | `VOICE_B` | Long English conditioned comparison |
| `VI02` | synthetic reference | `VOICE_C` | Long Vietnamese conditioned comparison |
| `MIX02` | synthetic reference | `VOICE_C` | English → Vietnamese → English code-switch |
| `NARR01` | synthetic reference | `VOICE_D` | Long-form bilingual narration |

Every case performs a real `POST /v1/audio/speech`, validates mono 24 kHz WAV output plus a minimum listening duration, records conditioning mode, voice profile, latency, duration, RTF and SHA-256, then renders an `IPython.display.Audio` player immediately below the case. Reference-conditioned cases use the model-card `references[{audio_path,text}]` contract with WAVs generated inside the same notebook session.

These are **human-listening samples**. Passing their transport/audio-format gates does not replace perceptual review and does not upgrade the pending voice-clone production claim.

## Evidence output

Successful execution writes evidence under:

```text
/kaggle/working/higgs-tts-v1.0.0-acceptance/
```

Key files include `server.log`, `production-smoke.wav`, four synthetic reference WAVs, eight showcase WAVs, `synthetic-reference-voices.json`, `showcase-suite.json`, `official-benchmark-rerun/summary.json`, and `FINAL-ACCEPTANCE.json`.

The final JSON binds the resolved release commit, tag object type, attached model version, T4x2 stage placement, readiness/smoke results, executed showcase cases, benchmark summary, and retained acceptance boundary.

## Acceptance boundary

`ACCEPTANCE=PASS` means the notebook's executable release, hardware, model, runtime, service, smoke, showcase-transport, and benchmark gates completed successfully in that session. It does **not** claim universal T4 compatibility, universal request-level bitwise determinism, a proven exact neural mechanism for onset instability, or production-ready voice cloning.
