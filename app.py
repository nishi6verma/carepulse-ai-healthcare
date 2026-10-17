import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CarePulse | Healthcare Prioritisation", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.4rem;}
[data-testid="stMetric"] {background: #f4f8fc; padding: 14px; border-radius: 10px; border: 1px solid #dce7f1;}
</style>
""", unsafe_allow_html=True)

st.title("🩺 CarePulse")
st.subheader("Real-Time AI-Assisted Healthcare Prioritisation")
st.caption("IBM Z / LinuxONE Datathon concept prototype • Synthetic demo data only")
st.warning("Research/demo only — not a medical device. Scores are illustrative, not clinically validated, and must never be used to diagnose or make real patient-care decisions.")

# Entirely synthetic sample records for demonstration.
SAMPLE = [
    {"Patient ID":"CP-1001", "Age":67, "Heart Rate":128, "SpO₂ (%)":89, "Systolic BP":88, "Temperature (°C)":39.1, "Symptoms":"Shortness of breath, dizziness", "Arrival":"2 min ago"},
    {"Patient ID":"CP-1002", "Age":54, "Heart Rate":104, "SpO₂ (%)":94, "Systolic BP":105, "Temperature (°C)":38.4, "Symptoms":"Fever, weakness", "Arrival":"5 min ago"},
    {"Patient ID":"CP-1003", "Age":29, "Heart Rate":82, "SpO₂ (%)":98, "Systolic BP":122, "Temperature (°C)":36.8, "Symptoms":"Mild headache", "Arrival":"8 min ago"},
    {"Patient ID":"CP-1004", "Age":73, "Heart Rate":112, "SpO₂ (%)":92, "Systolic BP":96, "Temperature (°C)":37.9, "Symptoms":"Fatigue, nausea", "Arrival":"11 min ago"},
    {"Patient ID":"CP-1005", "Age":41, "Heart Rate":76, "SpO₂ (%)":99, "Systolic BP":128, "Temperature (°C)":37.0, "Symptoms":"Minor ankle pain", "Arrival":"14 min ago"},
]


def score_case(row):
    """Transparent illustrative score. Not a validated clinical scoring system."""
    score, reasons = 0, []
    if row["SpO₂ (%)"] < 90:
        score += 4; reasons.append("Low oxygen saturation (<90%)")
    elif row["SpO₂ (%)"] < 94:
        score += 2; reasons.append("Reduced oxygen saturation (<94%)")
    if row["Systolic BP"] < 90:
        score += 4; reasons.append("Low systolic blood pressure (<90 mmHg)")
    elif row["Systolic BP"] < 100:
        score += 2; reasons.append("Lower systolic blood pressure (<100 mmHg)")
    if row["Heart Rate"] >= 130 or row["Heart Rate"] < 40:
        score += 3; reasons.append("Markedly abnormal heart rate")
    elif row["Heart Rate"] >= 120 or row["Heart Rate"] < 50:
        score += 2; reasons.append("Abnormal heart rate")
    if row["Temperature (°C)"] >= 39.0 or row["Temperature (°C)"] < 35.0:
        score += 2; reasons.append("Temperature outside illustrative range")
    elif row["Temperature (°C)"] >= 38.0:
        score += 1; reasons.append("Elevated temperature")
    if row["Age"] >= 75:
        score += 1; reasons.append("Older-age context flag")
    if score >= 6:
        priority = "Urgent review"
    elif score >= 3:
        priority = "Prompt review"
    else:
        priority = "Routine review"
    return pd.Series([score, priority, "; ".join(reasons) if reasons else "No configured demo threshold triggered"])

if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(SAMPLE)

with st.sidebar:
    st.header("Demo controls")
    st.write("Use synthetic cases or add a new sample case.")
    if st.button("Reset sample patients", use_container_width=True):
        st.session_state.patients = pd.DataFrame(SAMPLE)
        st.rerun()
    st.divider()
    st.subheader("Add a demo patient")
    with st.form("new_patient"):
        pid = st.text_input("Patient ID", value=f"CP-{1000 + len(st.session_state.patients) + 1}")
        age = st.number_input("Age", min_value=0, max_value=120, value=45)
        hr = st.number_input("Heart rate (bpm)", min_value=20, max_value=250, value=88)
        spo2 = st.number_input("SpO₂ (%)", min_value=50, max_value=100, value=97)
        sbp = st.number_input("Systolic BP (mmHg)", min_value=40, max_value=250, value=120)
        temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=43.0, value=37.0, step=0.1)
        symptoms = st.text_input("Symptoms", value="Demo symptoms")
        submitted = st.form_submit_button("Add synthetic case", use_container_width=True)
        if submitted:
            new_row = {"Patient ID": pid, "Age": int(age), "Heart Rate": int(hr), "SpO₂ (%)": int(spo2), "Systolic BP": int(sbp), "Temperature (°C)": float(temp), "Symptoms": symptoms, "Arrival": "just now"}
            st.session_state.patients = pd.concat([st.session_state.patients, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()

patients = st.session_state.patients.copy()
scored = patients.join(patients.apply(score_case, axis=1).rename(columns={0:"Score", 1:"Priority", 2:"Reason"}))
priority_order = {"Urgent review":0, "Prompt review":1, "Routine review":2}
scored["_order"] = scored["Priority"].map(priority_order)
scored = scored.sort_values(["_order", "Score"], ascending=[True, False]).drop(columns="_order")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Synthetic cases", len(scored))
c2.metric("Urgent review flags", int((scored["Priority"] == "Urgent review").sum()))
c3.metric("Prompt review flags", int((scored["Priority"] == "Prompt review").sum()))
c4.metric("Last refreshed", datetime.now().strftime("%H:%M:%S"))

st.markdown("### Prioritised worklist")
st.caption("The ranking is generated from transparent demo thresholds and is not a validated triage score.")
show_cols = ["Patient ID", "Age", "Heart Rate", "SpO₂ (%)", "Systolic BP", "Temperature (°C)", "Symptoms", "Arrival", "Score", "Priority"]
st.dataframe(scored[show_cols], use_container_width=True, hide_index=True)

st.markdown("### Alert explanations")
for _, row in scored.iterrows():
    with st.expander(f"{row['Patient ID']} — {row['Priority']} (demo score: {row['Score']})"):
        st.write(f"**Symptoms entered:** {row['Symptoms']}")
        st.write(f"**Illustrative trigger(s):** {row['Reason']}")
        st.write("**Suggested workflow:** A qualified clinician reviews the patient context and determines the appropriate next step. This demo does not issue medical instructions.")

csv = scored.to_csv(index=False).encode("utf-8")
st.download_button("Download demo worklist (CSV)", data=csv, file_name="carepulse_demo_worklist.csv", mime="text/csv")

st.markdown("### Reference architecture")
cols = st.columns(4)
architecture = [
    ("1 · Data input", "Synthetic vitals and symptom events"),
    ("2 · Processing", "Validation, threshold rules, scoring"),
    ("3 · Alert service", "Priority labels and explanations"),
    ("4 · Human review", "Clinician-led assessment and audit"),
]
for col, (heading, body) in zip(cols, architecture):
    with col:
        st.info(f"**{heading}**\n\n{body}")
st.caption("IBM Z / LinuxONE are proposed target infrastructure for secure, resilient deployment; this local prototype has not been deployed to IBM infrastructure.")
