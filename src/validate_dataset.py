"""Validate the benchmark schema and invariants."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED = {
    "claim_id",
    "topic",
    "claim_type",
    "english",
    "urdu",
    "roman_urdu",
    "gold_label",
    "source_title",
    "source_url",
    "source_note",
    "review_status",
}
LABEL_COUNTS = {"Supported": 24, "Refuted": 23, "Insufficient": 23}
TOPICS = {
    "Infectious disease",
    "Vaccines",
    "Nutrition",
    "Maternal/child health",
    "Diabetes/blood pressure",
    "Medication use",
    "Home remedies",
}


def validate(path: str | Path) -> None:
    frame = pd.read_csv(path)
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    expected_ids = {f"HC_{index:03d}" for index in range(1, 71)}
    if len(frame) != 70 or set(frame["claim_id"]) != expected_ids:
        raise ValueError("Expected exactly HC_001 through HC_070")
    if frame["claim_id"].duplicated().any():
        raise ValueError("Duplicate claim_id")
    if frame["gold_label"].value_counts().to_dict() != LABEL_COUNTS:
        raise ValueError(f"Unexpected label counts: {frame['gold_label'].value_counts().to_dict()}")
    if set(frame["topic"]) != TOPICS:
        raise ValueError("Unexpected topic set")
    required_nonblank = REQUIRED - {"spelling_variants"}
    if frame[list(required_nonblank)].isna().any().any():
        raise ValueError("Missing required values present")
    if not all(frame[column].astype(str).str.strip().ne("").all() for column in required_nonblank):
        raise ValueError("Blank values present")
    print(f"Validated {len(frame)} claims from {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    validate(parser.parse_args().dataset)
