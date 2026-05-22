import pandas as pd
import streamlit as st
from utils.api import run_campaign
from utils.sample_data import sample_leads
from components.metrics_card import render_metrics
from components.lead_table import render_leads
from components.analytics import render_analytics
from components.campaign_results import render_results

st.set_page_config(
    page_title="ARIP",
    layout="wide"
)

st.title(
    "ARIP — Agentic Revenue Intelligence Platform"
)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    leads = df.to_dict(
        orient="records"
    )

else:

    leads = sample_leads

st.subheader("Lead Preview")

render_leads(leads)

st.info(f"Loaded Leads: {len(leads)}")

if st.button("Run Campaign"):

    payload = {
        "leads": leads
    }

    with st.spinner("Running ARIP..."):

        result = run_campaign(payload)

    if result.get("detail"):

        st.error("Campaign execution failed.")

        st.stop()

    if result.get("status") == "failed":

        st.error(
            result.get(
                "error",
                "Campaign failed"
            )
        )

        st.stop()

    st.success("Campaign Completed")

    render_metrics(result)

    st.subheader("Ranked Leads")

    ranked_leads = result.get(
        "ranked_leads",
        []
    )

    render_analytics(
        ranked_leads
    )

    st.subheader("Execution Results")

    render_results(
        result.get(
            "results",
            result.get(
                "results",
                []
            )
        )
    )

    st.subheader("Logs")

    logs = result.get(
        "logs",
        []
    )

    if logs:

        for log in logs:
            st.code(log)

    else:

        st.warning(
            "No logs available."
        )