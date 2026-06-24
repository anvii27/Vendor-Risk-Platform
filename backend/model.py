import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest 
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__),"../models/isolation_forest.pkl")

FEATURES=[
    "Critical_Findings",
    "High_Findings",
    "Open_Risks",
    "Compliance_Score",
    "VAPT_Findings",
    "DLP_Violations",
    "Security_Incidents",
    "SLA_Breaches",
    "Mitigation_Overdue_Days",
]

def train_model(df: pd.DataFrame):
    X = df[FEATURES].fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42
    )
    model.fit(X_scaled)

    joblib.dump(
        {
            "model": model, "scaler": scaler, "features": FEATURES
        },MODEL_PATH
    )
    print(f"Model saved to {MODEL_PATH}")

    preds = model.predict(X_scaled)
    anomaly_count = (preds == -1).sum()
    print(f"Anomalies detected in training data: {anomaly_count} / {len(df)}")

_bundle = None

def _load_model():
    global _bundle
    if _bundle is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Model not found. Run train_model.py first."
            )
        _bundle = joblib.load(MODEL_PATH)
    return _bundle

def predict_anomalies(df: pd.DataFrame) -> pd.DataFrame:

    bundle = _load_model()
    model   = bundle["model"]
    scaler  = bundle["scaler"]
    features = bundle["features"]

    X = df[features].fillna(0)
    X_scaled = scaler.transform(X)

    preds  = model.predict(X_scaled)       # 1 = normal, -1 = anomaly
    scores = model.decision_function(X_scaled)

    result = df.copy()
    result["Anomaly"]       = preds == -1
    result["Anomaly_Score"] = np.round(scores, 4)

    return result

def get_anomaly_summary(df: pd.DataFrame) -> dict:

    if "Anomaly" not in df.columns:
        return {"count": 0, "vendors": []}

    flagged = df[df["Anomaly"] == True]
    return {
        "count": len(flagged),
        "vendors": flagged["Vendor_Name"].tolist()
    }