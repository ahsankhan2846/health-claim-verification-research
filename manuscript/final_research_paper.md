Same Claim, Different Script: A Multi-Form Benchmark for Health Claim Verification in English, Urdu, and Roman Urdu

Muhammad Ahsan Department of Computer Science


## Abstract

Health questions are often typed in English, Urdu script, or Roman Urdu, yet verification systems are rarely tested on whether the same claim receives the same verdict across these written forms. We present a 70-claim parallel benchmark (210 language-form entries) for health-claim verification in English, Urdu script, and Roman Urdu, covering seven topics with ten claims each. Each claim is linked to an official public-health source (WHO, CDC, NHS, FDA) and labelled Supported, Refuted, or Insufficient. We describe the construction, a translation and evidence-review protocol, a three-condition evaluation design (zero-shot, few-shot, translate-then-verify), and an analysis pipeline using cluster bootstrap intervals, exact McNemar tests with Holm correction, and claim-level cross-form consistency. We also report a design limitation found in our own audit: in the current release, wording and label are confounded, since every Insufficient claim contains an absolute or exact-quantity term, so a lexical rule alone scores 65.7% (46/70). We specify a revised labelling rule and a minimal-pair extension to remove this confound. We report a pilot run of one small open model, Qwen2.5-1.5B-Instruct, zero-shot. Accuracy was 55.7% in English and 32.9% in both Urdu and Roman Urdu; the English-versus-Urdu differences are significant after Holm correction (adjusted p = 0.007). However, the Urdu-form accuracy equals the rate of always answering Refuted (23/70), and the model gave that answer for 59 and 66 of the 70 claims, so the gap reflects near-collapse to one label, not a measured difference between the two scripts. Translate-then-verify could not be evaluated fairly because of a protocol deviation, and few-shot was not run. These results concern one 1.5-billion-parameter model on a benchmark whose translations and labels are still unreviewed. Keywords: multilingual fact verification; Urdu NLP; Roman Urdu; health misinformation; script robustness

1. Introduction

Speakers of Urdu routinely write in two scripts: the Perso-Arabic Urdu script and Roman Urdu, a Latin-script rendering with no standard orthography. Health information seeking in these forms is common, and a verification system that changes its verdict when only the writing form changes could give some users less reliable information than others. We hold the claim content fixed and vary only the form, which isolates representation effects from content differences.

The central question is whether writing form affects model accuracy and claim-level consistency in health claim verification. Our contributions are:

A 70-claim, three-form parallel benchmark with source citations, provisional labels, and explicit review-status fields.

A protocol for translation validation, independent evidence review, and adjudication, with a blinded reviewer sheet.

An evaluation design and open analysis code that analyses each model and condition separately and never pools runs.

An audit of the benchmark itself, including a wording/label confound and a concrete plan to remove it.

2. Related work

Claim verification against evidence was popularised by FEVER (Thorne et al., 2018) and extended to scientific claims in SciFact (Wadden et al., 2020). For public health, PUBHEALTH provides explained claims from fact-checking and health news sources (Kotonya and Toni, 2020), and HealthVer targets COVID-19 claims verified against scientific literature (Sarrouti et al., 2021). These resources are English-only.

Multilingual fact-checking resources include X-Fact, with short claims in 25 languages and expert veracity labels (Gupta and Srikumar, 2021), and a large multilingual dataset for retrieving previously fact-checked claims (Pikuliak et al., 2023). For Urdu specifically, UrduFactBench and UrduFactQA provide hand-annotated benchmarks, and translation-augmented pipelines were reported to outperform monolingual ones (Ahmad et al., 2025). These works vary language, not the script of one fixed claim, and are not specific to health.

Script variation is studied in work on transliteration for low-resource languages written in non-Latin scripts, which finds that the benefit of Latin-script input depends on the task and model size (Ma et al., 2024). Broader cross-lingual evaluation includes XNLI (Conneau et al., 2018), and the uneven coverage of the world's languages in NLP is documented by Joshi et al. (2020).

Within the limits of a preliminary search, we did not find a health-claim benchmark that pairs English, Urdu script, and Roman Urdu versions of the same claim. A systematic literature search is still pending, so we make no strong novelty claim.

3. Benchmark

3.1 Construction

The benchmark has 70 unique claims (HC_001 to HC_070) and three forms per claim, giving 210 entries. An existing 30-claim working file supplied HC_001 to HC_030 (15 Supported, 10 Refuted, 5 Insufficient); HC_031 to HC_070 were added (9, 13, and 18 respectively) with provisional source notes. Seven topics have ten claims each: infectious disease, medication use, vaccines, diabetes and blood pressure, maternal and child health, home remedies, and nutrition. Sources come from WHO (35 claims), CDC (17), NHS (15), FDA (2), and one other site (1). The 70 claims cite 44 distinct URLs, and 8 URLs support two or more claims.

Table 1. Claims by topic and provisional gold label.

Label counts are balanced overall but not within topics: Vaccines has six Insufficient claims and one Supported claim, so topic-level comparisons will be descriptive only.

3.2 Label definitions

Annotators apply the following rule to the claim exactly as written, including scope and qualifiers.

Supported: an authoritative source supports the claim as written, including its hedges.

Refuted: an authoritative source states or directly implies that the claim is false. This includes a universal claim (for example 'guarantees' or 'every') when the source states a limit, such as that vaccines are not fully effective in every person.

Insufficient: the claim is specific or plausible but no authoritative source addresses it, or the evidence is genuinely mixed. A source that merely does not mention the claim does not by itself justify Refuted, and Insufficient does not mean implausible.

The current provisional labels were assigned before this rule was fixed. Some claims may therefore move between Refuted and Insufficient during review; candidates are listed in the accompanying relabel proposal. Gold labels are shared across the three forms by design, so the benchmark tests representation robustness, not independent multilingual annotation quality.

3.3 Wording confound in the current release

In our audit, all 23 Insufficient claims contain an absolute or exact-quantity term (every, all, any, always, never, guarantees, completely, everyone, exactly), compared with 8 of the 47 Supported and Refuted claims (Table 2). A rule that predicts Insufficient when such a term is present and Supported otherwise reaches 46/70 = 65.7% accuracy, against 34.3% for the majority class. This describes the data, not any model. It means that a high Insufficient score could reflect a lexical cue, and the cue is present in all three forms.

Table 2. Absolute or exact-quantity wording by label (English form).

Relabelling alone would flip the confound rather than remove it. We therefore plan two additions before final release: hedged twins for universal claims (for example, 'COVID-19 vaccination reduces the risk of severe illness and death' beside 'prevents all severe illness and death'), and roughly ten plain-worded claims whose evidence is genuinely unsettled. All results will additionally be reported stratified by the presence of absolute wording.

3.4 Other known issues

Near-paraphrases: HC_002, HC_028, HC_035, and HC_054 all state that antibiotics do not act on viruses, and HC_009, HC_016, and HC_050 concern honey and infants. These will be kept as one claim per fact or documented as paraphrase sets.

Source fit: HC_008 asks about common-cold viruses but its source note concerns COVID-19; HC_033 and HC_063 cite a generic healthy-diet page that does not address the claim.

Claim types: the original 'claim_type' field has about 50 inconsistent values; a six-group normalised field is provided and requires review.

4. Translation and review protocol

English is the reference wording. Urdu script and Roman Urdu are parallel renderings of it, not independent claims. An automated screen flags script mixing and numeric mismatches, and it found no script errors; it cannot judge fluency or semantic equivalence. Numerals written as words in Urdu (for example 'twelve months') were not treated as errors.

Every row will be reviewed by two independent reviewers who label the English claim against the cited source and mark Urdu and Roman Urdu equivalence (negation, modality, quantifiers, numbers, units, medical terms). The reviewer sheet does not show the supplied gold label, to avoid anchoring; the key is held separately by the adjudicator. Disagreements go to a health-literate adjudicator, and original and adjudicated decisions are both retained. Cohen's kappa will be reported only for items rated independently, with its denominator. Reviewers state their language and health competence and are not described as native speakers unless that is accurate. No review has been completed at the time of writing, so no agreement statistic is reported.

Roman Urdu has no standard spelling. Variant spellings are recorded for the claims where we have noted them (10 of 70 at present); this field will be completed during review, because spelling variation is both a target phenomenon and a potential confound.

5. Experimental design

5.1 Planned design

Three conditions were planned: zero-shot, few-shot, and translate-then-verify. The prompt asks for exactly one of Supported, Refuted, or Insufficient and requests only the label. Few-shot demonstrations must come from a separate reviewed file whose claim IDs do not overlap the test set; without that file the few-shot condition is disabled. In the planned translate-then-verify condition, non-English claims are translated to English by the same model in a separate, logged step, and the translation is then classified. Decoding is greedy with a fixed seed, and each record stores the model identifier and version, prompt, raw response, parsed label, decoding parameters, and any error. Confidence is not inferred when a model does not provide a calibrated value.

5.2 What was actually run

One model was run: Qwen/Qwen2.5-1.5B-Instruct (resolved revision 989aa7980e4cf806f80c7fef2b1adb7bc71aa306), with greedy decoding (temperature 0, top-p 1), seed 42, and a limit of 32 new tokens. The run took place on 21 November 2026 (13:58 to 15:12 UTC) and produced 420 records: 70 claims x 3 forms x 2 conditions, with no duplicate records, no logged errors, and gold labels and claim text identical to the released benchmark. Few-shot was not run, because no separate demonstration file exists yet.

The run departed from the planned design in three ways that affect interpretation. First, the prompt did not include one-line definitions of the three labels. Second, translate-then-verify was implemented as a single prompt asking the model to translate internally and then classify, so no separate translation was logged. Third, the 32-token limit cut off many of those longer responses before a label appeared. For the English form, translate-then-verify uses the same prompt as zero-shot, and the two conditions gave identical outputs.

The raw JSONL contains 31 missing parsed labels, all in the combined translate-then-verify condition and none in English. Under the released three-label schema, all 31 are invalid outputs and are counted as incorrect. The raw responses and parser fields are preserved for independent re-analysis.

6. Evaluation

Metrics are accuracy, macro-F1 over the three labels, and invalid-output rate, computed separately for each model, condition, and form. Cross-form consistency is the proportion of claims for which all three forms receive the same label, and the proportion for which all three are correct; an invalid output is never counted as consistent.

Uncertainty uses a cluster bootstrap over claim IDs with 2,000 resamples (seed 42), so the three forms of a claim stay together. Paired form comparisons use exact McNemar tests on per-claim correctness, with Holm correction across the three form pairs within each model and condition. Topic and claim-type summaries are descriptive. Two reference points computed from the data are always reported beside model scores: the majority-class rate (34.3%) and the lexical-cue rule (65.7%) from Section 3.3. Results are also stratified by presence of absolute wording.

Intervals describe uncertainty over this sample of claims, not over all health claims or all Urdu speakers.

7. Results

All results are from the single pilot run described in Section 5.2 and describe one 1.5-billion-parameter model. Each cell covers 70 claims. Reference points are the majority-class rate (24/70 = 34.3%), the always-Refuted rate (23/70 = 32.9%), and the lexical-cue rule from Section 3.3 (46/70 = 65.7%).

Table 3. Accuracy, macro-F1, and invalid outputs by condition and form (Qwen2.5-1.5B-Instruct). Intervals are 2,000-resample cluster bootstrap over claims.

Figure 1. Left: accuracy by form with 95% cluster-bootstrap intervals; the English bars are the same in both conditions because the prompt is identical. Right: zero-shot predicted label counts per form against the gold distribution (unlabelled slivers are 2 Supported and 2 Insufficient for Roman Urdu).

7.1 Form differences

In zero-shot, English accuracy (55.7%) exceeded both Urdu (32.9%) and Roman Urdu (32.9%). Exact McNemar tests on per-claim correctness, Holm-corrected across the three form pairs, gave p = 0.0075 for English versus Urdu and for English versus Roman Urdu (26 discordant claims each), and p = 1.0 for Urdu versus Roman Urdu (2 discordant claims). Under translate-then-verify the English-versus-non-English differences were larger (adjusted p = 3.3e-05, 22 discordant claims), and Urdu versus Roman Urdu was again not different (p = 1.0).

7.2 What the model actually answered

The accuracy gap is explained largely by what the model chose to say, not by claim content. In the two non-English forms the model answered Refuted for 59 (Urdu) and 66 (Roman Urdu) of 70 claims. Recall for Supported claims was 0 of 24 in both forms, and recall for Refuted claims was 96% (Urdu) and 100% (Roman Urdu); accuracy of 23/70 is exactly what always answering Refuted would score. English answers were less degenerate (21 Supported, 44 Refuted, 5 Insufficient) but still over-predicted Refuted (gold: 23).

Table 4. Per-label recall in zero-shot, by form.

7.3 Cross-form consistency

In zero-shot, 41 of 70 claims (58.6%) received the same label in all three forms, but only 18 (25.7%) were correct in all three. The apparent agreement comes mostly from the Urdu and Roman Urdu forms both collapsing onto Refuted, so it should not be read as robustness. Under translate-then-verify, 12 of 70 claims (17.1%) were consistent, and all 12 were also correct; invalid outputs are never counted as consistent.

7.4 Absolute wording

Split by the wording flag from Section 3.3, zero-shot English accuracy was 82.1% (32/39) on claims without an absolute term and 22.6% (7/31) on claims with one. In Urdu it was 38.5% (15/39) and 25.8% (8/31), and in Roman Urdu 41.0% (16/39) and 22.6% (7/31). The model never reliably used Insufficient (Table 4), so the wording confound did not inflate its scores; it is also why its English accuracy sits below the 65.7% reached by the lexical-cue rule.

7.5 Translate-then-verify

Translate-then-verify cannot be assessed fairly as a two-stage intervention from this run. Of 140 non-English responses, 31 had no parsable label, often because the response was cut at 32 tokens before a label. Of the 109 valid answers, the Roman Urdu form received Supported for 51 of 53 and the Urdu form for 47 of 56, a strong shift toward Supported. Differences against zero-shot were not significant per form (exact McNemar: Urdu 21 versus 17 discordant claims, p = 0.627; Roman Urdu 22 versus 17, p = 0.522). Reading the raw responses (not a systematic coding), the internal translations were often wrong: for example, Roman Urdu HC_002 ('Antibiotics cure the common cold') was rendered 'Antibiotics can be used to treat cancer', and the Urdu text of HC_004 (mRNA vaccines change DNA) was rendered 'Code 19 converts human DNA to RNA'. Both were then labelled Supported.

8. Discussion

The pilot shows that this small model is close to chance on the two Urdu forms and does better in English, and that the English advantage survives correction for the three form comparisons. It does not show that Urdu script and Roman Urdu differ from each other, and it does not show a script effect that would carry over to larger or multilingual-trained models. Several features of the data limit what can be concluded.

The Urdu-form accuracy is indistinguishable from the always-Refuted rate and its intervals include that value, so the model may not be reading the claims at all. Differences in accuracy between forms are then driven by the answering default.

Even in English, the model scored 55.7% against 65.7% for a rule that only checks for absolute wording, and it never identified Insufficient claims. The benchmark is therefore hard for this model in a way that has little to do with script.

The translate-then-verify result is dominated by a protocol deviation (single prompt, 32-token limit, no logged translation), and the visibly wrong in-response translations suggest a further reason to expect that condition to hurt a model of this size. A fair test needs a separate, logged translation step with enough tokens.

The gold labels and translations are unreviewed. If an Urdu or Roman Urdu rendering is wrong, some of the Urdu-form errors may be the benchmark's, not the model's.

The most informative next steps are to repeat the run with larger and multilingual-trained models, to fix the prompt (label definitions, adequate token limit, logged translation), to add the hedged-twin claims so wording no longer predicts the label, and to complete the human review before any of these numbers are cited as findings.

9. Limitations and ethics

The benchmark is small and constructed; it is not a prevalence sample of health misinformation.

The empirical results come from one 1.5-billion-parameter model in a single run, with the protocol deviations in Section 5.2 and no few-shot condition. They should not be generalised to other models.

Labels are provisional, were assigned under a looser rule than the one in Section 3.2, and are confounded with wording (Section 3.3).

Translations are unreviewed by qualified Urdu and Roman Urdu reviewers. Dialect and Roman Urdu spelling variation are not yet characterised.

Source URLs have not yet been re-checked and dated; several claims share a source page, and some sources are only tangentially related.

Results depend on checkpoint version, prompt wording, decoding settings, and the token limit; the 32-token limit demonstrably affected the translate-then-verify condition.

The benchmark is for research evaluation. It is not medical advice and must not be used as a clinical decision system. Claims and labels may be out of date as guidance changes.


## 10. Conclusion

We release a three-form parallel health-claim benchmark, an evaluation pipeline, and a pilot run of one small model. The pilot found a significant English advantage over Urdu script and Roman Urdu, but that advantage coincides with the model defaulting to Refuted in the Urdu forms, and the translate-then-verify condition was compromised by a protocol deviation. We also document the benchmark's own weaknesses: unreviewed translations, provisional labels, and a wording/label confound. Whether script affects verification in stronger models remains an open question that needs corrected runs, additional models, and completed human review.

Data and code availability

The benchmark (CSV and JSONL), audit workbooks, reviewer materials, notebook, and analysis code accompany this paper. The raw model outputs (420 records) and the generated analysis tables are included. Repository: https://github.com/ahsankhan2846/health-claim-verification-research. Code is released under the MIT License; benchmark reuse must preserve the provisional-review fields and source notes.

AI assistance statement

An AI assistant helped inspect files, draft code, documentation, and parts of this manuscript. The author must verify all data, sources, translations, and claims and edit this statement to match the venue's policy.


## References

Ahmad, S., Iqbal, H., Ahsan, M., Naeem, N., Khan, M. A. R., Riaz, A., Manzoor, M. A., Wang, Y., and Nakov, P. (2025). UrduFactCheck: An agentic fact-checking framework for Urdu with evidence boosting and benchmarking. arXiv:2505.15063.

Conneau, A., Rinott, R., Lample, G., Williams, A., Bowman, S., Schwenk, H., and Stoyanov, V. (2018). XNLI: Evaluating cross-lingual sentence representations. EMNLP.

Gupta, A. and Srikumar, V. (2021). X-Fact: A new benchmark dataset for multilingual fact checking. ACL-IJCNLP (Short Papers), pp. 675-682.

Joshi, P., Santy, S., Budhiraja, A., Bali, K., and Choudhury, M. (2020). The state and fate of linguistic diversity and inclusion in the NLP world. ACL.

Kotonya, N. and Toni, F. (2020). Explainable automated fact-checking for public health claims. EMNLP.

Ma, C., Liu, Y., Ye, H., and Schütze, H. (2024). Exploring the role of transliteration in in-context learning for low-resource languages written in non-Latin scripts. arXiv:2407.02320.

Pikuliak, M., Srba, I., Moro, R., Hromadka, T., Smoleň, T., Melišek, M., Vykopal, I., Simko, J., Podroužek, J., and Bielikova, M. (2023). Multilingual previously fact-checked claim retrieval. EMNLP, pp. 16477-16500.

Sarrouti, M., Ben Abacha, A., Mrabet, Y., and Demner-Fushman, D. (2021). Evidence-based fact-checking of health-related claims. Findings of EMNLP.

Thorne, J., Vlachos, A., Christodoulopoulos, C., and Mittal, A. (2018). FEVER: a large-scale dataset for fact extraction and VERification. NAACL-HLT.

Wadden, D., Lin, S., Lo, K., Wang, L. L., van Zuylen, M., Cohan, A., and Hajishirzi, H. (2020). Fact or fiction: Verifying scientific claims. EMNLP.


### Table 1

| Topic | Supported | Refuted | Insufficient | Total |
| --- | --- | --- | --- | --- |
| Infectious disease | 4 | 4 | 2 | 10 |
| Medication use | 2 | 5 | 3 | 10 |
| Vaccines | 1 | 3 | 6 | 10 |
| Diabetes / blood pressure | 6 | 2 | 2 | 10 |
| Maternal / child health | 5 | 3 | 2 | 10 |
| Home remedies | 3 | 4 | 3 | 10 |
| Nutrition | 3 | 2 | 5 | 10 |
| Total | 24 | 23 | 23 | 70 |

### Table 2

| Gold label | No absolute term | Absolute term | Total |
| --- | --- | --- | --- |
| Supported | 23 | 1 | 24 |
| Refuted | 16 | 7 | 23 |
| Insufficient | 0 | 23 | 23 |

### Table 3

| Condition | Form | Correct | Accuracy (95% CI) | Macro-F1 | Invalid |
| --- | --- | --- | --- | --- | --- |
| Zero-shot | English | 39 | 55.7% (42.9-67.1) | 0.490 | 0 |
| Zero-shot | Urdu | 23 | 32.9% (22.9-44.3) | 0.198 | 0 |
| Zero-shot | Roman Urdu | 23 | 32.9% (22.9-44.3) | 0.172 | 0 |
| Translate-then-verify | English | 39 | 55.7% (42.9-67.1) | 0.490 | 0 |
| Translate-then-verify | Urdu | 19 | 27.1% (17.1-37.1) | 0.230 | 14 |
| Translate-then-verify | Roman Urdu | 18 | 25.7% (15.7-35.7) | 0.200 | 17 |

### Table 4

| Form (zero-shot) | Recall: Supported | Recall: Refuted | Recall: Insufficient |
| --- | --- | --- | --- |
| English | 88% (21/24) | 78% (18/23) | 0% (0/23) |
| Urdu | 0% (0/24) | 96% (22/23) | 4% (1/23) |
| Roman Urdu | 0% (0/24) | 100% (23/23) | 0% (0/23) |
