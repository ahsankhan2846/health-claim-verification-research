import json
from pathlib import Path

import pandas as pd


def test_raw_pilot_counts_match_published_analysis():
    rows = [
        json.loads(line)
        for line in Path("results/raw_outputs.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    frame = pd.DataFrame(rows)
    assert len(frame) == 420
    assert frame["run_id"].nunique() == 420
    assert frame["error"].isna().all()
    assert frame["predicted_label"].isna().sum() == 31

    expected = {
        ("zero_shot", "english"): (39, 0),
        ("zero_shot", "urdu"): (23, 0),
        ("zero_shot", "roman_urdu"): (23, 0),
        ("translate_then_verify", "english"): (39, 0),
        ("translate_then_verify", "urdu"): (19, 14),
        ("translate_then_verify", "roman_urdu"): (18, 17),
    }
    for key, (correct, invalid) in expected.items():
        condition, form = key
        group = frame[
            frame["prompting_condition"].eq(condition) & frame["form"].eq(form)
        ]
        assert int(group["predicted_label"].eq(group["gold_label"]).sum()) == correct
        assert int(group["predicted_label"].isna().sum()) == invalid
