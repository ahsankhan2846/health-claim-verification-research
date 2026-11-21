# Repository audit

## Audit date

2026-11-21 UTC.

## Verified inventory

The repository contains a 70-claim CSV/JSONL benchmark, translation and source audit workbooks, an annotation sheet and guidelines, a DOCX manuscript, a guarded Colab notebook, raw model outputs, derived metrics, and figures.

## Raw-result verification

- `results/raw_outputs.jsonl` contains 420 rows: 70 claims × 3 forms × 2 conditions.
- There are 420 unique `run_id` values, 70 claim IDs, and no duplicate condition/claim/form triples.
- All rows use `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, seed 42, temperature 0, and 32 maximum new tokens.
- No execution errors were recorded.
- There are 31 invalid/unparsed predictions: 14 Urdu and 17 Roman Urdu rows in the combined translate-then-verify condition.

## Methodological findings

1. The raw condition named `translate_then_verify` uses one prompt that asks the model to translate internally and classify. It does **not** save an independent translation-stage output. It must not be described as a two-stage translation experiment.
2. The uploaded summary reports `accuracy` on valid predictions but also reports `correct` over all rows. For example, translate-then-verify Urdu is 19/56 valid-output accuracy (33.93%) and 19/70 all-example accuracy (27.14%). Both denominators must be reported separately.
3. The current benchmark labels and translations remain provisional. No independent human review or inter-annotator agreement is present.
4. The benchmark is balanced by topic and label, but the repository's own proposal identifies an absolute-word/label confound and near-duplicate claim families. This limits causal interpretation.
5. The current results are a single-model pilot. They cannot support claims about multilingual models generally.
6. The prior notebook combines translation and verification and does not provide a saved translation artifact. A corrected two-stage pipeline is supplied in `src/evaluate.py`.

## Engineering findings

- Earlier analysis code expected `model` and `condition`, while raw outputs use `model_requested` and `prompting_condition`; the replacement analysis pipeline accepts the raw schema.
- Earlier notebooks used environment-specific paths; the new command-line pipeline uses repository-relative arguments.
- The repository was missing a license, requirements file, prompts, tests, and a formal audit; these are now added.
- A subsequently supplied DOCX contained stronger benchmark discussion but also disagreed with the raw JSONL on invalid-output counts and condition-pair comparisons. The corrected manuscript was regenerated from the raw records; the supplied draft is not treated as an evidence source.

## Blocking external work

- Qualified Urdu/Roman Urdu semantic review.
- Independent evidence and gold-label review.
- A separate leakage-safe few-shot demonstration set.
- Additional model runs if the paper is to make claims beyond one 1.5B pilot.
- Final live URL checks and venue-specific formatting.

## External verification limitation

Outbound checks of the 43 unique benchmark source URLs returned no HTTP response in the execution environment. URL reachability and current source content therefore remain pending external verification and are not represented as completed quality checks.
