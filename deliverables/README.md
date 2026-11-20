# Same Claim, Different Script

This package contains a 70-claim benchmark for health-claim verification in English, Urdu script, and Roman Urdu.

## Status

The benchmark and analysis scaffold are complete as files, but qualified Urdu/Roman Urdu review, independent evidence/label review, adjudication, URL verification, and model inference remain pending. No model predictions or statistical findings are included.

The benchmark has 70 unique claims, 210 language-form entries, seven topics with ten claims each, and labels of Supported=24, Refuted=23, Insufficient=23. The original 30-row working file was preserved as the source for HC_001–HC_030; HC_031–HC_070 were added with provisional source notes.

## Files

- `data/final_benchmark_70.csv` and `.jsonl`: benchmark data.
- `audit/translation_validation_report.xlsx`: automated screening plus pending human review.
- `audit/source_label_audit.xlsx`: source and label audit scaffold.
- `deliverables/final_research_paper.docx`: revised manuscript.
- `deliverables/annotation_guidelines.docx`: annotation protocol.
- `deliverables/annotator_review_sheet.xlsx`: reviewer-ready sheet.
- `analysis.py`: analysis functions for verified raw JSONL outputs.
- `code/run_models_colab.ipynb`: guarded Colab notebook.
- `deliverables/data_dictionary.md`: column definitions.
- `limitations_and_pending_work.md`: submission blockers.

## Run locally

```bash
python -m venv .venv
.venv/bin/pip install pandas numpy scipy scikit-learn statsmodels matplotlib seaborn transformers accelerate sentencepiece
.venv/bin/python analysis.py --raw results/raw_outputs.jsonl --out results/analysis --bootstrap 2000
```

Raw JSONL must contain `claim_id`, `form`, `gold_label`, and `predicted_label` (or `raw_response`). Retain model ID/version, prompt, condition, decoding parameters, timestamp, and errors. Invalid outputs are counted as errors.

## Evaluation protocol

English, Urdu, and Roman Urdu are paired by `claim_id`. Few-shot demonstrations must come from a separate reviewed file and must not share IDs with the 70-claim test benchmark. Translate-then-verify must log the translation prompt and raw output. Confidence is not inferred when a model does not provide a calibrated value.

## Human review

Two independent reviewers should complete the reviewer sheet. They must check semantic equivalence, source-label alignment, qualifiers, numbers, and script integrity. Disagreements require documented adjudication. Only after this review should provisional labels and translations be treated as final.
