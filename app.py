import streamlit as st
import pandas as pd

# UI Configuration - Professional Look
st.set_page_config(page_title="YOUTUBE TRENDLIST", layout="wide")

# Custom Styling for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("📊 YOUTUBE TRENDLIST: Advanced Predictive Dashboard")
st.markdown("### IIT Patna Capstone Project | Group 109 ")

# Load Data
@st.cache_data
def load_data():
    try:
        # Loading your specific dataset
        df = pd.read_csv('FINAL_YT_INDIA_DATA.csv')
        df['trending_date'] = pd.to_datetime(df['trending_date']).dt.date
        return df
    except:
        return None

df = load_data()

if df is not None:
    # --- MODULE 1: SEARCH ENGINE ---
    st.header("🔍 Creator Search Engine")
    search = st.text_input("Enter Channel Name:", key="search_bar", placeholder="e.g., T-Series, CarryMinati")
    if search:
        res = df[df['channel_title'].str.contains(search, case=False, na=False)]
        if not res.empty:
            st.success(f"Top 10 Trending Videos for **{search}**")
            display_df = res[['title', 'views', 'likes', 'trending_date']].head(10).reset_index(drop=True)
            display_df.index += 1 
            st.table(display_df)
        else:
            st.warning("No data found for this channel.")

    # --- MODULE 2: VIRALITY SIMULATOR ---
    st.divider()
    st.header("🚀 Virality Simulator (V3.0)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Metadata Strategy")
        title_length = st.slider("Title Word Count", 1, 60, 12)
        tone_choice = st.radio("Title Tone", ["Negative", "Neutral", "Positive"], index=2, horizontal=True)
        video_duration = st.slider("Video Duration (Minutes)", 1, 60, 10)
    
    with col2:
        st.subheader("🔥 Engagement Signals")
        caps_count = st.number_input("CAPS words in Title", 0, 30, 2)
        engagement = st.radio("Audience Interaction", ["Low", "Medium", "High"], index=1, horizontal=True)
        has_symbol = st.checkbox("Include Emojis/Symbols?", value=True)

    # --- ENHANCED LOGIC ---
    score = 20  # Base
    
    if 7 <= title_length <= 15: score += 15
    elif title_length > 35: score -= 10
    
    if tone_choice == "Positive": score += 15
    elif tone_choice == "Negative": score += 12
    else: score += 5
    
    if 8 <= video_duration <= 18: score += 25  # Sweet spot for Watch Time
    else: score += 10
        
    if engagement == "High": score += 20
    elif engagement == "Medium": score += 10
    
    score += (caps_count * 2) 
    if has_symbol: score += 5

    final_score = max(5, min(score, 100))

    # --- PREMIUM DISPLAY ---
    st.divider()
    m1, m2 = st.columns([1, 2])
    
    with m1:
        st.metric(label="Predicted Success Rate", value=f"{final_score}%")
    
    with m2:
        st.write("### Analysis Verdict:")
        # BALLOONS ONLY AT 95% OR ABOVE
        if final_score >= 95:
            st.success("🏆 **VIRAL MASTERPIECE!** Predicted to hit #1 on Trending.")
            st.balloons() 
        elif final_score > 70:
            st.info("📈 **Highly Competitive.** Video has strong trending potential.")
        else:
            st.warning("⚖️ **Needs Optimization.** Content might struggle against top creators.")

    st.progress(final_score / 100)

else:
    st.error("Dataset not found! Please check 'FINAL_YT_INDIA_DATA.csv' on GitHub.")