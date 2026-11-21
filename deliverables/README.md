# Deliverables

This directory contains the benchmark and manuscript artifacts. The empirical pilot is genuine but limited to one Qwen checkpoint and two conditions.

`final_research_paper.docx` and `final_research_paper.pdf` are generated from the corrected manuscript source in `../manuscript/final_research_paper.md`.

## Important distinction

The preserved raw condition named `translate_then_verify` used a combined prompt. It did not save a separate translation stage. Use `run_models_colab_corrected.ipynb` or `src/evaluate.py` for the true two-stage condition.

## Human review

`annotator_review_sheet.xlsx` is for independent reviewers and does not contain gold labels. `adjudicator_key_DO_NOT_SHARE_WITH_REVIEWERS.xlsx` is restricted to adjudication and must not be sent to independent reviewers.

The benchmark, source labels, and translations remain provisional until independent review and adjudication.
