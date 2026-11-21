# Same Claim, Different Script

**A multi-form benchmark for health-claim verification in English, Urdu, and Roman Urdu.**

## What is in this repository?

- `deliverables/`: benchmark, manuscript, annotation materials, audit workbooks, and corrected Colab notebook.
- `manuscript/`: editable Markdown source for the conference manuscript.
- `results/`: preserved raw Qwen pilot outputs, original derived files, corrected denominator-aware analysis, and figures.
- `src/`: reproducible evaluation and analysis code.
- `prompts/`: versioned prompt templates.
- `configs/`: pilot configuration.
- `docs/`: repository audit, literature positioning, venue guidance, and submission checklist.
- `tests/`: automated integrity tests.

## Empirical status

The repository contains one genuine pilot run:

- Model: `Qwen/Qwen2.5-1.5B-Instruct`
- Revision: `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- 420 raw rows: 70 claims × 3 forms × 2 conditions
- Conditions: zero-shot and a **combined translation/classification prompt**
- No few-shot run and no true two-stage translation run are present

The combined prompt is preserved for auditability but must not be described as a two-stage translation intervention. The new pipeline can run a proper two-stage condition and saves the translation artifact separately.

The current manuscript reports the preserved raw JSONL counts, including 17 invalid Roman Urdu outputs in the combined-prompt condition. It should not be replaced by an uploaded draft whose tables disagree with `results/raw_outputs.jsonl`.

## Reproduce analysis

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m src.analysis \
  --raw results/raw_outputs.jsonl \
  --out results/analysis \
  --bootstrap 2000
```

The analysis reports both:

- **All-example accuracy:** invalid outputs count as incorrect.
- **Valid-output accuracy:** invalid outputs are excluded, with the valid denominator shown.

## Run a new experiment

```bash
export HF_TOKEN=...  # only if the checkpoint requires authentication
python -m src.evaluate \
  --dataset deliverables/final_benchmark_70.csv \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --condition zero_shot \
  --output results/new_zero_shot.jsonl
```

For a true two-stage translation experiment:

```bash
python -m src.evaluate \
  --dataset deliverables/final_benchmark_70.csv \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --condition translate_then_verify \
  --output results/new_two_stage.jsonl
```

Few-shot evaluation requires a separate demonstration CSV and rejects any `claim_id` overlap with the held-out benchmark.

## Scientific limitations

The benchmark labels and translations still require qualified human review. The current results are a single-model pilot and do not support general claims about multilingual models, causal script effects, or medical safety. See `docs/repository_audit.md`, `docs/final_submission_checklist.md`, and `deliverables/limitations_and_pending_work.md`.

## Citation and licensing

The code is released under the MIT License. Dataset reuse should preserve the source notes, review-status fields, and the limitation that labels are provisional until adjudication.
