# Changes in this revision
- `analysis.py` / `code/analysis.py`: reads the notebook schema; all metrics per (model, condition, form); McNemar + Holm now run; cluster bootstrap vectorised; consistency treats invalid outputs as inconsistent; tolerant label parser (`Supported.`, `Label: Refuted`); errors on duplicate rows from appended re-runs.
- Notebook: shared label parser; chat template used when available; translate-then-verify is a two-step, logged translation (translation prompt and raw output are saved); one `run_id` per run; clearer instruction with label definitions.
- Reviewer sheet: gold label removed so reviewers label independently. The key is in `adjudicator_key_DO_NOT_SHARE_WITH_REVIEWERS.xlsx` for the adjudicator only.
- Data: added `claim_type_normalized` (heuristic, 6 groups; review it). **Gold labels unchanged.**
- Folder layout now matches the README (`data/`, `audit/`, `code/`, `deliverables/`).
- Paper: "preregistered" changed to "pre-specified (not formally preregistered)".
- New: `label_confound_and_relabel_proposal.md`, `relabel_candidates.csv`.
- Not done: relabelling, new claims, URL checks, translation review, any model runs, a data dictionary file (still missing).
