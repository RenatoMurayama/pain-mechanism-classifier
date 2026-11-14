# Pain Mechanism Criteria — Clinical Rationale

**Project:** pain-mechanism-classifier
**Author:** Renato Murayama (Physiotherapist · MSc Medical Informatics student)
**Version:** 0.1 — November 2026

> **Purpose.** This document summarises the evidence-based clinical criteria used to design the synthetic dataset and the decision-support logic of this project. It is an educational reference, **not a diagnostic protocol**. The tool supports — and never replaces — the clinical judgement of qualified health professionals.

---

## 1. Definitions (IASP)

- **Pain** — "An unpleasant sensory and emotional experience associated with, or resembling that associated with, actual or potential tissue damage" (Raja et al., 2020). Pain is always a personal experience, influenced by biological, psychological and social factors.
- **Mechanistic descriptors** recognised by the IASP:

| Descriptor | Definition (summary) | Key reference |
|---|---|---|
| **Nociceptive** | Pain arising from actual or threatened damage to non-neural tissue, due to activation of nociceptors | IASP terminology |
| **Neuropathic** | Pain caused by a lesion or disease of the somatosensory nervous system | Treede et al., 2008; Finnerup et al., 2016 |
| **Nociplastic** | Pain arising from altered nociception despite no clear evidence of tissue damage or of disease/lesion of the somatosensory system | Kosek et al., 2016; Kosek et al., 2021 |
| **Mixed** *(clinical concept, not an IASP descriptor)* | Clinically relevant overlap of two or more mechanisms in the same patient | Freynhagen et al., 2019 |

---

## 2. Step 0 — Safety gate (red flags)

Before any mechanism classification, **serious pathology must be screened**. If red flags are present, the tool does **not** classify and recommends **medical referral**.

Examples (Finucane et al., 2020):
- History of cancer, unexplained weight loss → possible malignancy
- Fever, recent infection, immunosuppression, IV drug use → possible infection
- Saddle anaesthesia, bladder/bowel dysfunction, bilateral neurological signs → possible cauda equina syndrome
- Significant trauma, osteoporosis, prolonged corticosteroid use → possible fracture
- Progressive neurological deficit
- Inflammatory features (e.g., morning stiffness > 30 min, elevated CRP/ESR) → possible inflammatory/rheumatic disease

---

## 3. Clinical indicators by mechanism

Based on Smart et al. (2012, parts 1–3), Shraim et al. (2022, Delphi consensus), Finnerup et al. (2016) and Kosek et al. (2021).

| Indicator | Nociceptive | Neuropathic | Nociplastic |
|---|---|---|---|
| **Duration** | Often acute or subacute; can be chronic | Acute or chronic | Chronic (≥ 3 months, by definition) |
| **Distribution** | Localised to the area of injury/dysfunction | Neuroanatomically plausible (dermatome / nerve territory) | Regional, multifocal or widespread; not anatomically logical |
| **Behaviour** | Clear, proportionate mechanical/anatomical aggravating and easing factors | Associated with nerve provocation (e.g., neurodynamic tests) | Disproportionate, unpredictable; non-mechanical aggravating factors |
| **Quality** | Aching, intermittent, sharp with movement | Burning, shooting, electric, tingling | Diffuse, variable |
| **Sensory signs** | Normal sensation | Sensory deficit or gain in the nerve territory (hypoaesthesia, allodynia) | Widespread hypersensitivity (e.g., allodynia outside the painful area) |
| **History** | Clear mechanism of injury | History or evidence of nerve injury/compression | Comorbidities: sleep disturbance, fatigue, cognitive problems, hypersensitivity to light/sound/smells |
| **Screening tools** | Low DN4/painDETECT and CSI scores | **DN4 ≥ 4** · **painDETECT ≥ 19** | **CSI ≥ 40** |

### Grading systems (summary)

- **Neuropathic pain** (Finnerup et al., 2016): *possible* (history + plausible distribution) → *probable* (+ sensory signs on examination) → *definite* (+ diagnostic test confirming a lesion/disease).
- **Nociplastic pain** (Kosek et al., 2021): *possible* (pain ≥ 3 months, regional/multifocal/widespread distribution, not entirely explained by nociceptive or neuropathic mechanisms, plus clinical signs of pain hypersensitivity) → *probable* (+ history of hypersensitivity **and** comorbidities such as sleep disturbance, fatigue or cognitive problems).

---

## 4. Screening instruments

| Instrument | What it screens | Score range | Cut-off | Reference |
|---|---|---|---|---|
| **DN4** (Douleur Neuropathique 4) | Neuropathic pain (interview + examination) | 0–10 | ≥ 4 | Bouhassira et al., 2005 |
| **painDETECT** | Neuropathic component | −1 to 38 | ≤ 12 unlikely · 13–18 ambiguous · ≥ 19 likely | Freynhagen et al., 2006 |
| **CSI** (Central Sensitization Inventory), Part A | Symptoms related to central sensitisation | 0–100 (25 items × 0–4) | ≥ 40; severity: 0–29 subclinical, 30–39 mild, 40–49 moderate, 50–59 severe, 60–100 extreme | Mayer et al., 2012; Neblett et al., 2013, 2017 |

> **Caution:** CSI scores are also influenced by psychological distress. No single instrument classifies a pain mechanism on its own.

---

## 5. Imaging and laboratory tests

- Imaging findings are **only meaningful when concordant with the clinical presentation**. Degenerative findings (e.g., disc degeneration, bulges) are highly prevalent in **asymptomatic** people and increase with age (Brinjikji et al., 2015).
- In this project, imaging and lab tests are summarised as:
  - *Imaging finding concordant with symptoms* (yes / no / not performed) → supports nociceptive
  - *Nerve compression on imaging, concordant with symptoms* (yes / no / not performed) → supports neuropathic
  - *Elevated inflammatory markers (CRP/ESR)* → contributes to the **red-flag gate**
- Routine imaging is **not recommended** for non-specific musculoskeletal pain without red flags (Lin et al., 2020).

---

## 6. Psychosocial factors (biopsychosocial approach)

Psychosocial factors influence pain experience, disability and prognosis **across all mechanisms** (Lin et al., 2020; Hill et al., 2008).

| Factor | Example instrument | Reference |
|---|---|---|
| Anxiety and depression | HADS | Zigmond & Snaith, 1983 |
| Pain catastrophising | PCS | Sullivan et al., 1995 |
| Fear of movement (kinesiophobia) | TSK | Miller et al., 1991 |
| Prognostic risk (low back pain) | STarT Back Tool | Hill et al., 2008 |
| Work stress, sleep quality | Clinical interview / rating scales | — |

> **Ethical note:** psychosocial factors are **not** synonymous with nociplastic pain. In the synthetic data they are present in all classes, with only a modest increase in the nociplastic group, to avoid encoding the stigma that pain is "all in the head".

---

## 7. Mixed pain

Mixed pain describes a clinically relevant overlap of mechanisms (e.g., nociceptive + neuropathic in radicular low back pain, or nociceptive + nociplastic in chronic osteoarthritis). It is very common in chronic musculoskeletal pain (Freynhagen et al., 2019) and is expected to be the **hardest class** for the model to distinguish.

---

## 8. Best-practice care (what the tool can show after classification)

Eleven consistent recommendations from high-quality clinical practice guidelines (Lin et al., 2020), including: patient-centred care; screening for serious pathology; assessing psychosocial factors; discouraging routine imaging; physical examination; monitoring progress; education and reassurance; addressing physical activity and exercise; manual therapy only as an adjunct; offering evidence-informed non-surgical care before surgery; and facilitating return to work.

Further guidance: NICE NG59 (low back pain and sciatica) and NICE NG193 (chronic primary pain).

---

## 9. Class prevalence assumptions

No single study reports the prevalence of all four classes together, so the class distribution of the synthetic dataset is derived by combining sources:

- **Nociplastic / central sensitisation:** ~22% of patients with low back pain (± leg pain) met clinical criteria for central sensitisation (Smart et al., 2012).
- **Neuropathic component:** ~37% of patients with chronic low back pain had a likely neuropathic component (Freynhagen et al., 2006); a meta-analysis reported a pooled prevalence of ~47% (Gudala et al., 2017). This figure **includes mixed cases**, so it is split between "pure" neuropathic and mixed pain.
- **Nociceptive:** the remaining proportion, consistent with the high share of acute/subacute presentations in primary care.

| Scenario | Nociceptive | Neuropathic | Nociplastic | Mixed | Use in the project |
|---|---|---|---|---|---|
| **A — Evidence-informed (primary care)** | 40% | 15% | 20% | 25% | Main dataset for training and testing |
| **B — Specialised chronic pain setting** (author's clinical caseload estimate) | 20% | 10% | 40% | 30% | Robustness test (dataset shift) |

> **Rationale:** prevalence depends on the clinical setting. Patients in specialised or private physiotherapy practices are often chronic and referred after previous treatments, so nociplastic and mixed presentations are more frequent. Scenario B tests whether the model generalises to a different case mix — a key concept in AI evaluation (generalisability and dataset shift).

---

## 10. How these criteria are used in this project

1. **Red-flag gate** → fixed rules (no machine learning).
2. **Synthetic data generation** → each class is generated with **probabilistic** (not deterministic) patterns derived from the indicators above, including noise, missing values, class imbalance and ambiguous mixed cases.
3. **Machine learning model** → predicts the **predominant mechanism**.
4. **Guideline content** → fixed, mechanism-specific educational recommendations.

---

## 11. Limitations

- The dataset is **synthetic**: the model learns the rules encoded from this document. Results demonstrate the **end-to-end process**, not clinical validity.
- Real-world use would require clinical data, external validation and regulatory assessment (e.g., IMDRF clinical evaluation, EU MDR / AI Act).
- Criteria are simplified for educational purposes and must be applied with clinical judgement.

---

## References

- Bouhassira D, et al. Comparison of pain syndromes associated with nervous or somatic lesions and development of a new neuropathic pain diagnostic questionnaire (DN4). *Pain*. 2005;114(1-2):29-36.
- Brinjikji W, et al. Systematic literature review of imaging features of spinal degeneration in asymptomatic populations. *AJNR Am J Neuroradiol*. 2015;36(4):811-816.
- Finnerup NB, et al. Neuropathic pain: an updated grading system for research and clinical practice. *Pain*. 2016;157(8):1599-1606.
- Finucane LM, et al. International framework for red flags for potential serious spinal pathologies. *J Orthop Sports Phys Ther*. 2020;50(7):350-372.
- Freynhagen R, et al. painDETECT: a new screening questionnaire to identify neuropathic components in patients with back pain. *Curr Med Res Opin*. 2006;22(10):1911-1920.
- Freynhagen R, et al. Current understanding of the mixed pain concept: a brief narrative review. *Curr Med Res Opin*. 2019;35(6):1011-1018.
- Gudala K, et al. High prevalence of neuropathic pain component in patients with low back pain: evidence from meta-analysis. *Pain Physician*. 2017;20(5):343-352.
- Hill JC, et al. A primary care back pain screening tool: identifying patient subgroups for initial treatment. *Arthritis Rheum*. 2008;59(5):632-641.
- Kosek E, et al. Do we need a third mechanistic descriptor for chronic pain states? *Pain*. 2016;157(7):1382-1386.
- Kosek E, et al. Chronic nociplastic pain affecting the musculoskeletal system: clinical criteria and grading system. *Pain*. 2021;162(11):2629-2634.
- Lin I, et al. What does best practice care for musculoskeletal pain look like? Eleven consistent recommendations from high-quality clinical practice guidelines. *Br J Sports Med*. 2020;54(2):79-86.
- Mayer TG, et al. The development and psychometric validation of the Central Sensitization Inventory. *Pain Pract*. 2012;12(4):276-285.
- Miller RP, Kori SH, Todd DD. The Tampa Scale: a measure of kinesiophobia. *Clin J Pain*. 1991;7(1):51.
- Neblett R, et al. The Central Sensitization Inventory (CSI): establishing clinically significant values for identifying central sensitivity syndromes. *J Pain*. 2013;14(5):438-445.
- Neblett R, et al. Establishing clinically relevant severity levels for the Central Sensitization Inventory. *Pain Pract*. 2017;17(2):166-175.
- Raja SN, et al. The revised International Association for the Study of Pain definition of pain: concepts, challenges, and compromises. *Pain*. 2020;161(9):1976-1982.
- Shraim MA, et al. Features and methods to discriminate between mechanism-based categories of pain experienced in the musculoskeletal system: a Delphi expert consensus study. *Pain*. 2022;163(9):1812-1828.
- Smart KM, et al. Mechanisms-based classifications of musculoskeletal pain: parts 1–3. *Man Ther*. 2012;17(4):336-357.
- Sullivan MJL, Bishop SR, Pivik J. The Pain Catastrophizing Scale: development and validation. *Psychol Assess*. 1995;7(4):524-532.
- Treede RD, et al. Neuropathic pain: redefinition and a grading system for clinical and research purposes. *Neurology*. 2008;70(18):1630-1635.
- Zigmond AS, Snaith RP. The Hospital Anxiety and Depression Scale. *Acta Psychiatr Scand*. 1983;67(6):361-370.
- NICE. Low back pain and sciatica in over 16s: assessment and management (NG59). 2016, updated 2020.
- NICE. Chronic pain (primary and secondary) in over 16s: assessment of all chronic pain and management of chronic primary pain (NG193). 2021.
