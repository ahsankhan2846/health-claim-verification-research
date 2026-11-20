"""Reproducible analysis for the three-form health-claim benchmark.

The script analyzes verified raw model outputs only. It never creates model
predictions and exits with a clear message when no raw output file is present.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.stats import chi2
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from sklearn.metrics import accuracy_score, f1_score


LABELS = ["Supported", "Refuted", "Insufficient"]
FORMS = ["english", "urdu", "roman_urdu"]


def normalize_prediction(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    text = " ".join(text.split())
    if text in {"supported", "support", "true", "entailment", "yes"}:
        return "Supported"
    if text in {"refuted", "refute", "false", "contradiction", "no"}:
        return "Refuted"
    if text in {"insufficient", "insufficient evidence", "unknown", "uncertain", "mixed"}:
        return "Insufficient"
    return None


def load_outputs(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No raw output file found at {path}")
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            item["predicted_label_normalized"] = normalize_prediction(
                item.get("predicted_label", item.get("raw_response"))
            )
            item["form"] = str(item.get("form", "")).lower()
            rows.append(item)
    if not rows:
        raise ValueError(f"Raw output file {path} is empty")
    frame = pd.DataFrame(rows)
    required = {"claim_id", "form", "gold_label", "predicted_label_normalized"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Raw output file is missing required columns: {sorted(missing)}")
    frame["correct"] = frame["predicted_label_normalized"] == frame["gold_label"]
    frame["invalid_output"] = frame["predicted_label_normalized"].isna()
    return frame


def summarize(frame: pd.DataFrame) -> pd.DataFrame:
    records = []
    for form, group in frame.groupby("form", dropna=False):
        y_true = group["gold_label"]
        y_pred = group["predicted_label_normalized"].fillna("__invalid__")
        records.append({
            "form": form,
            "n": len(group),
            "correct": int(group["correct"].sum()),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
            "invalid_n": int(group["invalid_output"].sum()),
            "invalid_rate": float(group["invalid_output"].mean()),
        })
    return pd.DataFrame(records)


def claim_consistency(frame: pd.DataFrame) -> pd.DataFrame:
    pivot = frame.pivot_table(index="claim_id", columns="form", values="predicted_label_normalized", aggfunc="first")
    for form in FORMS:
        if form not in pivot:
            pivot[form] = np.nan
    pivot = pivot[FORMS]
    pivot["all_three_same"] = pivot.nunique(axis=1, dropna=False).eq(1)
    pivot["all_three_correct"] = (
        frame.pivot_table(index="claim_id", columns="form", values="gold_label", aggfunc="first")
        .reindex(columns=FORMS)
        .eq(pivot)
        .all(axis=1)
    )
    return pivot.reset_index()


def cluster_bootstrap(frame: pd.DataFrame, statistic, n_resamples: int = 2000, seed: int = 42) -> tuple[float, float, float]:
    claims = frame["claim_id"].drop_duplicates().to_numpy()
    rng = np.random.default_rng(seed)
    observed = float(statistic(frame))
    samples = []
    for _ in range(n_resamples):
        chosen = rng.choice(claims, size=len(claims), replace=True)
        pieces = [frame[frame["claim_id"] == claim] for claim in chosen]
        boot = pd.concat(pieces, ignore_index=True)
        samples.append(float(statistic(boot)))
    lower, upper = np.quantile(samples, [0.025, 0.975])
    return observed, float(lower), float(upper)


def paired_mcnemar(frame: pd.DataFrame) -> pd.DataFrame:
    wide = frame.pivot_table(index=["claim_id", "model", "condition"], columns="form", values="correct", aggfunc="first")
    results = []
    pairs = [("english", "urdu"), ("english", "roman_urdu"), ("urdu", "roman_urdu")]
    for left, right in pairs:
        subset = wide.dropna(subset=[left, right])
        table = np.zeros((2, 2), dtype=int)
        for a, b in zip(subset[left].astype(bool), subset[right].astype(bool)):
            table[int(a), int(b)] += 1
        test = mcnemar(table, exact=True)
        results.append({"comparison": f"{left}_vs_{right}", "n_pairs": len(subset), "discordant": int(table[0, 1] + table[1, 0]), "p_value": float(test.pvalue)})
    if results:
        adjusted = multipletests([item["p_value"] for item in results], method="holm")[1]
        for item, value in zip(results, adjusted):
            item["p_holm"] = float(value)
    return pd.DataFrame(results)


def run_analysis(raw_path: str | Path, output_dir: str | Path, n_bootstrap: int = 2000) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frame = load_outputs(raw_path)
    summarize(frame).to_csv(output_dir / "summary_by_form.csv", index=False)
    consistency = claim_consistency(frame)
    consistency.to_csv(output_dir / "claim_consistency.csv", index=False)
    if {"model", "condition"} <= set(frame.columns):
        paired_mcnemar(frame).to_csv(output_dir / "mcnemar_holm.csv", index=False)
    ci_rows = []
    for form, group in frame.groupby("form"):
        observed, lower, upper = cluster_bootstrap(group, lambda x: float(x["correct"].mean()), n_bootstrap)
        ci_rows.append({"form": form, "accuracy": observed, "ci_lower": lower, "ci_upper": upper, "n": len(group)})
    pd.DataFrame(ci_rows).to_csv(output_dir / "cluster_bootstrap_accuracy.csv", index=False)
    with (output_dir / "analysis_metadata.json").open("w", encoding="utf-8") as handle:
        json.dump({"raw_path": str(raw_path), "n_bootstrap": n_bootstrap, "seed": 42, "rows_analyzed": len(frame)}, handle, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, help="Verified raw JSONL outputs")
    parser.add_argument("--out", required=True, help="Directory for generated analysis tables")
    parser.add_argument("--bootstrap", type=int, default=2000)
    args = parser.parse_args()
    run_analysis(args.raw, args.out, args.bootstrap)


if __name__ == "__main__":
    main()
