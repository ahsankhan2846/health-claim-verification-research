# Quality-control report

| Item | Status | Evidence |
|---|---|---|
| Dataset completeness | Completed | 70 unique IDs, 210 language-form fields, HC_001–HC_070 |
| Exact label counts | Completed | Supported 24, Refuted 23, Insufficient 23 |
| Topic distribution | Completed | Seven topics, ten claims per topic |
| Translation validation | Requires human validation | Automated screening report generated; no native-speaker review claimed |
| Source verification | Partially completed | Source/title/note fields present; outbound URL checks blocked in this environment |
| Annotation status | Requires human validation | Reviewer sheet and protocol generated; no annotations or agreement scores claimed |
| Data leakage status | Completed in code/protocol | Few-shot cell rejects missing separate demonstrations and checks ID overlap |
| Notebook execution | Requires experiment execution | Notebook syntax generated and guarded; no model was run |
| Statistical analysis | Partially completed | `analysis.py` implements metrics, 2,000-cluster bootstrap, McNemar, and Holm correction; no results exist |
| Manuscript status | Partially completed | Revised DOCX separates methods from pending empirical results |
| Remaining limitations | Requires human validation / experiment execution | See `limitations_and_pending_work.md` |

## Existing-material audit findings

- The working CSV actually contains 30 rows with 15 Supported, 10 Refuted, and 5 Insufficient claims.
- The supplied audit CSV contains 11 flags, but several do not match the current working CSV wording; the final audit preserves those flags as historical discrepancies.
- The original notebook references missing `run_eval.py`, `verify_benchmark.py`, `check_raw_integrity.py`, `repro_check.py`, and `benchmark_v0_70.jsonl` files. The corrected notebook no longer assumes those absent paths.
- The manuscript PDF describes a 70-claim pilot and completed review/results despite the supplied files containing no 70-claim benchmark or model outputs. The revised manuscript removes unsupported empirical claims and marks results pending.
