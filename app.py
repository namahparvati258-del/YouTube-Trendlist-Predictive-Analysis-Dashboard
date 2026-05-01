import streamlit as st
import pandas as pd
from textblob import TextBlob

# UI Configuration
st.set_page_config(page_title="YOUTUBE TRENDLIST", layout="wide")
st.title("📊 YOUTUBE TRENDLIST: Advanced Predictive Dashboard")
st.markdown("### IIT Patna Capstone Project | Group 109 ")

# Load Data
@st.cache_data
def load_data():
    # Aapki file ka name check kar lena agar CSV upload ho gayi hai
    df = pd.read_csv('FINAL_YT_INDIA_DATA.csv')
    df['trending_date'] = pd.to_datetime(df['trending_date']).dt.date
    return df

try:
    df = load_data()
    
    # --- MODULE 1: SEARCH ---
    st.header("🔍 Creator Search Engine")
    search = st.text_input("Enter Channel Name:")
    if search:
        res = df[df['channel_title'].str.contains(search, case=False, na=False)]
        if not res.empty:
            display_df = res[['title', 'views', 'likes', 'trending_date']].head(10).reset_index(drop=True)
            display_df.index += 1 
            st.table(display_df)
        else:
            st.warning("No data found.")

    # --- MODULE 2: DYNAMIC VIRALITY SIMULATOR ---
    st.divider()
    st.header("🚀 Advanced Virality Simulator")
    st.info("Har parameter ko badal kar dekhiye, score turant change hoga.")

    col1, col2 = st.columns(2)
    with col1:
        title_length = st.slider("Select Title Word Count", 1, 60, 15)
        sentiment_choice = st.select_slider("Tone of the Title", options=["Negative", "Neutral", "Positive"], value="Neutral")
    
    with col2:
        caps_count = st.number_input("Number of CAPITALIZED Words", 0, 30, 2)
        has_symbol = st.checkbox("Include Emojis/Symbols?", value=True)

    # --- NEW DYNAMIC LOGIC (Calculates on every move) ---
    score = 30  # Base Score

    # 1. Length Logic (Ideal length for Indian YouTube is 6-12 words)
    if 6 <= title_length <= 15:
        score += 25
    elif title_length > 30:
        score -= 10 # Zyada lamba title score kam karega
    else:
        score += 10

    # 2. Sentiment Logic
    if sentiment_choice == "Positive":
        score += 20
    elif sentiment_choice == "Negative":
        score += 15 # Curiosity create karta hai
    else:
        score += 5 # Neutral ka score sabse kam

    # 3. Caps Logic (Per word bonus)
    score += (caps_count * 3) # Har ek capital word par 3% badhega

    # 4. Symbol Logic
    if has_symbol:
        score += 10

    # Final Boundary
    final_score = max(5, min(score, 100)) # 5% se 100% ke beech rahega

    # Display Result
    st.subheader(f"Projected Virality Score: {final_score}%")
    
    # Color coding based on score
    if final_score > 80:
        st.success(f"🔥 Exceptional! This combination is highly likely to trend.")
        st.balloons()
    elif final_score > 50:
        st.info(f"⚡ Good Potential. Solid performance expected.")
    else:
        st.warning(f"⚠️ Low Engagement. Try adding more Positive words or Caps.")
        
    st.progress(final_score / 100)

except Exception as e:
    st.error(f"Error: {e}")