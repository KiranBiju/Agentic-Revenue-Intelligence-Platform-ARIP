import streamlit as st
import pandas as pd

def render_leads(leads):
    st.dataframe(pd.DataFrame(leads))