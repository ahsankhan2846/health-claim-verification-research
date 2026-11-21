"""Metrics and statistical analysis for verified raw predictions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.metrics import accuracy_score, classification_report, f1_score
from statsmodels.stats.multitest import multipletests

LABELS = ["Supported", "Refuted", "Insufficient"]
FORMS = ["english", "urdu", "roman_urdu"]


def normalize_label(value: object) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).strip().lower().split())
    matches = [
        label for label in LABELS
        if label.lower() in text and len(text) <= 80
    ]
    return matches[0] if len(matches) == 1 else None


def load_raw(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    frame = pd.DataFrame(rows)
    required = {"claim_id", "form", "gold_label", "predicted_label"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing raw-output columns: {sorted(missing)}")
    frame["predicted_label_normalized"] = frame["predicted_label"].map(normalize_label)
    frame["invalid_output"] = frame["predicted_label_normalized"].isna()
    frame["correct_all_examples"] = (
        frame["predicted_label_normalized"] == frame["gold_label"]
    )
    if frame.duplicated(["prompting_condition", "claim_id", "form"]).any():
        raise ValueError("Duplicate condition/claim/form rows detected")
    return frame


def summarize(frame: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for keys, group in frame.groupby(["prompting_condition", "form"], dropna=False):
        condition, form = keys
        valid = group.loc[~group["invalid_output"]]
        records.append({
            "condition": condition,
            "form": form,
            "n_all": len(group),
            "correct_all": int(group["correct_all_examples"].sum()),
            "accuracy_all": float(group["correct_all_examples"].mean()),
            "n_valid": len(valid),
            "correct_valid": int(valid["correct_all_examples"].sum()),
            "accuracy_valid": (
                float(valid["correct_all_examples"].mean()) if len(valid) else None
            ),
            "macro_f1_valid": (
                f1_score(
                    valid["gold_label"],
                    valid["predicted_label_normalized"],
                    labels=LABELS,
                    average="macro",
                    zero_division=0,
                ) if len(valid) else None
            ),
            "invalid_n": int(group["invalid_output"].sum()),
            "invalid_rate": float(group["invalid_output"].mean()),
        })
    return pd.DataFrame(records)


def consistency(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (condition, claim_id), group in frame.groupby(
        ["prompting_condition", "claim_id"], dropna=False
    ):
        by_form = group.set_index("form")
        predictions = by_form["predicted_label_normalized"]
        rows.append({
            "condition": condition,
            "claim_id": claim_id,
            "all_three_same": (
                predictions.notna().all() and predictions.nunique() == 1
            ),
            "all_three_correct": (
                len(by_form) == 3 and by_form["correct_all_examples"].all()
            ),
            "valid_forms": int(predictions.notna().sum()),
        })
    return pd.DataFrame(rows)


def cluster_bootstrap(
    frame: pd.DataFrame,
    statistic: Callable[[pd.DataFrame], float],
    resamples: int = 2000,
    seed: int = 42,
) -> tuple[float, float, float]:
    claims = frame["claim_id"].drop_duplicates().to_numpy()
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(resamples):
        chosen = rng.choice(claims, len(claims), replace=True)
        boot = pd.concat(
            [frame.loc[frame["claim_id"].eq(claim)] for claim in chosen],
            ignore_index=True,
        )
        values.append(statistic(boot))
    return (
        statistic(frame),
        float(np.quantile(values, 0.025)),
        float(np.quantile(values, 0.975)),
    )


def paired_tests(frame: pd.DataFrame) -> pd.DataFrame:
    records = []
    for condition, group in frame.groupby("prompting_condition"):
        wide = group.pivot(index="claim_id", columns="form", values="correct_all_examples")
        p_values = []
        local = []
        for left, right in (
            ("english", "urdu"),
            ("english", "roman_urdu"),
            ("urdu", "roman_urdu"),
        ):
            pair = wide[[left, right]].dropna()
            left_only = int((pair[left] & ~pair[right]).sum())
            right_only = int((~pair[left] & pair[right]).sum())
            discordant = left_only + right_only
            p_value = (
                binomtest(min(left_only, right_only), discordant, 0.5).pvalue
                if discordant else 1.0
            )
            local.append({
                "condition": condition,
                "left_form": left,
                "right_form": right,
                "left_correct_right_wrong": left_only,
                "left_wrong_right_correct": right_only,
                "discordant_pairs": discordant,
                "p_exact": p_value,
            })
            p_values.append(p_value)
        adjusted = multipletests(p_values, method="holm")[1]
        for record, value in zip(local, adjusted):
            record["p_holm"] = float(value)
            records.append(record)
    return pd.DataFrame(records)


def run(raw_path: str | Path, output_dir: str | Path, bootstrap_resamples: int = 2000) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    frame = load_raw(raw_path)
    summarize(frame).to_csv(output / "summary_corrected.csv", index=False)
    consistency(frame).to_csv(output / "claim_consistency_corrected.csv", index=False)
    paired_tests(frame).to_csv(output / "mcnemar_holm_corrected.csv", index=False)
    ci_rows = []
    for (condition, form), group in frame.groupby(
        ["prompting_condition", "form"], dropna=False
    ):
        observed, lower, upper = cluster_bootstrap(
            group, lambda item: float(item["correct_all_examples"].mean()),
            bootstrap_resamples,
        )
        ci_rows.append({
            "condition": condition,
            "form": form,
            "accuracy_all": observed,
            "ci_low": lower,
            "ci_high": upper,
            "n_all": len(group),
        })
    pd.DataFrame(ci_rows).to_csv(output / "cluster_bootstrap_corrected.csv", index=False)
    (output / "analysis_metadata.json").write_text(json.dumps({
        "bootstrap_resamples": bootstrap_resamples,
        "seed": 42,
        "rows": len(frame),
        "invalid_outputs": int(frame["invalid_output"].sum()),
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--bootstrap", type=int, default=2000)
    args = parser.parse_args()
    run(args.raw, args.out, args.bootstrap)
