# Experiment results

## Run identity

- Model: `Qwen/Qwen2.5-1.5B-Instruct`
- Resolved revision SHA: `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- Run date: 2026-11-21 UTC
- Seed: 42
- Temperature: 0
- Maximum new tokens: 32
- Conditions: zero-shot and translate-then-verify
- No few-shot condition was run because no separate, leakage-safe demonstration file was supplied.

## Integrity

The raw file contains 420 rows: 210 for zero-shot and 210 for translate-then-verify. It covers 70 claim IDs and three forms, with 420 unique run IDs and no execution errors. There are 31 invalid/unparsed outputs, all in translate-then-verify: 14 in Urdu and 17 in Roman Urdu.

## Main accuracy

Accuracy below is correctness divided by all 70 claims in the form. Separate valid-output accuracy and macro-F1 are reported by the uploaded summary table.

| Condition | English | Urdu | Roman Urdu |
|---|---:|---:|---:|
| Zero-shot | 39/70 (55.71%) | 23/70 (32.86%) | 23/70 (32.86%) |
| Translate-then-verify | 39/70 (55.71%) | 19/70 (27.14%) | 18/70 (25.71%) |

Zero-shot macro-F1 was 0.4902 for English, 0.1985 for Urdu, and 0.1723 for Roman Urdu. Translate-then-verify macro-F1 was 0.4902 for English, 0.2299 for Urdu, and 0.2000 for Roman Urdu.

## Cluster bootstrap

The supplied 95% claim-cluster bootstrap intervals use 2,000 resamples:

| Condition | Form | Accuracy | 95% interval |
|---|---|---:|---:|
| Zero-shot | English | 55.71% | 44.29%-68.57% |
| Zero-shot | Urdu | 32.86% | 22.86%-44.29% |
| Zero-shot | Roman Urdu | 32.86% | 22.86%-44.29% |
| Translate-then-verify | English | 55.71% | 42.86%-67.14% |
| Translate-then-verify | Urdu | 27.14% | 17.14%-37.14% |
| Translate-then-verify | Roman Urdu | 25.71% | 15.71%-35.71% |

## Cross-form consistency

With a valid prediction for all three forms required:

- Zero-shot: 41/70 claims (58.57%) had the same prediction across all forms.
- Zero-shot: 18/70 claims (25.71%) were correct in all three forms.
- Translate-then-verify: 12/70 claims (17.14%) had the same prediction across all forms.
- Translate-then-verify: 12/70 claims (17.14%) were correct in all three forms.

## Paired McNemar tests

Exact paired McNemar tests compare per-claim correctness within each condition. Holm correction was applied across the three form pairs in each condition.

| Condition | Comparison | Correct-left/wrong-right | Wrong-left/correct-right | Exact p | Holm p |
|---|---|---:|---:|---:|---:|
| Zero-shot | English vs Urdu | 21 | 5 | 0.002494 | 0.007482 |
| Zero-shot | English vs Roman Urdu | 21 | 5 | 0.002494 | 0.007482 |
| Zero-shot | Urdu vs Roman Urdu | 1 | 1 | 1.000000 | 1.000000 |
| Translate-then-verify | English vs Urdu | 21 | 1 | 0.000011 | 0.000022 |
| Translate-then-verify | English vs Roman Urdu | 22 | 1 | 0.0000057 | 0.0000172 |
| Translate-then-verify | Urdu vs Roman Urdu | 6 | 5 | 1.000000 | 1.000000 |

## Interpretation limits

These are pilot findings for one 1.5B-parameter model, not evidence for a general effect across model families. The dataset and its gold labels remain pending independent evidence review and translation review. Translate-then-verify introduced substantially more invalid outputs, so accuracy and consistency figures must be interpreted with missingness. No native-speaker review, inter-annotator agreement, or source verification has been claimed.

The claim-cluster bootstrap preserves claim IDs but does not validate external generalizability; the 70 claims are a constructed benchmark rather than a population sample.
