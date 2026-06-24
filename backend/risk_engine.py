import pandas as pd

df = pd.read_csv("../data/vendors.csv")

def calculate_risk_score(row):
    score = (
        row["Critical_Findings"] * 3 +
        row["High_Findings"] * 1.5 +
        row["Open_Risks"] * 1 +
        (100 - row["Compliance_Score"]) * 0.4 +
        row["VAPT_Findings"] * 1.5 +
        row["DLP_Violations"] * 2 +
        row["Security_Incidents"] * 5 +
        row["SLA_Breaches"] * 2 +
        row["Mitigation_Overdue_Days"] * 0.1
    )

    if row["MFA_Enabled"] == "No":
        score += 5

    if row["Data_Access_Level"] == "Sensitive":
        score += 5

    return round(score, 2)

def categorize_risk(score):
    if score >= 90:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"
    
def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Risk_Score"]            = df.apply(calculate_risk_score, axis=1)
    df["Calculated_Risk_Level"] = df["Risk_Score"].apply(categorize_risk)
    return df.sort_values("Risk_Score", ascending=False).reset_index(drop=True)

def get_summary_stats(df: pd.DataFrame) -> dict:
    return {
        "total":    len(df),
        "critical": int((df["Calculated_Risk_Level"] == "Critical").sum()),
        "high":     int((df["Calculated_Risk_Level"] == "High").sum()),
        "medium":   int((df["Calculated_Risk_Level"] == "Medium").sum()),
        "low":      int((df["Calculated_Risk_Level"] == "Low").sum()),
        "avg_score": round(df["Risk_Score"].mean(), 1),
    }
