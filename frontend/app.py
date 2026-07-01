import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import sys
import os

BACKEND = "http://localhost:8000"

sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

COLORS = {
    "Critical": "#ef4444",
    "High":     "#f97316",
    "Medium":   "#eab308",
    "Low":      "#22c55e",
}

st.set_page_config(
    page_title="Vendor Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🛡️ Vendor Risk")
    st.caption("Third-Party Risk Intelligence Platform")
    st.divider()

    try:
        health = requests.get(f"{BACKEND}/health", timeout=3)
        st.success("API connected")
    except Exception:
        st.error("API offline")
        st.caption("Run: uvicorn main:app --reload --port 8000")

    st.divider()

    st.subheader("Upload Data")
    file = st.file_uploader("Replace with your CSV", type=["csv"])

    if file:
        with st.spinner("Uploading..."):
            response = requests.post(
                f"{BACKEND}/upload",
                files={"file": (file.name, file.getvalue(), "text/csv")},
            )
        if response.status_code == 200:
            result = response.json()
            st.session_state["raw_data"] = result["data"]
            st.session_state.pop("scored_data", None)
            st.session_state.pop("stats", None)
            st.success(f"Loaded {result['rows']} vendors")
        else:
            st.error(response.json().get("detail", "Upload failed"))

    st.divider()
    st.caption("Filters")

    tier_filter = st.multiselect(
        "Risk Tier",
        options=["Critical", "High", "Medium", "Low"],
    )

    selected_industry = "All"
    selected_region = "All"

    if "scored_data" in st.session_state:
        df_all = pd.DataFrame(st.session_state["scored_data"])

        industries = ["All"] + sorted(df_all["Vendor_Category"].dropna().unique().tolist())
        selected_industry = st.selectbox("Vendor Category", industries)

        regions = ["All"] + sorted(df_all["Region"].dropna().unique().tolist())
        selected_region = st.selectbox("Region", regions)


# ── Auto-load sample data on first run ───────────────────────────────────────
def load_sample_data():
    sample_path = os.path.join(os.path.dirname(__file__), "../data/vendors.csv")
    if not os.path.exists(sample_path):
        return False
    try:
        df = pd.read_csv(sample_path)
        response = requests.post(
            f"{BACKEND}/score",
            json={"data": df.to_dict(orient="records")},
        )
        if response.status_code == 200:
            result = response.json()
            st.session_state["scored_data"] = result["data"]
            st.session_state["stats"]       = result["stats"]
            st.session_state["raw_data"]    = df.to_dict(orient="records")
            return True
    except Exception:
        return False
    return False


if "scored_data" not in st.session_state:
    with st.spinner("Loading sample dataset..."):
        load_sample_data()

if "raw_data" in st.session_state and "scored_data" not in st.session_state:
    with st.spinner("Scoring vendors..."):
        response = requests.post(
            f"{BACKEND}/score",
            json={"data": st.session_state["raw_data"]},
        )
    if response.status_code == 200:
        result = response.json()
        st.session_state["scored_data"] = result["data"]
        st.session_state["stats"]       = result["stats"]


# ── Main dashboard ────────────────────────────────────────────────────────────
st.title("🛡️ Vendor Risk Intelligence Dashboard")

if "scored_data" not in st.session_state:
    st.warning("Could not load data. Make sure the backend is running.")
    st.stop()

df = pd.DataFrame(st.session_state["scored_data"])
stats = st.session_state["stats"]

# Apply filters
df_filtered = df[df["Calculated_Risk_Level"].isin(tier_filter)] if tier_filter else df

if selected_industry != "All":
    df_filtered = df_filtered[df_filtered["Vendor_Category"] == selected_industry]

if selected_region != "All":
    df_filtered = df_filtered[df_filtered["Region"] == selected_region]


# ── KPI row ───────────────────────────────────────────────────────────────────
st.subheader("Overview")

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Vendors",  stats["total"])
k2.metric("🔴 Critical",    stats["critical"])
k3.metric("🟠 High",        stats["high"])
k4.metric("🟡 Medium",      stats["medium"])
k5.metric("🟢 Low",         stats["low"])
k6.metric("Avg Risk Score", stats["avg_score"])

st.divider()

# ── Charts row 1 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    tier_counts = df_filtered["Calculated_Risk_Level"].value_counts().reset_index()
    tier_counts.columns = ["Tier", "Count"]
    fig_pie = px.pie(
        tier_counts,
        names="Tier",
        values="Count",
        color="Tier",
        color_discrete_map=COLORS,
        title="Risk Tier Distribution",
        hole=0.4,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    top20 = df_filtered.sort_values("Risk_Score", ascending=False).head(20)
    fig_bar = px.bar(
        top20,
        x="Vendor_Name",
        y="Risk_Score",
        color="Calculated_Risk_Level",
        color_discrete_map=COLORS,
        title="Top 20 Riskiest Vendors",
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Charts row 2 ──────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    category_risk = df_filtered.groupby("Vendor_Category")["Risk_Score"].mean().reset_index()
    category_risk.columns = ["Category", "Avg Risk Score"]
    category_risk = category_risk.sort_values("Avg Risk Score", ascending=False)
    fig_cat = px.bar(
        category_risk,
        x="Category",
        y="Avg Risk Score",
        title="Avg Risk Score by Vendor Category",
        color="Avg Risk Score",
        color_continuous_scale="Reds",
    )
    fig_cat.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_cat, use_container_width=True)

with col4:
    region_risk = df_filtered.groupby("Region")["Risk_Score"].mean().reset_index()
    region_risk.columns = ["Region", "Avg Risk Score"]
    fig_region = px.bar(
        region_risk,
        x="Region",
        y="Avg Risk Score",
        title="Avg Risk Score by Region",
        color="Avg Risk Score",
        color_continuous_scale="Oranges",
    )
    st.plotly_chart(fig_region, use_container_width=True)

st.divider()

# ── Immediate action section ──────────────────────────────────────────────────
critical_vendors = df[
    (df["Calculated_Risk_Level"] == "Critical")
].sort_values("Risk_Score", ascending=False).head(5)

if len(critical_vendors) > 0:
    st.subheader("Vendors Requiring Immediate Action")
    st.caption("Top 5 Critical risk vendors — escalate immediately")

    for _, row in critical_vendors.iterrows():
        col_name, col_score, col_findings, col_incidents, col_days = st.columns([3, 1, 1, 1, 1])

        col_name.markdown(f"**{row['Vendor_Name']}**  \n{row['Vendor_Category']} — {row['Region']}")
        col_score.metric("Risk Score", row["Risk_Score"])
        col_findings.metric("Critical Findings", row["Critical_Findings"])
        col_incidents.metric("Incidents", row["Security_Incidents"])
        col_days.metric("Days Overdue", row["Mitigation_Overdue_Days"])

        st.divider()
        

# ── Vendor table ──────────────────────────────────────────────────────────────
st.subheader("Vendor Risk Table")

search = st.text_input("Search vendor name")
if search:
    df_filtered = df_filtered[
        df_filtered["Vendor_Name"].str.contains(search, case=False, na=False)
    ]

display_cols = [c for c in [
    "Vendor_Name", "Vendor_Category", "Region",
    "Risk_Score", "Calculated_Risk_Level",
    "Critical_Findings", "Security_Incidents",
    "Compliance_Score", "MFA_Enabled",
] if c in df_filtered.columns]

st.dataframe(
    df_filtered[display_cols].sort_values("Risk_Score", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "⬇️ Download Results CSV",
    data=df_filtered.to_csv(index=False),
    file_name="vendor_risk_results.csv",
    mime="text/csv",
)

st.divider()

# ── Vendor detail ─────────────────────────────────────────────────────────────
st.subheader("Vendor Deep Dive")

vendor_name = st.selectbox(
    "Select a vendor",
    options=df.sort_values("Risk_Score", ascending=False)["Vendor_Name"].tolist(),
)

vendor = df[df["Vendor_Name"] == vendor_name].iloc[0].to_dict()
tier   = vendor["Calculated_Risk_Level"]
score  = vendor["Risk_Score"]
color  = COLORS.get(tier, "#94a3b8")

st.markdown(
    f"""
    <div style="background:{color}20;border-left:5px solid {color};
                padding:16px;border-radius:6px;margin-bottom:16px;">
        <h3 style="margin:0;color:{color};">{vendor_name}</h3>
        <p style="margin:4px 0 0;font-size:1.1rem;">
            Risk Score: <strong>{score}</strong> &nbsp;|&nbsp;
            Tier: <strong>{tier}</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Critical Findings",  vendor.get("Critical_Findings", "—"))
m2.metric("High Findings",      vendor.get("High_Findings", "—"))
m3.metric("Security Incidents", vendor.get("Security_Incidents", "—"))
m4.metric("Days Overdue",       vendor.get("Mitigation_Overdue_Days", "—"))

m5, m6, m7, m8 = st.columns(4)
m5.metric("Compliance Score",  f"{vendor.get('Compliance_Score', '—')}%")
m6.metric("MFA Enabled",       vendor.get("MFA_Enabled", "—"))
m7.metric("Data Access",       vendor.get("Data_Access_Level", "—"))
m8.metric("SLA Breaches",      vendor.get("SLA_Breaches", "—"))

st.divider()
st.subheader("Summary")

if st.button("Generate AI Summary", type="primary"):
    with st.spinner("Generating summary..."):
        response = requests.post(
            f"{BACKEND}/summary",
            json={"vendor": vendor},
        )
    if response.status_code == 200:
        summary_text = response.json()["summary"]
        st.info(summary_text)
    else:
        st.error("Summary generation failed.")