# Literature review and research positioning

## Verified anchors

- Thorne et al. (2018), **FEVER**, introduced a large claim/evidence verification benchmark with SUPPORTS, REFUTES, and NOT ENOUGH INFO-style reasoning.
- Wadden et al. (2020), **SciFact**, evaluates scientific claims against evidence from scientific abstracts.
- Kotonya and Toni (2020), **PUBHEALTH**, studies explainable public-health claim verification.
- Sarrouti et al. (2021), **HEALTHVER**, constructs health-related claims paired with scientific evidence and SUPPORT/REFUTE/NEUTRAL relations. ACL Anthology: https://aclanthology.org/2021.findings-emnlp.297/
- Gupta and Srikumar (2021), **X-Fact**, provides multilingual fact-checking data but does not isolate script variation for the same claim.
- Ahmad et al. (2025), **UrduFactCheck**, introduces UrduFactBench and UrduFactQA and evaluates Urdu factuality and claim verification. ACL Anthology: https://aclanthology.org/2025.findings-emnlp.1240/
- Shcharbakova et al. (2025), **When Scale Meets Diversity**, evaluates multilingual claim verification on X-Fact and shows that model scale alone is not a reliable proxy for verification quality. ACL Anthology: https://aclanthology.org/2025.fever-1.5/
- A 2026 AbjadNLP paper, **Code-Switching as a Safety Failure Mode in Large Language Models**, reports degradation on Roman Urdu and related transliterated inputs. ACL Anthology: https://aclanthology.org/2026.abjadnlp-1.37/

## Positioning

The contribution should not be framed as the first Urdu fact-checking benchmark: UrduFactBench now exists. The defensible contribution is narrower: a controlled, claim-aligned comparison in which English, Urdu script, and Roman Urdu versions are intended to express the same health claim. The study is a script/form robustness benchmark, not a replacement for UrduFactBench or a general health misinformation corpus.

## Claims to avoid

- “First Urdu fact-checking benchmark.”
- “Models are unsafe for health use.”
- “Roman Urdu causes errors.”
- “Translation solves multilingual verification.”

The current data support only descriptive pilot observations for one Qwen checkpoint and two conditions, with unresolved translation and label validation.
