"""
    Graphical User Interface module

    This module contains launches a Streamlit web app to browse through the scraped job offers
    
"""

import streamlit as st
import pandas as pd

from src.scraper import scrape_jobs


# -------------------------------
#  STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="APEC Job Scraper", layout="wide")
st.title("💼 APEC Job Scraper (Data science in Paris)")

# Creating thte session_state variable to store fetched job offers
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# Button to launch scraping
if st.button("🚀 Launch Scraping"):
    with st.spinner("Scraping APEC job offers… please wait (10–15 s)…"):
        st.session_state.jobs = scrape_jobs()
    st.success(f"✅ Scraping finished – {len(st.session_state.jobs)} offers found on the first page!")

# Display the table of jobs
if st.session_state.jobs:
    df = pd.DataFrame(st.session_state.jobs).drop("pub_date", axis=1)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Click **Launch Scraping** to retrieve job offers.")
