import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from utils import generate_vendor_summary

test_vendor = {
    "Vendor_Name": "Test Vendor Inc",
    "Risk_Score": 145,
    "Calculated_Risk_Level": "Critical",
    "Critical_Findings": 9,
    "High_Findings": 15,
    "Security_Incidents": 4,
    "DLP_Violations": 5,
    "SLA_Breaches": 4,
    "Mitigation_Overdue_Days": 120,
    "MFA_Enabled": "No",
    "Compliance_Score": 45,
    "Data_Access_Level": "Sensitive",
    "Anomaly": True,
}

summary = generate_vendor_summary(test_vendor)
print(summary)