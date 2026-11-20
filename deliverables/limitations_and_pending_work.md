# Limitations and pending work

## Requires human validation

- Urdu and Roman Urdu translations have not been reviewed by qualified human language reviewers.
- Source URLs and evidence-label alignment have not been independently checked claim by claim.
- Gold labels remain provisional.
- The prior audit contains entries that do not match the current 30-row CSV; those discrepancies are recorded rather than silently treated as corrections.
- The manuscript bibliography and novelty claim require final bibliographic and literature-search verification.

## Requires experiment execution

- No model inference has been run in this handoff.
- No raw model responses, confidence values, execution logs, accuracy, macro-F1, confidence intervals, McNemar tests, or cross-form consistency results exist.
- The notebook requires a model checkpoint, compatible hardware, package installation, and any required credentials.
- A separate, non-test few-shot demonstration file must be supplied before enabling few-shot evaluation.

## Methodological limitations

- Seventy claims are a constructed benchmark, not a population sample.
- The three forms share a gold label by design; this tests representation robustness, not independent multilingual annotation quality.
- Roman Urdu has no single standardized orthography, so spelling variation is both a target phenomenon and a potential confound.
- Insufficient means the cited evidence does not establish the exact claim; it is not simply a synonym for implausible.
- Cluster bootstrap intervals describe uncertainty over sampled claims, not all health claims or all Urdu speakers.

## Personal steps required before submission

1. Arrange qualified Urdu and Roman Urdu review for every row.
2. Have two independent reviewers verify every source, label, qualifier, and translation; adjudicate disagreements.
3. Check every source URL and record the access date.
4. Create a separate reviewed few-shot demonstration set, or report zero-shot-only results.
5. Run configured models and retain raw JSONL, prompts, versions, timestamps, and logs.
6. Run `analysis.py` and write Results and Discussion only from those outputs.
7. Complete the literature search, bibliography verification, ethics statement, AI-assistance statement, and venue formatting.
8. Perform a final author review for medical wording and confirm the benchmark is not presented as medical advice.
