# 🛡️ Vendor Risk Intelligence Platform

An end-to-end **Third-Party Risk Management (TPRM)** platform built for telecom vendor assessments. Automatically scores vendor risk, detects anomalies using ML, and generates AI-powered executive summaries for CISOs and managers.

---

## 🔗 Live Demo
> Add your Streamlit Cloud link here after deployment

---

## 📌 Problem Statement

Telecom companies work with hundreds of vendors — tower maintenance, fiber operations, cloud services, NOC operations and more. Security teams need to know:

- Which vendors are high risk?
- Which risks remain unresolved?
- Which vendors need immediate attention?

Manually reviewing vendor assessments takes days. This platform automates the entire process in seconds.

---

## ⚡ Features

| Feature | Description |
|---|---|
| 📤 CSV Upload | Upload vendor assessment data in CSV format |
| ⚡ Risk Scoring Engine | Weighted formula scoring 9 risk factors |
| 🚨 Immediate Action Panel | Top 5 critical vendors flagged at the top |
| 📊 Interactive Dashboard | Charts by tier, category, and region |
| 🔍 Vendor Deep Dive | Full breakdown of any individual vendor |
| 🤖 ML Anomaly Detection | Isolation Forest flags statistically abnormal vendors |
| 📝 AI Executive Summary | LLM generates a 3-sentence CISO-ready briefing |
| ⬇️ Export | Download filtered results as CSV |

---

## 🏗️ Architecture

─────────────────────┐         ┌──────────────────────────┐
│  Streamlit Frontend │──HTTP──▶│     FastAPI Backend       │
│  frontend/app.py    │         │  backend/main.py          │
└─────────────────────┘         │  backend/risk_engine.py   │
│  backend/model.py         │
│  backend/utils.py         │
└────────────┬─────────────┘
│
┌─────────▼──────────┐
│  Groq API (LLM)    │
│  Isolation Forest  │
└────────────────────┘

---

## 📊 Risk Scoring Formula

```python
score = (
    Critical_Findings        * 3   +
    High_Findings            * 1.5 +
    Open_Risks               * 1   +
    (100 - Compliance_Score) * 0.4 +
    VAPT_Findings            * 1.5 +
    DLP_Violations           * 2   +
    Security_Incidents       * 5   +
    SLA_Breaches             * 2   +
    Mitigation_Overdue_Days  * 0.1
)
# +5 if MFA not enabled
# +5 if Data Access Level is Sensitive
```

| Score | Tier |
|---|---|
| 90–200 | 🔴 Critical |
| 60–89  | 🟠 High |
| 30–59  | 🟡 Medium |
| 0–29   | 🟢 Low |

---

## 🤖 ML Model

**Isolation Forest** (unsupervised anomaly detection)

- No labelled data required
- Trained on 1000 synthetic telecom vendors
- Flags vendors that are statistically abnormal across all risk factors combined
- Catches risk patterns the rule-based formula alone would miss

---

## 🚀 Quickstart

### 1. Clone and install

```bash
git clone https://github.com/anvii27/Vendor-Risk-Platform
cd Vendor-Risk-Platform
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
export GROQ_API_KEY=your_groq_key_here
```

### 3. Run backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

### 4. Run frontend

```bash
cd frontend
streamlit run app.py
```

---

## 📁 Project Structure

vendor-risk-platform/
├── backend/
│   ├── main.py              # FastAPI endpoints
│   ├── risk_engine.py       # Risk scoring formula
│   ├── model.py             # Isolation Forest ML model
│   └── utils.py             # Groq LLM integration
├── frontend/
│   └── app.py               # Streamlit dashboard
├── data/
│   └── vendors.csv          # 1000 synthetic telecom vendors
├── models/
│   └── isolation_forest.pkl # Trained ML model
├── notebooks/
│   ├── generate_data.py     # Synthetic data generation
│   ├── train_model.py       # Model training script
│   ├── test_scoring.py      # Scoring verification
│   └── test_summary.py      # LLM summary testing
└── requirements.txt

---

## 📋 Required CSV Columns

Vendor_ID, Vendor_Name, Vendor_Category, Vendor_Circle,
Service_Criticality, Region, Critical_Findings, High_Findings,
Open_Risks, Compliance_Score, VAPT_Findings, Patch_Compliance,
MFA_Enabled, Data_Access_Level, DLP_Violations, Security_Incidents,
SLA_Breaches, Mitigation_Overdue_Days, Last_Assessment_Date,
Assessment_Frequency, Risk_Review_Status

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| ML Model | Isolation Forest (scikit-learn) |
| Charts | Plotly |
| LLM Summaries | Groq + Llama 3.3 70B |
| Data Processing | pandas, numpy |
| Synthetic Data | Faker |

---

## 📚 Frameworks Referenced

- NIST Cybersecurity Framework (CSF)
- SIG Lite (Shared Assessments)
- ISO/IEC 27001

---

## 🗺️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Upload and validate CSV |
| POST | `/score` | Calculate risk scores |
| POST | `/predict` | Run anomaly detection |
| POST | `/summary` | Generate AI executive summary |

---

## 👤 Author

Built as a portfolio project demonstrating Third-Party Risk Management (TPRM) automation skills developed during a security risk internship.

---

## 📄 License

MIT
