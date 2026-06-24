import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

import pandas as pd
from risk_engine import score_dataframe, get_summary_stats

df = pd.read_csv("../data/vendors.csv")
df_scored = score_dataframe(df)

print(df_scored["Calculated_Risk_Level"].value_counts())
print(df_scored[["Vendor_ID", "Vendor_Name", "Risk_Score", "Calculated_Risk_Level"]].head())