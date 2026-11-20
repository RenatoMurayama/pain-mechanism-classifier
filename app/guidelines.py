# Fixed, guideline-based educational content (not machine learning)
# Sources: Lin et al. 2020 (BJSM); NICE NG59, NG193, CG173

COMMON_PRINCIPLES = [
    "Patient-centred care: listen, explain and agree goals together",
    "Education and reassurance about a usually favourable course",
    "Promote physical activity and exercise",
    "Assess psychosocial factors and monitor progress over time",
]

GUIDELINES = {
    "nociceptive": {
        "do": [
            "Explain the tissue-related cause and expected recovery",
            "Graded activity and exercise matched to tissue tolerance",
            "Use manual therapy only as an adjunct to active care",
        ],
        "avoid": [
            "Routine imaging without red flags",
            "Prolonged rest or passive treatment as the only approach",
        ],
        "refer": [
            "Medical review if recovery does not follow the expected course",
            "Urgent referral if any red flag appears",
        ],
    },
    "neuropathic": {
        "do": [
            "Explain nerve-related pain in simple terms",
            "Graded exercise and neural mobilisation within symptom tolerance",
            "Monitor sensation, strength and reflexes over time",
        ],
        "avoid": [
            "Loading that causes lasting symptom flare-ups",
            "Surgical referral before a trial of non-surgical care (unless red flags)",
        ],
        "refer": [
            "Medical review to consider medication (NICE CG173)",
            "Urgent referral if neurological deficit progresses",
        ],
    },
    "nociplastic": {
        "do": [
            "Pain neuroscience education: pain is real, the nervous system is sensitised",
            "Graded activity and exercise with pacing",
            "Address sleep, stress and fatigue as part of the plan",
        ],
        "avoid": [
            "Repeated imaging or searching for a single tissue cause",
            "Explanations that increase threat (e.g., 'damaged' or 'degenerated')",
        ],
        "refer": [
            "Psychological therapy (e.g., CBT or ACT) when distress is high (NICE NG193)",
            "Interdisciplinary pain service if pain is persistent and disabling",
        ],
    },
    "mixed": {
        "do": [
            "Identify the dominant component and address each one",
            "Combine education with graded exercise",
            "Reassess regularly: the dominant mechanism can change",
        ],
        "avoid": [
            "A single-mechanism approach",
            "Relying on one questionnaire to decide",
        ],
        "refer": [
            "Medical review if a neuropathic component needs medication",
            "Interdisciplinary care for complex or persistent cases",
        ],
    },
}