# Submission-readiness gate

## Overall status: **Not yet ready for empirical submission**

The package is locally complete and reproducible as a research scaffold, but two external gates remain mandatory:

1. **Human validation:** qualified Urdu/Roman Urdu reviewers and independent evidence/label reviewers must complete and sign the supplied sheets.
2. **Remaining experiment execution:** few-shot evaluation and preferably additional models are not yet complete.

## Gate results

| Gate | Status | Evidence |
|---|---|---|
| 70 unique claims | Completed | HC_001–HC_070 |
| 210 language-form entries | Completed | Three forms per claim |
| Label balance | Completed | 24 / 23 / 23 |
| Seven-topic balance | Completed | Ten claims per topic |
| Schema and local integrity | Completed | Automated local checks passed |
| Translation equivalence | Requires human validation | Automated checks are screening only |
| Source URL availability | Requires external verification | DNS/network unavailable in this environment |
| Source-label correctness | Requires human validation | Audit workbook prepared |
| Annotation agreement | Requires human validation | No annotators or kappa fabricated |
| Few-shot leakage control | Completed in notebook | Separate demonstration file required |
| Model execution | Completed, pilot only | Qwen 2.5 1.5B zero-shot and translate-then-verify: 420 genuine outputs |
| Statistical results | Completed, pilot only | Accuracy, macro-F1, cluster bootstrap, consistency, McNemar, and Holm tables generated |
| Manuscript evidence claims | Partially completed | Pilot Results are evidence-bounded; human validation and few-shot remain pending |

## Required final author actions

Complete the two external gates, run the analysis from raw outputs, insert only verified tables/figures into the manuscript, and rerun this checklist. The ZIP `submission_package.zip` is a handoff package, not evidence that the study is empirically submission-ready.
