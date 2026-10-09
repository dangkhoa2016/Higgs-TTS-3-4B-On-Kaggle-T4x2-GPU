# Known Limitations

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](known-limitations.vi.md)

## Qualified hardware scope

The accepted baseline is Kaggle NVIDIA Tesla T4 x2 with the recorded runtime stack and stage placement. The repository does not establish universal compatibility for every T4 host, CUDA/driver combination, or alternate deployment environment.

## Single-T4 production headroom

A single T4 can run functional inference, but the qualified single-T4 headroom qualification state failed production headroom. MIX02 hit CUDA OOM after the pipeline had consumed almost all GPU0 memory. Single-T4 is therefore not the production-safe baseline claimed by this project.

## Zero-shot onset instability

Historical VI02/MIX02 onset loss, MIX03 near-silence, and MIX04 onset behavior were localized with high confidence to zero-shot autoregressive acoustic generation/bootstrap before codec decode.

The exact learned-model internal mechanism remains unproven. Documentation must not convert the localization result into a stronger causal claim.

## Reference-conditioned diagnostic path

The synthetic SLT reference improved onset stability during diagnosis, but human review found undesirable Vietnamese regional-accent/tone realization. That conditioned path is diagnostic only and is rejected as the current production default.

## Voice cloning

Voice-clone transport/runtime works with synthetic references, but final perceptual production acceptance is still pending. The repository does not claim production-ready voice cloning and does not use real-person voice cloning for its tests.

## Bitwise determinism

Ten of eleven official benchmark cases were immediately byte-identical across three repetitions. EN02 diverged on the first observation and then produced four consecutive byte-identical results. The cause is unproven, so universal request-level bitwise determinism is not claimed.

## Warm benchmark scope

The official performance numbers describe a warm runtime. FlashInfer cold JIT is intentionally excluded and may add substantial first-use time on a fresh environment.

## Heavy artifacts

Model weights, the Python virtual environment, benchmark WAVs, raw benchmark telemetry, and the captured FlashInfer cache tarball are intentionally excluded from Git. Their absence is a repository packaging decision, not evidence that those artifacts never existed during qualification.

## Reviewer-showcase text coverage and silent tails

A fresh 2026-10-09 reviewer run exposed three additional perceptual/content failures: `NARR01` omitted the initial word “At”, `MIX01` did not verbalize the literal technical token `x2`, and zero-shot `VI01` produced speech only for the first sentence followed by about 26 seconds of near-silence. The run is retained in `evidence/kaggle-showcase-human-review-2026-10-09.json`. The notebook now adds a waveform-activity gate for sustained silence, normalizes spoken `T4 x2` to “hai GPU T4”, and keeps token-coverage/perceptual acceptance explicitly dependent on human listening.
