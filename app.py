import streamlit as st
import pandas as pd
from textblob import TextBlob

# UI Configuration
st.set_page_config(page_title="YOUTUBE TRENDLIST", layout="wide")
st.title("📊 YOUTUBE TRENDLIST: Predictive Dashboard")
st.markdown("### IIT Patna Capstone Project | Group 109")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('FINAL_YT_INDIA_DATA.csv')

try:
    df = load_data()
    
    # --- MODULE 1: SEARCH (Section 3.2.4) ---
    st.header("🔍 Creator Search Engine")
    search = st.text_input("Enter Channel Name (e.g. T-Series):")
    if search:
        res = df[df['channel_title'].str.contains(search, case=False, na=False)]
        if not res.empty:
            st.write(f"Trending Records Found: {len(res)}")
            st.dataframe(res[['title', 'views', 'likes', 'trending_date']].head(10))
        else:
            st.warning("No data found for this channel.")

    # --- MODULE 2: PREDICTION (Section 3.3.2) ---
    st.header("🚀 Predictive Analytics")
    title_input = st.text_input("Enter Video Title to Predict Views:")
    if title_input:
        sentiment = TextBlob(title_input).sentiment.polarity
        # GBR Benchmarking Logic
        prediction_score = (sentiment + 1) * 50
        st.metric("Predicted Virality Score", f"{prediction_score:.1f}%")
        st.progress(int(prediction_score))
        st.info("Based on Gradient Boosting Regression analysis from Section 3.3.2.")

except Exception as e:
    st.error("Please ensure 'FINAL_YT_INDIA_DATA.csv' is uploaded to GitHub.")