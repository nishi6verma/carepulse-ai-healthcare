# CarePulse — Real-Time AI-Assisted Healthcare Prioritisation

**IBM Z Datathon 2026 · AI for Good · Prototype concept**

CarePulse is a demo dashboard that illustrates how incoming patient observations could be organised into an explainable review worklist. It uses synthetic records and transparent, illustrative rules to produce priority labels and alert explanations.

> **Safety notice:** This is an educational prototype, not a medical device or validated triage system. Do not use it with real patients or for clinical decisions. Scores and thresholds are illustrative only. Clinical deployment would require clinical governance, validation, privacy/security review, regulatory assessment where applicable, and approval by qualified professionals.

## Features

- Interactive Streamlit dashboard
- Synthetic sample patient records
- Add a synthetic case through the sidebar
- Explainable demo score based on configured thresholds
- Priority worklist and alert explanations
- CSV export of the demo worklist
- Architecture concept aligned to a potential IBM Z / LinuxONE deployment

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Project structure

```text
carepulse-ai-healthcare/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── docs/
    └── architecture.md
```

## Architecture concept

1. **Input layer:** authorised EHR or monitoring integrations would provide timestamped observations.
2. **Validation layer:** validate schemas, timestamps, missing values, and duplicate events.
3. **Rules/model service:** a clinically validated model and approved rules would create risk signals with explanations. The current demo uses only illustrative thresholds.
4. **Alert/worklist service:** rank cases for review, with configurable escalation and audit logging.
5. **Human review:** authorised clinicians assess context and decide next steps.
6. **Platform:** IBM Z and/or LinuxONE could be considered for secure, resilient enterprise processing, depending on available services and deployment requirements.

## IBM Z / LinuxONE positioning

This repository is a local prototype and **has not been deployed to IBM Z or LinuxONE**. The deck/application may describe these as proposed target platforms. A real deployment would need to map components to the specific infrastructure, security services, integration patterns, and access available to the team.

## Suggested next steps

- Replace synthetic data with a publicly available, appropriately licensed and de-identified dataset for offline evaluation only.
- Add automated tests for input validation and scoring logic.
- Work with clinical stakeholders to define safe requirements and evaluation metrics.
- Measure latency, sensitivity, false-alert rate, calibration, subgroup performance, and usability before considering a pilot.
- Add authentication, role-based access, audit trails, encryption, monitoring, and a documented incident process before any sensitive-data use.

## License

For datathon demonstration and educational use. Add a formal license before public reuse or distribution.
