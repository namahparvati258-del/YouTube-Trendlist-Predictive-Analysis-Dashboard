import streamlit as st
import pandas as pd
from textblob import TextBlob

# UI Configuration
st.set_page_config(page_title="YOUTUBE TRENDLIST", layout="wide")
st.title("📊 YOUTUBE TRENDLIST: Advanced Predictive Dashboard")
st.markdown("### IIT Patna Capstone Project | Group 109 - Rakesh Kumawat")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('FINAL_YT_INDIA_DATA.csv')
    df['trending_date'] = pd.to_datetime(df['trending_date']).dt.date
    return df

try:
    df = load_data()
    
    # --- MODULE 1: SEARCH (Section 3.2.4) ---
    st.header("🔍 Creator Search Engine")
    search = st.text_input("Enter Channel Name (e.g. T-Series, Zee Music):")
    if search:
        res = df[df['channel_title'].str.contains(search, case=False, na=False)]
        if not res.empty:
            st.write(f"Showing top results for: {search}")
            # FIX: Indexing starts from 1, 2, 3...
            display_df = res[['title', 'views', 'likes', 'trending_date']].head(10).reset_index(drop=True)
            display_df.index += 1 
            st.table(display_df)
        else:
            st.warning("No data found for this channel.")

    # --- MODULE 2: VIRALITY SIMULATOR (Section 3.3.2) ---
    st.divider()
    st.header("🚀 Advanced Virality Simulator")
    st.info("Set the parameters of your video title to predict its trending potential.")

    col1, col2 = st.columns(2)
    with col1:
        # Title word count slider
        title_length = st.slider("Select Title Word Count", 1, 50, 10)
        # Sentiment selection
        sentiment_choice = st.select_slider("Tone of the Title", options=["Negative", "Neutral", "Positive"], value="Positive")
    
    with col2:
        # Capital words input
        caps_count = st.number_input("Number of CAPITALIZED Words", 0, 20, 2)
        # Special characters
        has_symbol = st.checkbox("Include Emojis/Exclamation marks?", value=True)

    # Logic based on our GBR Benchmarks
    virality_score = 40 # Base score
    if sentiment_choice == "Positive": virality_score += 20
    if 7 <= title_length <= 15: virality_score += 15
    if caps_count >= 2: virality_score += 15
    if has_symbol: virality_score += 10
    
    final_result = min(virality_score, 100)

    st.subheader(f"Projected Virality Score: {final_result}%")
    st.progress(final_result / 100)
    
    if final_result > 70:
        st.success("🔥 This title has high trending potential in the Indian market!")
    else:
        st.warning("⚠️ Consider optimizing the title length or emotional tone.")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")