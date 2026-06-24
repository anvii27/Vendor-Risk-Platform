from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import sys 
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from risk_engine import score_dataframe, get_summary_stats

app = FastAPI(
    title="Vendor Risk Scoring API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_COLUMNS = [
    "Vendor_ID",
    "Vendor_Name",
    "Critical_Findings",
    "High_Findings",
    "Open_Risks",
    "Compliance_Score",
    "VAPT_Findings",
    "DLP_Violations",
    "Security_Incidents",
    "SLA_Breaches",
    "Mitigation_Overdue_Days",
    "MFA_Enabled",
    "Data_Access_Level",
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Check file type
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(
            status_code=400,
            detail="Only .csv and .xlsx files are supported."
        )
    contents = await file.read()
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not read file: {e}"
        )
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required columns: {missing}"
        )

    return {
        "message": "File uploaded successfully",
        "rows": len(df),
        "data": df.to_dict(orient="records")
    }

@app.post("/score")
def score(payload: dict):
    records = payload.get("data", [])

    if not records:
        raise HTTPException(
            status_code=400,
            detail="No vendor data provided."
        )
    df = pd.DataFrame(records)
    df_scored = score_dataframe(df)
    stats = get_summary_stats(df_scored)

    return {
        "message": "Scoring complete",
        "stats": stats,
        "data": df_scored.to_dict(orient="records")
    }