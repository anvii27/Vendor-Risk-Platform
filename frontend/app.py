import streamlit as st
import requests
import pandas as pd

BACKEND = "http://localhost:8000"

st.set_page_config(
    page_title="Vendor Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Vendor Risk Intelligence Platform")
st.caption("Upload vendor assessment data to score risk and detect anomalies.")

try:
    health = requests.get(f"{BACKEND}/health", timeout=3)
    if health.status_code == 200:
        st.success("Backend connected", icon="✅")
    else:
        st.error("Backend error")
except Exception:
    st.error("Backend offline. Run: uvicorn main:app --reload --port 8000", icon="🔴")

st.divider()

st.subheader("Upload Vendor Data")

file = st.file_uploader("Choose a CSV file", type=["csv"])

if file:
    with st.spinner("Uploading..."):
        response = requests.post(
            f"{BACKEND}/upload",
            files={"file": (file.name, file.getvalue(), "text/csv")},
        )

    if response.status_code == 200:
        result = response.json()
        st.session_state["raw_data"] = result["data"]
        st.success(f"Loaded {result['rows']} vendors")
        st.dataframe(pd.DataFrame(result["data"]).head(10), use_container_width=True)
    else:
        st.error(response.json().get("detail", "Upload failed"))

st.divider()

st.subheader("Calculate Risk Scores")

if "raw_data" in st.session_state:
    if st.button("⚡ Run Risk Scoring", type="primary"):
        with st.spinner("Scoring vendors..."):
            response = requests.post(
                f"{BACKEND}/score",
                json={"data": st.session_state["raw_data"]},
            )

        if response.status_code == 200:
            result = response.json()
            st.session_state["scored_data"] = result["data"]
            st.session_state["stats"] = result["stats"]
            st.success("Scoring complete!")
        else:
            st.error(response.json().get("detail", "Scoring failed"))

    if "scored_data" in st.session_state:
        stats = st.session_state["stats"]

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Vendors", stats["total"])
        col2.metric("🔴 Critical", stats["critical"])
        col3.metric("🟠 High", stats["high"])
        col4.metric("🟡 Medium", stats["medium"])
        col5.metric("🟢 Low", stats["low"])

    df_scored = pd.DataFrame(st.session_state["scored_data"])

    tier_filter = st.multiselect(
        "Filter by risk tier",
        options=["Critical", "High", "Medium", "Low"],
        default=["Critical", "High"],
    )

    filtered = df_scored[df_scored["Calculated_Risk_Level"].isin(tier_filter)] if tier_filter else df_scored

    st.dataframe(
        filtered[["Vendor_Name", "Risk_Score", "Calculated_Risk_Level"]]
        .sort_values("Risk_Score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

st.divider()

st.subheader("Risk Distribution")

import plotly.express as px

tier_counts = df_scored["Calculated_Risk_Level"].value_counts().reset_index()
tier_counts.columns = ["Tier", "Count"]

colors = {
        "Critical": "#ef4444",
        "High": "#f97316",
        "Medium": "#eab308",
        "Low": "#22c55e",
    }

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
        fig_pie = px.pie(
            tier_counts,
            names="Tier",
            values="Count",
            color="Tier",
            color_discrete_map=colors,
            title="Vendors by Risk Tier",
            hole=0.4,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
        top20 = df_scored.sort_values("Risk_Score", ascending=False).head(20)
        fig_bar = px.bar(
            top20,
            x="Vendor_Name",
            y="Risk_Score",
            color="Calculated_Risk_Level",
            color_discrete_map=colors,
            title="Top 20 Riskiest Vendors",
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.subheader("Vendor Deep Dive")

vendor_name = st.selectbox(
        "Select a vendor to inspect",
        options=df_scored.sort_values("Risk_Score", ascending=False)["Vendor_Name"].tolist(),
    )

vendor = df_scored[df_scored["Vendor_Name"] == vendor_name].iloc[0].to_dict()

tier = vendor["Calculated_Risk_Level"]
score = vendor["Risk_Score"]
color = colors.get(tier, "#94a3b8")

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
m1.metric("Critical Findings", vendor.get("Critical_Findings", "—"))
m2.metric("High Findings", vendor.get("High_Findings", "—"))
m3.metric("Security Incidents", vendor.get("Security_Incidents", "—"))
m4.metric("Days Overdue", vendor.get("Mitigation_Overdue_Days", "—"))

m5, m6, m7, m8 = st.columns(4)
m5.metric("Compliance Score", f"{vendor.get('Compliance_Score', '—')}%")
m6.metric("MFA Enabled", vendor.get("MFA_Enabled", "—"))
m7.metric("Data Access", vendor.get("Data_Access_Level", "—"))
m8.metric("SLA Breaches", vendor.get("SLA_Breaches", "—"))