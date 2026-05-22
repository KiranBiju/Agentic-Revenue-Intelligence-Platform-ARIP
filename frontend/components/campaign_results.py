import streamlit as st

def render_results(results):
    for item in results:
        st.json(item)