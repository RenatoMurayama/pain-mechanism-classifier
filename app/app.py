from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from guidelines import COMMON_PRINCIPLES, GUIDELINES

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_DIR / "models" / "pain_mechanism_model.joblib"

# Page setup
st.set_page_config(page_title="Pain Mechanism Classifier", layout="centered")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

# Header
st.title("Pain Mechanism Classifier")
st.caption("Educational decision-support prototype for health and movement professionals.")
st.warning("Not a medical device. Trained on synthetic data. Does not replace clinical judgement.")

# Red-flag screening (rule-based, not ML)
RED_FLAGS = {
    "cancer": "History of cancer or unexplained weight loss",
    "infection": "Fever, recent infection, immunosuppression or IV drug use",
    "cauda_equina": "Saddle anaesthesia, bladder/bowel changes or bilateral neurological signs",
    "fracture": "Major trauma, osteoporosis or prolonged corticosteroid use",
    "neuro_deficit": "Progressive neurological deficit",
    "inflammatory": "Inflammatory signs (morning stiffness > 30 min, raised CRP/ESR)",
    "imaging_serious": "Serious imaging finding (e.g., fracture, suspected malignancy, cord compression)",
}

st.header("1. Red-flag screening")
st.write("Tick any red flag found at any stage of the assessment (history, examination, imaging or labs).")

flags_present = []
for key, label in RED_FLAGS.items():
    if st.checkbox(label, key=key):
        flags_present.append(label)

if flags_present:
    st.error("Red flag(s) present: refer for medical assessment. No pain mechanism classification is shown.")
    for label in flags_present:
        st.markdown(f"- {label}")
    st.stop()

st.success("No red flags ticked. Continue to the pain assessment.")
st.caption("Screen again whenever new information appears during assessment or treatment.")

# Model inputs (same names and order as training)
FEATURE_ORDER = list(model.feature_names_in_)
CATEGORICAL_FEATURES = ["pain_distribution", "imaging_tissue_finding", "imaging_nerve_compression"]
NUMERIC_FEATURES = [col for col in FEATURE_ORDER if col not in CATEGORICAL_FEATURES]

# Display labels for categorical options
DISTRIBUTION_LABELS = {
    "localized": "Localised (at the site of injury/dysfunction)",
    "dermatomal": "Dermatomal / nerve territory",
    "regional": "Regional (beyond one site, not widespread)",
    "widespread": "Widespread",
}
IMAGING_LABELS = {"yes": "Yes", "no": "No", "not_performed": "Not performed"}

st.header("2. Pain assessment")
st.write("Leave a questionnaire empty if it was not applied.")

with st.form("assessment_form"):
    st.subheader("History")
    duration = st.number_input("Pain duration (months)", min_value=0.25, max_value=240.0, value=3.0, step=0.5)
    distribution = st.selectbox("Pain distribution", options=list(DISTRIBUTION_LABELS), format_func=DISTRIBUTION_LABELS.get)
    sleep = st.slider("Sleep quality (0 = very poor, 10 = very good)", 0, 10, 6)

    st.subheader("Pain questionnaires")
    dn4 = st.number_input("DN4 (0-10)", min_value=0, max_value=10, value=None, placeholder="Not applied")
    paindetect = st.number_input("painDETECT (-1 to 38)", min_value=-1, max_value=38, value=None, placeholder="Not applied")
    csi = st.number_input("CSI, Part A (0-100)", min_value=0, max_value=100, value=None, placeholder="Not applied")

    st.subheader("Imaging (findings concordant with symptoms)")
    tissue = st.radio("Tissue finding", options=list(IMAGING_LABELS), format_func=IMAGING_LABELS.get, index=2, horizontal=True)
    nerve = st.radio("Nerve compression", options=list(IMAGING_LABELS), format_func=IMAGING_LABELS.get, index=2, horizontal=True)

    st.subheader("Psychosocial factors")
    hads_a = st.number_input("HADS anxiety (0-21)", min_value=0, max_value=21, value=None, placeholder="Not applied")
    hads_d = st.number_input("HADS depression (0-21)", min_value=0, max_value=21, value=None, placeholder="Not applied")
    pcs = st.number_input("PCS, catastrophising (0-52)", min_value=0, max_value=52, value=None, placeholder="Not applied")
    tsk = st.number_input("TSK, fear of movement (17-68)", min_value=17, max_value=68, value=None, placeholder="Not applied")
    work_stress = st.slider("Work stress (0 = none, 10 = extreme)", 0, 10, 5)

    submitted = st.form_submit_button("Classify pain mechanism")

if not submitted:
    st.stop()

# Build one-row table for the model
inputs = {
    "pain_duration_months": duration,
    "dn4_score": dn4,
    "paindetect_score": paindetect,
    "csi_score": csi,
    "sleep_quality": sleep,
    "hads_anxiety": hads_a,
    "hads_depression": hads_d,
    "pcs_score": pcs,
    "tsk_score": tsk,
    "work_stress": work_stress,
    "pain_distribution": distribution,
    "imaging_tissue_finding": tissue,
    "imaging_nerve_compression": nerve,
}
X_new = pd.DataFrame([inputs])[FEATURE_ORDER]
X_new[NUMERIC_FEATURES] = X_new[NUMERIC_FEATURES].astype(float)

# Prediction
probas = model.predict_proba(X_new)[0]
proba_table = pd.Series(probas, index=model.classes_).sort_values(ascending=False)
top_class, second_class = proba_table.index[0], proba_table.index[1]
top_p, second_p = proba_table.iloc[0], proba_table.iloc[1]

st.header("3. Result")
st.subheader(f"Predicted predominant mechanism: {top_class.capitalize()} ({top_p:.0%})")

for mechanism, p in proba_table.items():
    st.progress(float(p), text=f"{mechanism.capitalize()}: {p:.0%}")

# Warnings
UNCERTAINTY_MARGIN = 0.15
if top_p - second_p < UNCERTAINTY_MARGIN:
    st.warning(f"Uncertain result: profile between {top_class} and {second_class}. Use clinical reasoning to decide.")

if tissue == "not_performed" and nerve == "not_performed":
    st.info("No imaging available. In testing, neuropathic sensitivity dropped from 87% to 76% without imaging.")

missing = [col for col in NUMERIC_FEATURES if pd.isna(X_new.at[0, col])]
if missing:
    st.info(f"Not applied: {', '.join(missing)}. Training medians were used, so the result is less reliable.")

# Explanation: linear contributions for the predicted class
preprocess = model.named_steps["preprocess"]
classifier = model.named_steps["model"]
x_t = preprocess.transform(X_new)[0]
feature_names = [name.split("__", 1)[1] for name in preprocess.get_feature_names_out()]
class_idx = list(classifier.classes_).index(top_class)
contributions = pd.Series(classifier.coef_[class_idx] * x_t, index=feature_names)

supporting = contributions[contributions > 0].sort_values(ascending=False).head(3)
against = contributions[contributions < 0].sort_values().head(2)

def describe(name):
    label = name.replace("_", " ")
    if name in X_new.columns and pd.notna(X_new.at[0, name]):
        return f"{label} = {X_new.at[0, name]:g}"
    return label


st.subheader("Main reasons")
st.write(f"**Towards {top_class}:**")
for name, value in supporting.items():
    st.markdown(f"- {describe(name)} (+{value:.2f})")
st.write(f"**Against {top_class}:**")
for name, value in against.items():
    st.markdown(f"- {describe(name)} ({value:.2f})")
st.caption("Contributions in log-odds compared with an average training patient. They describe the model, not the cause of pain.")

# Guideline-based recommendations
SECTION_TITLES = {"do": "Do", "avoid": "Avoid", "refer": "Refer"}


def show_guidelines(mechanism):
    for section, title in SECTION_TITLES.items():
        st.markdown(f"**{title}**")
        for item in GUIDELINES[mechanism][section]:
            st.markdown(f"- {item}")


st.header("4. Guideline-based recommendations")
st.caption("Fixed educational content, not machine learning. Users without diagnostic competence: use for education and referral only.")

st.markdown("**For all mechanisms**")
for item in COMMON_PRINCIPLES:
    st.markdown(f"- {item}")

st.subheader(top_class.capitalize())
show_guidelines(top_class)

if top_p - second_p < UNCERTAINTY_MARGIN:
    with st.expander(f"Also consider: {second_class.capitalize()}"):
        show_guidelines(second_class)

st.caption("Sources: Lin et al. 2020 (BJSM); NICE NG59, NG193 and CG173.")