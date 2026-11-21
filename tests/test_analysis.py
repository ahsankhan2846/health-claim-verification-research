import json

from src.analysis import load_raw, summarize


def test_raw_results_have_unique_evaluation_keys(tmp_path):
    rows = [
        {
            "claim_id": "HC_001",
            "form": "english",
            "gold_label": "Supported",
            "predicted_label": "Supported",
            "prompting_condition": "zero_shot",
        },
        {
            "claim_id": "HC_001",
            "form": "urdu",
            "gold_label": "Supported",
            "predicted_label": None,
            "prompting_condition": "zero_shot",
        },
    ]
    path = tmp_path / "raw.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    frame = load_raw(path)
    summary = summarize(frame)
    urdu = summary.loc[summary["form"].eq("urdu")].iloc[0]
    assert urdu["n_all"] == 1
    assert urdu["n_valid"] == 0
    assert urdu["accuracy_all"] == 0
    assert urdu["invalid_n"] == 1


def test_normalized_and_valid_denominators_are_distinct(tmp_path):
    rows = [
        {
            "claim_id": "HC_001",
            "form": "urdu",
            "gold_label": "Supported",
            "predicted_label": "Supported",
            "prompting_condition": "translate_then_verify",
        },
        {
            "claim_id": "HC_002",
            "form": "urdu",
            "gold_label": "Refuted",
            "predicted_label": None,
            "prompting_condition": "translate_then_verify",
        },
    ]
    path = tmp_path / "raw.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    summary = summarize(load_raw(path)).iloc[0]
    assert summary["correct_all"] == 1
    assert summary["n_all"] == 2
    assert summary["n_valid"] == 1
    assert summary["correct_valid"] == 1
    assert summary["accuracy_all"] == 0.5
    assert summary["accuracy_valid"] == 1.0
