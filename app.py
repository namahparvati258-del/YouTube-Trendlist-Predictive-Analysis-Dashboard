import streamlit as st
import pandas as pd

# UI Configuration
st.set_page_config(page_title="YOUTUBE TRENDLIST", layout="wide")
st.title("📊 YOUTUBE TRENDLIST: Advanced Predictive Dashboard")
st.markdown("### IIT Patna Capstone Project | Group 109 ")

# Load Data
@st.cache_data
def load_data():
    try:
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
            display_df = res[['title', 'views', 'likes', 'trending_date']].head(10).reset_index(drop=True)
            display_df.index += 1 
            st.table(display_df)
        else:
            st.warning("No data found for this channel.")

    # --- MODULE 2: MULTI-FACTOR VIRALITY SIMULATOR ---
    st.divider()
    st.header("🚀 Advanced Virality Simulator (Multi-Factor Analysis)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Content Strategy")
        title_length = st.slider("Select Title Word Count", 1, 60, 12, key="slider_length")
        
        # Tone Selection (Radio Buttons)
        tone_choice = st.radio(
            "Title Tone", 
            ["Negative", "Neutral", "Positive"], 
            index=2, 
            horizontal=True,
            key="radio_tone"
        )
        
        video_duration = st.slider("Video Duration (Minutes)", 1, 60, 10, key="video_len")
    
    with col2:
        st.subheader("🔥 Engagement & Formatting")
        caps_count = st.number_input("CAPITALIZED Words in Title", 0, 30, 2, key="input_caps")
        
        # Engagement Selection (Radio Buttons for No-Lag)
        engagement = st.radio(
            "Expected Audience Interaction", 
            ["Low", "Medium", "High"], 
            index=1, 
            horizontal=True,
            key="radio_engagement"
        )
        
        has_symbol = st.checkbox("Include Emojis/Symbols? (🔥, !!, ?)", value=True, key="check_sym")

    # --- UPDATED HYBRID LOGIC ---
    score = 25 
    
    # 1. Title Length
    if 7 <= title_length <= 15: score += 15
    elif title_length > 35: score -= 10
    
    # 2. Tone
    if tone_choice == "Positive": score += 15
    elif tone_choice == "Negative": score += 12
    else: score += 5
    
    # 3. Video Length
    if 8 <= video_duration <= 18: score += 20
    elif 3 <= video_duration < 8: score += 10
    else: score += 5
        
    # 4. Engagement (Strict Categories)
    if engagement == "High": score += 25
    elif engagement == "Medium": score += 15
    else: score += 5
    
    # 5. Caps & Symbols
    score += (caps_count * 3) 
    if has_symbol: score += 5

    final_score = max(5, min(score, 100))

    # --- RESULTS ---
    st.subheader(f"Projected Virality Score: {final_score}%")
    st.progress(final_score / 100)
    
    if final_score >= 90:
        st.success("🔥 LEGENDARY! This combination hits the 'Sweet Spot' of the algorithm.")
        st.balloons() # Strictly at 90%+
    elif final_score > 65:
        st.info("⚡ Strong Potential. Good balance of metadata.")
    else:
        st.warning("⚠️ Optimization Suggested for better reach.")

else:
    st.error("Dataset not found! Please ensure 'FINAL_YT_INDIA_DATA.csv' is in your GitHub.")