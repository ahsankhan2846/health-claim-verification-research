# Pilot experiment results

## Status and scope

This report describes one genuine pilot run of `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, on the 70-claim benchmark. It is not evidence about all multilingual models.

The raw file contains two conditions:

1. `zero_shot`
2. `translate_then_verify_combined_prompt`

The second condition is retained under the original raw label `translate_then_verify`, but the prompt asked the model to translate internally and classify in one generation. It did not save an independent translation-stage output. It is therefore **not** a valid two-stage translation experiment and is reported as a combined-prompt pilot only.

No few-shot condition was run because no separate leakage-safe demonstration file was supplied.

## Run integrity

- 420 rows: 70 claims × 3 forms × 2 conditions.
- 420 unique run IDs.
- 70 claim IDs and no duplicate condition/claim/form triples.
- No execution errors.
- 31 invalid/unparsed predictions, all in the combined-prompt condition: 14 Urdu and 17 Roman Urdu.
- Seed 42, temperature 0, maximum 32 generated tokens.

## Accuracy with explicit denominators

Invalid outputs count as incorrect in **all-example accuracy**. Valid-output accuracy excludes invalid predictions and is reported separately.

| Condition | Form | Correct/all | All-example accuracy | Correct valid/valid | Valid-output accuracy | Invalid |
|---|---|---:|---:|---:|---:|---:|
| Zero-shot | English | 39/70 | 55.71% | 39/70 | 55.71% | 0 |
| Zero-shot | Urdu | 23/70 | 32.86% | 23/70 | 32.86% | 0 |
| Zero-shot | Roman Urdu | 23/70 | 32.86% | 23/70 | 32.86% | 0 |
| Combined prompt | English | 39/70 | 55.71% | 39/70 | 55.71% | 0 |
| Combined prompt | Urdu | 19/70 | 27.14% | 19/56 | 33.93% | 14 |
| Combined prompt | Roman Urdu | 18/70 | 25.71% | 18/53 | 33.96% | 17 |

The prior summary CSV's `accuracy` column is valid-output accuracy, while its `correct` column is all-example correctness. The corrected derived table `summary_corrected.csv` reports both explicitly.

## Macro-F1

Macro-F1 over valid predictions was 0.4902 English, 0.1985 Urdu, and 0.1723 Roman Urdu for zero-shot. For the combined prompt it was 0.4902 English, 0.2299 Urdu, and 0.2000 Roman Urdu. These values are unstable with 70 claims and should be treated as descriptive.

## Claim-cluster bootstrap

The corrected bootstrap uses 2,000 resamples of claim IDs and all-example correctness:

| Condition | Form | Accuracy | 95% interval |
|---|---|---:|---:|
| Zero-shot | English | 55.71% | 44.29%–68.57% |
| Zero-shot | Urdu | 32.86% | 22.86%–44.29% |
| Zero-shot | Roman Urdu | 32.86% | 22.86%–44.29% |
| Combined prompt | English | 55.71% | 42.86%–67.14% |
| Combined prompt | Urdu | 27.14% | 17.14%–37.14% |
| Combined prompt | Roman Urdu | 25.71% | 15.71%–35.71% |

## Cross-form consistency

Requiring three valid predictions:

- Zero-shot: 41/70 claims (58.57%) had the same prediction across all forms.
- Zero-shot: 18/70 claims (25.71%) were correct in all forms.
- Combined prompt: 12/70 claims (17.14%) had the same prediction across all forms.
- Combined prompt: 12/70 claims (17.14%) were correct in all forms.

## Paired tests

Exact paired McNemar tests compare claim-level correctness; Holm correction is applied within each condition:

| Condition | Comparison | Left-correct/right-wrong | Left-wrong/right-correct | Exact p | Holm p |
|---|---|---:|---:|---:|---:|
| Zero-shot | English vs Urdu | 21 | 5 | 0.002494 | 0.007482 |
| Zero-shot | English vs Roman Urdu | 21 | 5 | 0.002494 | 0.007482 |
| Zero-shot | Urdu vs Roman Urdu | 1 | 1 | 1.000000 | 1.000000 |
| Combined prompt | English vs Urdu | 21 | 1 | 0.000011 | 0.000022 |
| Combined prompt | English vs Roman Urdu | 22 | 1 | 0.0000057 | 0.0000172 |
| Combined prompt | Urdu vs Roman Urdu | 6 | 5 | 1.000000 | 1.000000 |

These tests compare this model on paired claims; they do not establish causal script effects or generalize across models.

## Interpretation limits

The English advantage is a descriptive pilot observation for one small checkpoint. The benchmark's translations and gold labels still require human validation. The combined prompt's invalid outputs make it unsuitable as evidence for a properly implemented translate-then-verify intervention. The new two-stage pipeline in `src/evaluate.py` must be run before making claims about translation-based mitigation.
