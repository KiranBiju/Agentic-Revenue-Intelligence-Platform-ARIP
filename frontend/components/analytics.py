import streamlit as st
import pandas as pd
import plotly.express as px


def render_analytics(ranked_leads):

    st.subheader("Lead Analytics")

    if not ranked_leads:
        st.warning("No ranked leads available.")
        return
    
    if not isinstance(ranked_leads, list):
        st.error("ranked_leads is not a list")
        st.write(ranked_leads)
        return

    df = pd.DataFrame(ranked_leads)
    
    st.write("Available Columns:")
    st.write(df.columns.tolist())

    required_columns = ["name", "score"]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        st.error(
            f"Missing analytics columns: {missing}"
        )

        st.write(df)

        return

    fig = px.bar(
        df,
        x="name",
        y="score",
        title="Lead Priority Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.dataframe(df)