# Model Card — Pain Mechanism Classifier

**Author:** Renato Murayama (Physiotherapist · MSc Medical Informatics student, University of Minho)
**Version:** 1.0 — November 2026
**Status:** Educational portfolio project. **Not a medical device. Not validated on real patients. Not for clinical use.**

---

## 1. Model details

| Item | Description |
|---|---|
| Task | Multiclass classification of the **predominant musculoskeletal pain mechanism** |
| Classes | Nociceptive · Neuropathic · Nociplastic · Mixed (IASP mechanistic descriptors + mixed pain) |
| Algorithm | Multinomial logistic regression (scikit-learn), `class_weight="balanced"` |
| Preprocessing | Median imputation + standardisation (numeric); one-hot encoding (categorical); fitted on training data only |
| Comparator | Random forest (300 trees) — similar performance; logistic regression chosen for simplicity and interpretability |
| Safety gate | Rule-based red-flag screening **before** the model (not machine learning) |

## 2. Intended use (IMDRF-style definition statement)

- **Medical purpose:** to **inform clinical management** by suggesting the predominant pain mechanism and showing guideline-based educational content for that mechanism. The tool does not diagnose, treat or replace clinical judgement.
- **Healthcare situation:** musculoskeletal pain, **without red flags**. Classification is suspended when any red flag is present.
- **Intended population:** adults with musculoskeletal pain assessed in primary care, physiotherapy or exercise settings.
- **Intended users:** health and movement professionals (physicians, physiotherapists, nurses, exercise physiologists, physical educators and personal trainers, manual therapists such as massage therapists). Users without diagnostic competence use the output for education and referral only.
- **Hypothetical risk category:** IMDRF Category II (informs clinical management in a non-critical situation). Under EU MDR Rule 11, comparable software would likely be Class IIa and, under the EU AI Act, a high-risk AI system.

**Out of scope:** patients with red flags; children; use by patients themselves; use as the sole basis for diagnosis, treatment, medication or imaging decisions.

## 3. Data

- **Synthetic dataset** of 2,000 patients generated in Python from published clinical criteria (IASP; Kosek et al., 2021; Finnerup et al., 2016; Smart et al., 2012; Shraim et al., 2022). See `docs/pain_mechanism_criteria.md`.
- **Variables (13 model inputs):** pain duration, pain distribution, DN4, painDETECT, CSI, sleep quality, imaging (concordant tissue finding, concordant nerve compression), HADS anxiety, HADS depression, PCS, TSK, work stress.
- **Class prevalence (scenario A, evidence-informed):** nociceptive 40%, mixed 25%, nociplastic 20%, neuropathic 15%.
- **Realism features:** probabilistic (not deterministic) class patterns, correlated variables (CSI–sleep; latent psychological distress), clinically informed missing data (MCAR, MAR, MNAR), and imaging "not performed" as an informative category.
- **Red flags:** 190 patients (9.5%) with ≥ 1 red flag (including serious imaging findings) were excluded from modelling, leaving 1,810 eligible patients.
- **Split:** stratified 80/20 → 1,448 training / 362 test patients (one row per patient, so no patient overlap).

## 4. Performance

### Cross-validation (training set, stratified 5-fold)

| Model | Balanced accuracy | Macro F1 | AUROC (OvR) |
|---|---|---|---|
| **Logistic regression (selected)** | **0.796** | **0.783** | **0.953** |
| Random forest | 0.802 | 0.795 | 0.949 |

Adding missing-value indicators did not improve performance.

### Held-out test set (n = 362, opened once)

**Balanced accuracy 0.805 · Accuracy 0.826 · AUROC 0.96**

| Mechanism | Precision | Recall (sensitivity) | n |
|---|---|---|---|
| Nociceptive | 0.953 | 0.986 | 143 |
| Neuropathic | 0.762 | 0.873 | 55 |
| Mixed | 0.694 | 0.621 | 95 |
| Nociplastic | 0.773 | 0.739 | 69 |

**Error analysis:** errors concentrate on the clinically ambiguous **mixed** class (e.g., 25% of nociplastic and 13% of neuropathic cases predicted as mixed). The most harmful confusions are rare: neuropathic → nociceptive 0%; nociplastic → nociceptive 1% (1 of 69).

### Robustness tests

| Test | Result |
|---|---|
| **Prevalence shift** (scenario B: chronic pain clinic — nociceptive 20%, neuropathic 10%, mixed 30%, nociplastic 40%) | Balanced accuracy 0.811 (stable); accuracy 0.769. Per-class recall stable; precision changed with prevalence (nociplastic 0.77 → 0.87; neuropathic 0.76 → 0.65), as expected from Bayes' theorem |
| **Ablation without imaging** (retrained) | Balanced accuracy 0.780; neuropathic recall 0.80 |
| **Workflow change: no imaging available** (final model) | Balanced accuracy 0.779; neuropathic recall 0.76; nociplastic → nociceptive errors 2 of 69 |

Imaging contributes mainly through clinically meaningful findings (concordant nerve compression), with minimal reliance on the "not performed" pattern.

## 5. Interpretability

- **Global:** coefficients are consistent with published criteria — duration, widespread distribution and CSI drive nociplastic predictions; dermatomal distribution, painDETECT, DN4 and concordant nerve compression drive neuropathic predictions; short duration and localised pain drive nociceptive predictions. Psychosocial variables have near-zero weights.
- **Local:** SHAP waterfall plots explain each individual prediction. When the top two probabilities are close, the tool should communicate uncertainty (e.g., "profile between mixed and nociplastic").

## 6. Fairness and bias (MINIMAR)

| MINIMAR element | This project |
|---|---|
| Study population and setting | Synthetic adults with musculoskeletal pain; primary care case mix (scenario A) and chronic pain clinic case mix (scenario B) |
| Patient demographics | **Not available** — the synthetic data contain no age, sex, ethnicity or socioeconomic variables |
| Model architecture | Multinomial logistic regression with a rule-based red-flag gate |
| Model evaluation | Stratified 5-fold CV, held-out test set, prevalence-shift and imaging-shortcut tests |

- **Subgroup fairness could not be assessed** because no demographic variables exist. With real data, performance must be reported by sex, age group, ethnicity and socioeconomic status.
- **Known bias risks with real data:** measurement bias (questionnaire validity across languages and cultures), representation bias (who reaches specialist care), and access bias (imaging ordered unequally).
- **Ethical design choice:** psychosocial factors were generated in all classes with only a modest increase in nociplastic pain, to avoid encoding the stigma that nociplastic pain is "psychological".

## 7. Limitations

1. **Synthetic data:** the model learns the rules encoded in the data-generation process. Results demonstrate the end-to-end method, **not clinical validity**.
2. **Simplified clinical picture:** real assessment includes physical examination findings not modelled here, such as neurodynamic tests, quantitative sensory testing, **gait assessment** (for the lumbar spine and lower limbs) and **assessment of functional arm movements** (for the cervical spine and upper limbs), which reveal movement patterns and motor behaviour relevant to the pain mechanism.
3. **Mixed pain** is defined inconsistently in the literature and is the least reliable class.
4. **Simplified relationships:** e.g., sleep is modelled as a consequence of central sensitisation, although the relationship is bidirectional.
5. **No external, temporal or geographic validation.**

## 8. Recommendations before any real-world use

1. Train and validate on real, ethically approved clinical data, with expert-adjudicated labels.
2. External validation in different settings, plus subgroup fairness analysis.
3. Local validation in **silent mode** before go-live, with clinician feedback.
4. Monitoring after deployment (data drift, performance, safety events) and a defined process for model updates.
5. Regulatory assessment (EU MDR, EU AI Act) and data protection (GDPR).

## References

See `docs/pain_mechanism_criteria.md` for clinical references. Model reporting follows Mitchell M, et al. Model Cards for Model Reporting. *FAT\* '19*, 2019; and Hernandez-Boussard T, et al. MINIMAR (MINimum Information for Medical AI Reporting). *J Am Med Inform Assoc*. 2020;27(12):2011-2015.
