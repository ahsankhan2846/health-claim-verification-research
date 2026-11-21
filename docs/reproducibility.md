# Reproducibility guide

## Environment

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The preserved pilot was run with `Qwen/Qwen2.5-1.5B-Instruct`, revision
`989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, seed 42, greedy decoding, and
32 maximum new tokens. The exact configuration is in `configs/pilot_config.json`.

## Validate and analyze the released pilot

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m src.validate_dataset deliverables/final_benchmark_70.csv
.venv/bin/python -m src.analysis \
  --raw results/raw_outputs.jsonl \
  --out results/analysis \
  --bootstrap 2000
```

The analysis treats invalid outputs as incorrect for all-example accuracy and
also reports valid-output accuracy with its separate denominator. Bootstrap
resampling is clustered by `claim_id`; paired form comparisons use exact
McNemar tests with Holm correction.

## Run a new model evaluation

```bash
.venv/bin/python -m src.evaluate \
  --dataset deliverables/final_benchmark_70.csv \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --revision 989aa7980e4cf806f80c7fef2b1adb7bc71aa306 \
  --condition zero_shot \
  --output results/new_zero_shot.jsonl
```

The true two-stage condition is selected with
`--condition translate_then_verify`. It stores translation prompts and outputs
separately from the verification prompt and response. Few-shot evaluation
requires an external demonstrations file and rejects overlapping claim IDs.

## Evidence boundaries

`results/raw_outputs.jsonl` is preserved evidence and must not be edited.
Human translation review, evidence-label adjudication, additional models, and
the true two-stage/few-shot runs are not present in the released pilot.
