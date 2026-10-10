# Lịch sử phát triển

> 🌐 Ngôn ngữ / Language: [English](development-history.md) | **Tiếng Việt**

Lịch sử này tách các engineering milestone có evidence khỏi pre-publication clean-history assembly. Trước lần community publication đầu tiên, các file liên quan có thể được fold vào focused commit đại diện cho concern cần review; retained evidence timestamps vẫn là authority cho chronology của experiment/runtime.

## 2026-10-08 — model và runtime qualification

Project dùng Kaggle mirror hiện có `dangkhoa2016/bosonai-higgs-tts-3-4b`, original model weights và runtime FP16 SGLang-Omni. Một Tesla T4 tạo speech thành công sau khi FlashInfer cold-JIT link path được xử lý bằng `LD_LIBRARY_PATH=/usr/local/nvidia/lib64:${LD_LIBRARY_PATH:-}` cùng `LIBRARY_PATH=/usr/local/nvidia/lib64:${LIBRARY_PATH:-}`.

Functional validation kiểm tra English, Vietnamese, control tokens, mixed-language prompts và synthetic-reference voice-clone transport. Human review cũng phát hiện các perceptual failure thực: VI02 mất từ đầu, MIX02 mất từ đầu, MIX03 gần như silent, MIX04 mất từ English đầu tiên và original synthetic voice-clone reference nghe quá low/heavy.

## 2026-10-08 — single-T4 headroom failure và T4x2 recovery

single-T4 headroom qualification giữ lại production-headroom failure: sau warm/reference use GPU0 gần như hết free memory và MIX02 bị CUDA OOM. Kết quả này trở thành negative evidence thay vì bị che giấu.

T4x2 stage-placement qualification chuyển `audio_encoder` và `vocoder` sang GPU1, giữ `tts_engine` trên GPU0 và preprocessing trên CPU. Tensor parallelism tiếp tục disabled. Mixed-language suite 5 case sau đó đạt 5/5 HTTP 200 và phục hồi MIX02 trước đó bị OOM.

## 2026-10-09 — onset root-cause audit và perceptual acceptance

Static và raw-code audits loại trừ tokenizer text loss, delay-pattern off-by-one, codec/WAV assembly clipping, max-token truncation và request concurrency khỏi nguồn gây onset failures. Raw-code re-decode và API WAV output có correlation khoảng 0.9999998 hoặc cao hơn.

Classification được giữ là `zero-shot AR acoustic-generation/bootstrap instability before codec decode`, với high confidence cho layer localization trong khi exact learned-model internal mechanism vẫn unproven.

Fixed-seed zero-shot variants cải thiện các case bị ảnh hưởng. SLT-conditioned diagnostic cải thiện onset stability nhưng tạo Vietnamese regional/tone characteristics không mong muốn và bị reject làm production default. MIX04 cuối cùng được human approval tại seed 12346, temperature 0.65, sau đó loudness normalization.

## 2026-10-09 — production packaging và official warm benchmark

Production helpers, readiness checks, smoke validation, runtime lock data và migration bundle được chuẩn bị. Official warm T4x2 benchmark chạy tuần tự 11 cases x 3 repetitions: 33/33 HTTP 200, mean latency khoảng 6.014 s, aggregate RTF khoảng 1.086832 và GPU peaks 10,951/4,511 MiB.

Mười trên mười một case byte-stable ngay trong ba repetitions đầu. EN02 diverge ở first observation rồi tạo bốn kết quả byte-identical liên tiếp; cause vẫn unproven.

## 2026-10-09 — clean public-history rebuild

Initial GitHub publication bị reject vì commits được tạo cách nhau vài giây và trông như bulk import. Repository vì vậy được rebuild từ clean root bằng retained engineering authority, small reviewable commits, bilingual documentation, MIT licensing, governance, tests, CI và explicit preservation of failures.

Rewrite không fabricate historical commit timestamps. Historical engineering dates nằm trong tài liệu này và retained evidence; Git commits ghi thời điểm rewrite thực sự diễn ra.

## 2026-10-09 — Kaggle production showcase và public release đầu tiên

Repository bổ sung Kaggle T4x2 production showcase notebook có thể import trực tiếp để reviewer bắt đầu từ GitHub release, attach Kaggle model mirror hiện có, chạy service thật, nghe multilingual acceptance outputs và rerun official benchmark từ fresh session. Notebook verify annotated tag `v1.0.0` resolve đúng checked-out HEAD thay vì nhúng một commit hash tự tham chiếu.

Sau khi clean-history branch PASS local repository verification và GitHub Actions, annotated tag `v1.0.0` trở thành public release boundary đầu tiên. Voice-clone production acceptance vẫn pending; release không nâng unresolved perceptual claim này thành production claim.
