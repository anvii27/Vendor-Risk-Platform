import os
import google.generativeai as genai


API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.0-flash"


def generate_vendor_summary(vendor: dict) -> str:
    """
    Calls Gemini API to write a 3-sentence executive summary
    for a single vendor, written for a CISO audience.
    """
    if not API_KEY:
        return "⚠️ GEMINI_API_KEY not set. Add it to your environment to enable AI summaries."

    anomaly_note = (
        "The ML model has flagged this vendor as a statistical anomaly compared to the overall vendor population."
        if vendor.get("Anomaly")
        else "The ML model considers this vendor's profile within normal range."
    )

    prompt = f"""You are a senior cybersecurity risk analyst writing a briefing for a CISO.
Write exactly 3 sentences. No bullet points, no headers.

Vendor data:
- Name: {vendor.get('Vendor_Name')}
- Risk Score: {vendor.get('Risk_Score', 'N/A')} / 200
- Risk Tier: {vendor.get('Calculated_Risk_Level', 'N/A')}
- Critical Findings: {vendor.get('Critical_Findings', 0)}
- High Findings: {vendor.get('High_Findings', 0)}
- Security Incidents: {vendor.get('Security_Incidents', 0)}
- DLP Violations: {vendor.get('DLP_Violations', 0)}
- SLA Breaches: {vendor.get('SLA_Breaches', 0)}
- Days Overdue: {vendor.get('Mitigation_Overdue_Days', 0)}
- MFA Enabled: {vendor.get('MFA_Enabled', 'Unknown')}
- Compliance Score: {vendor.get('Compliance_Score', 0)}%
- Data Access Level: {vendor.get('Data_Access_Level', 'Unknown')}
- ML Anomaly Detection: {anomaly_note}

Rules:
1. Sentence 1 — summarise the current risk posture and score.
2. Sentence 2 — name the top 2 drivers of this risk.
3. Sentence 3 — give a concrete, actionable recommendation (escalate / remediate / monitor / deprioritise).
Be direct. No hedging. Write as if presenting to a board."""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {e}"