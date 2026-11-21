# Limitations and pending work

## Requires human validation

- Urdu and Roman Urdu translations have not been reviewed by qualified human language reviewers.
- Source URLs and evidence-label alignment have not been independently checked claim by claim.
- Gold labels remain provisional.
- The prior audit contains entries that do not match the current 30-row CSV; those discrepancies are recorded rather than silently treated as corrections.
- The manuscript bibliography and novelty claim require final bibliographic and literature-search verification.

## Pilot experiment completed

- Genuine zero-shot and translate-then-verify outputs exist for Qwen 2.5 1.5B-Instruct, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`.
- Raw outputs contain 420 rows, 420 unique run IDs, and no execution errors.
- A separate, non-test few-shot demonstration file has not been supplied, so few-shot was not executed.
- No calibrated confidence values were collected.

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
