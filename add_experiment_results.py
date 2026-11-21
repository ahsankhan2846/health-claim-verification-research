from __future__ import annotations

import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
from scipy.stats import binomtest
from statsmodels.stats.multitest import multipletests


REPO = Path("/root/health_claim_verification_repo")
UPLOAD = Path("/root/.copilot/uploads/2026-11-21-be958fd8")
RESULTS = REPO / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

for name in [
    "raw_outputs.jsonl",
    "summary_by_condition_form.csv",
    "cluster_bootstrap_accuracy.csv",
    "claim_consistency.csv",
    "accuracy_heatmap.png",
    "final_benchmark_70.csv",
]:
    source = UPLOAD / name
    if source.exists():
        shutil.copy2(source, RESULTS / name)

with (RESULTS / "raw_outputs.jsonl").open(encoding="utf-8") as handle:
    raw = [json.loads(line) for line in handle if line.strip()]

assert len(raw) == 420
assert len({row["run_id"] for row in raw}) == 420
assert len({row["claim_id"] for row in raw}) == 70
assert {row["model_requested"] for row in raw} == {"Qwen/Qwen2.5-1.5B-Instruct"}
assert {row["model_resolved_version"] for row in raw} == {
    "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
}

summary = pd.read_csv(RESULTS / "summary_by_condition_form.csv")
bootstrap = pd.read_csv(RESULTS / "cluster_bootstrap_accuracy.csv")

consistency = defaultdict(list)
for row in raw:
    consistency[(row["prompting_condition"], row["claim_id"])].append(row)

consistency_records = []
for (condition, claim_id), rows in consistency.items():
    by_form = {row["form"]: row for row in rows}
    valid = [row["predicted_label"] for row in rows if row["predicted_label"] is not None]
    all_three_same = len(valid) == 3 and len(set(valid)) == 1
    all_three_correct = len(by_form) == 3 and all(
        by_form[form]["predicted_label"] == by_form[form]["gold_label"]
        for form in ("english", "urdu", "roman_urdu")
    )
    consistency_records.append({
        "condition": condition,
        "claim_id": claim_id,
        "all_three_same": all_three_same,
        "all_three_correct": all_three_correct,
    })

consistency_df = pd.DataFrame(consistency_records)
consistency_df.to_csv(RESULTS / "claim_consistency_recalculated.csv", index=False)

mcnemar_records = []
for condition in ("zero_shot", "translate_then_verify"):
    condition_rows = [row for row in raw if row["prompting_condition"] == condition]
    pivot = defaultdict(dict)
    for row in condition_rows:
        pivot[row["claim_id"]][row["form"]] = (
            row["predicted_label"] == row["gold_label"]
        )

    p_values = []
    pair_records = []
    for left, right in (
        ("english", "urdu"),
        ("english", "roman_urdu"),
        ("urdu", "roman_urdu"),
    ):
        left_only = right_only = 0
        for pair in pivot.values():
            if left in pair and right in pair:
                left_only += int(pair[left] and not pair[right])
                right_only += int(not pair[left] and pair[right])
        discordant = left_only + right_only
        p = (
            binomtest(min(left_only, right_only), discordant, 0.5).pvalue
            if discordant
            else 1.0
        )
        pair_records.append({
            "condition": condition,
            "left_form": left,
            "right_form": right,
            "left_correct_right_wrong": left_only,
            "left_wrong_right_correct": right_only,
            "discordant_pairs": discordant,
            "p_exact": p,
        })
        p_values.append(p)

adjusted = multipletests(p_values, method="holm")[1]
for record, adjusted_p in zip(pair_records, adjusted):
    record["p_holm"] = float(adjusted_p)
    mcnemar_records.append(record)

pd.DataFrame(mcnemar_records).to_csv(
    RESULTS / "mcnemar_holm.csv", index=False
)

topic_records = []
for (condition, topic, form), rows in pd.DataFrame(raw).groupby(
    ["prompting_condition", "topic", "form"], dropna=False
):
    correct = int((rows["predicted_label"] == rows["gold_label"]).sum())
    invalid = int(rows["predicted_label"].isna().sum())
    topic_records.append({
        "condition": condition,
        "topic": topic,
        "form": form,
        "n": len(rows),
        "correct": correct,
        "accuracy": correct / len(rows),
        "invalid_n": invalid,
    })
topic_df = pd.DataFrame(topic_records)
topic_df.to_csv(RESULTS / "topic_accuracy.csv", index=False)

for condition in ("zero_shot", "translate_then_verify"):
    pivot = topic_df[topic_df["condition"] == condition].pivot(
        index="topic", columns="form", values="accuracy"
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="Blues", vmin=0, vmax=1)
    plt.title(f"Topic accuracy: {condition}")
    plt.tight_layout()
    plt.savefig(
        RESULTS / f"topic_accuracy_{condition}.png",
        dpi=200,
        bbox_inches="tight",
    )
    plt.close()

result_text = """# Experiment results

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
"""
(REPO / "results" / "RESULTS_REPORT.md").write_text(result_text, encoding="utf-8")

# Update README status.
readme = REPO / "README.md"
readme_text = readme.read_text(encoding="utf-8")
readme_text = readme_text.replace(
    "Important: translation/evidence review and actual model execution remain pending",
    "Experiment status: genuine single-model raw results are present for Qwen 2.5 1.5B; translation/evidence review and few-shot execution remain pending",
)
readme.write_text(readme_text, encoding="utf-8")

# Update manuscript.
paper = Document(REPO / "deliverables" / "final_research_paper.docx")

paper.paragraphs[3].text = (
    "This paper presents a 70-claim parallel benchmark for studying whether health-claim "
    "verification changes when the same underlying claim is written in English, Urdu script, "
    "or Roman Urdu. The benchmark contains 210 language-form entries across seven topics and "
    "three provisional gold labels: Supported, Refuted, and Insufficient. In a genuine pilot "
    "run, Qwen 2.5 1.5B (revision 989aa7980e4cf806f80c7fef2b1adb7bc71aa306) achieved 55.71% "
    "English accuracy in both zero-shot and translate-then-verify conditions, compared with "
    "32.86% and 32.86% for Urdu and Roman Urdu in zero-shot, and 27.14% and 25.71% under "
    "translate-then-verify. Cross-form and paired differences are reported below. Few-shot "
    "evaluation, human translation validation, and independent source-label adjudication "
    "remain pending."
)

paper.paragraphs[18].text = (
    "The planned conditions are zero-shot verification, few-shot verification, and "
    "translate-then-verify. Few-shot demonstrations must come from a separate demonstration "
    "set that is not part of the 70-claim test benchmark. No separate few-shot file was "
    "supplied, so few-shot was not executed. The completed pilot used Qwen 2.5 1.5B "
    "(revision 989aa7980e4cf806f80c7fef2b1adb7bc71aa306), temperature 0, seed 42, and "
    "32 maximum generated tokens."
)

paper.paragraphs[22].text = (
    "In zero-shot evaluation, accuracy was 55.71% in English, 32.86% in Urdu, and 32.86% "
    "in Roman Urdu. In translate-then-verify, English remained 55.71%, while Urdu and Roman "
    "Urdu fell to 27.14% and 25.71%, respectively. Urdu and Roman Urdu had 14 and 17 invalid "
    "outputs under translate-then-verify, so the accuracy denominators are 56 and 53 valid "
    "predictions for parsable-only accuracy; the table and cluster bootstrap report correctness "
    "over all 70 claims."
)

paper.paragraphs[29].text = (
    "This pilot establishes that the proposed benchmark and pipeline can produce genuine, "
    "traceable results for a single model, but it does not establish a general multilingual "
    "performance ranking. The observed English advantage was statistically detectable in paired "
    "tests in this pilot, and translation reduced model robustness partly by increasing invalid "
    "responses. Submission should wait for translation and evidence adjudication and should "
    "avoid broader model or safety claims until additional models and conditions are run."
)

paper.save(REPO / "deliverables" / "final_research_paper.docx")

print("updated repository with genuine results")
