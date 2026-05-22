import streamlit as st


def render_metrics(result):

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Leads",
        result.get("total_leads", 0)
    )

    col2.metric(
        "Selected Leads",
        result.get("selected", 0)
    )

    col3.metric(
        "Processed",
        result.get("processed", 0)
    )

    col4.metric(
        "Top Score",
        round(result.get("top_score", 0), 3)
    )