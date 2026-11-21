# Label/wording confound: findings and proposal

**Status: proposal only. No gold label in `data/` has been changed.** Every item below needs the two-reviewer source check before any label moves.

## The problem
All 23 Insufficient claims contain an absolute or exact-quantity word (every, all, guarantees, never, completely, exactly). Only 8 of the other 47 do. A model can score well on Insufficient by keying on those words, so the benchmark would partly measure lexical cues, not health-claim verification, and the cue is the same in all three scripts.

The rule for "Insufficient" vs "Refuted" is also applied inconsistently:

| Pattern | Labelled Insufficient | Labelled Refuted |
|---|---|---|
| Universal protection claim | HC_034 mask prevents every infection; HC_038 flu vaccine prevents every infection; HC_042 vaccine, never infected | HC_068 essential oils kill every virus; HC_045 detox removes all toxins |
| Universal safety claim | (none) | HC_050 honey safe for every infant; HC_047 raw milk safer for everyone |

## Proposed rule (to adopt in `annotation_guidelines.docx`)
- **Refuted**: an authoritative source states or directly implies the claim is false. This includes a universal claim ("guarantees", "every", "never") where the source states a limit, e.g. vaccines are not 100% effective, or scans cannot detect everything.
- **Insufficient**: the claim is specific or plausible, but no authoritative source addresses it or the evidence is genuinely mixed. A source that only fails to mention the claim is not enough on its own to call it Refuted.
- **Supported**: the source supports the claim as written, including its hedges.

## Candidate relabels (see `relabel_candidates.csv`)
**Insufficient → Refuted (likely under the rule above):** HC_034, 036, 038, 039, 040, 042, 043, 051, 052, 066, 061.
**Keep Insufficient (specific or unverifiable quantity or formula):** HC_020, 025, 029, 030, 057, 069, 046, 048, 060, 063, 033. HC_026 is borderline.
**Refuted → check whether Insufficient fits better** (the source note says the guidance "does not support", not "contradicts"): HC_056, HC_068.
**Source mismatch:** HC_008 claims "kills the viruses that cause the common cold" but the cited note is about COVID-19. HC_033 (garlic) and HC_063 (lemon water) cite the generic WHO healthy-diet page rather than a source about the claim.

## Why relabelling alone is not enough
Moving the universal-protection claims to Refuted would flip the confound: absolute wording would predict Refuted instead of Insufficient. Balance must come from new items.

**Minimal pairs.** For each universal claim, add a hedged twin that is Supported, so wording no longer predicts the label:
| Existing (absolute) | Proposed hedged twin (Supported, source to verify) |
|---|---|
| HC_043 COVID-19 vaccination prevents all severe illness and death | COVID-19 vaccination reduces the risk of severe illness and death from COVID-19 |
| HC_038 flu vaccine prevents every infection | Seasonal flu vaccination can reduce the risk of flu illness |
| HC_034 mask prevents every respiratory infection | A well-fitting mask can reduce the risk of respiratory infection |
| HC_051 breastfeeding prevents every infection | Breastfeeding provides immune benefits to infants |
| HC_052 ultrasound guarantees a healthy baby | A pregnancy ultrasound can detect some fetal abnormalities |

**Non-absolute Insufficient claims.** Add roughly 10 claims with plain wording and genuinely unsettled evidence, for example a hedged "may help" claim about a supplement where authoritative sources say evidence is limited. Pick them from Cochrane, WHO or NHS pages that say so explicitly, and record the sentence that does.

**Near-duplicates.** Keep one of HC_002 / 035 / 054 / 028 (antibiotics and viruses) and one of HC_009 / 016 / 050 (honey), or label them as intentional paraphrase sets so they are not counted as independent claims.

Target after revision: wording features (absolute word present or absent) approximately balanced within each label.
