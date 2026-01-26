import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Page config MUST be first
st.set_page_config(
    page_title="💎 Game Boy Scout",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT.parent / "token_logs.csv"
MOMENTUM_FILE = ROOT.parent / "momentum_logs.csv"

# Game Boy Color CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    /* Game Boy Shell */
    .main {
        background: linear-gradient(135deg, #6b4d9e 0%, #4a3570 100%);
        font-family: 'Press Start 2P', monospace;
    }
    
    /* Game Boy Screen */
    .stApp {
        background-color: #0f380f;
        color: #9bbc0f;
    }
    
    /* Headers - Game Boy Green */
    h1, h2, h3 {
        color: #9bbc0f !important;
        font-family: 'Press Start 2P', monospace !important;
        text-shadow: 2px 2px #0f380f;
        font-size: 16px !important;
        line-height: 1.8 !important;
    }
    
    h1 { font-size: 20px !important; }
    
    /* Pixel borders */
    .token-card {
        background-color: #306230;
        border: 4px solid #0f380f;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        line-height: 1.8;
        color: #9bbc0f;
        box-shadow: 4px 4px 0px #0f380f;
    }
    
    /* Alert box - darker green */
    .alert-card {
        background-color: #0f380f;
        border: 4px solid #9bbc0f;
        padding: 12px;
        margin: 8px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
        line-height: 1.6;
        color: #8bac0f;
    }
    
    /* Metric boxes */
    .stMetric {
        background-color: #306230 !important;
        border: 3px solid #0f380f !important;
        padding: 10px !important;
        font-family: 'Press Start 2P', monospace !important;
        color: #9bbc0f !important;
    }
    
    .stMetric label {
        color: #8bac0f !important;
        font-size: 8px !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #9bbc0f !important;
        font-size: 18px !important;
    }
    
    /* Sidebar - Game Boy Color purple */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6b4d9e 0%, #4a3570 100%);
        border-right: 5px solid #0f380f;
    }
    
    section[data-testid="stSidebar"] * {
        color: #9bbc0f !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }
    
    /* Buttons - Game Boy style */
    .stButton button {
        background-color: #8bac0f !important;
        color: #0f380f !important;
        border: 3px solid #0f380f !important;
        border-radius: 15px !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 10px !important;
        padding: 10px 20px !important;
        box-shadow: 3px 3px 0px #0f380f !important;
    }
    
    .stButton button:hover {
        background-color: #9bbc0f !important;
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #0f380f !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input {
        background-color: #306230 !important;
        color: #9bbc0f !important;
        border: 2px solid #0f380f !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }
    
    /* Sliders */
    .stSlider {
        font-family: 'Press Start 2P', monospace !important;
    }
    
    /* Divider */
    hr {
        border-color: #0f380f !important;
        border-width: 2px !important;
    }
    
    /* Loading animation - pixelated */
    .stSpinner > div {
        border-color: #9bbc0f !important;
    }
    
    /* Dataframe */
    .dataframe {
        font-family: 'Press Start 2P', monospace !important;
        font-size: 8px !important;
        background-color: #306230 !important;
        color: #9bbc0f !important;
    }
    
    /* Status text */
    .status-text {
        background-color: #0f380f;
        border: 3px solid #306230;
        padding: 10px;
        text-align: center;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        color: #8bac0f;
        margin: 20px 0;
    }
    
    /* Blink animation for alerts */
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.5; }
    }
    
    .blink {
        animation: blink 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Title with Game Boy aesthetic
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #306230; border: 5px solid #0f380f; margin-bottom: 20px;'>
    <h1>🎮 GAME BOY SCOUT 💎</h1>
    <p style='color: #8bac0f; font-size: 10px; font-family: "Press Start 2P", monospace;'>
        SOLANA HIDDEN GEM SCANNER
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Game Boy Controls
with st.sidebar:
    st.markdown("### 🕹️ CONTROLS")
    st.markdown("---")
    
    auto_refresh = st.slider("REFRESH (SEC)", 5, 60, 15)
    
    st.markdown("---")
    st.markdown("### 🎯 FILTERS")
    
    min_score = st.slider("MIN SCORE", 0, 10, 6)
    min_holders = st.number_input("MIN HOLDERS", 0, 1000, 68)
    
    st.markdown("---")
    
    require_momentum = st.checkbox("MOMENTUM > +20%", False)
    show_today_only = st.checkbox("TODAY ONLY", False)
    
    st.markdown("---")
    
    search_symbol = st.text_input("SEARCH", "").upper()
    
    st.markdown("---")
    
    chains = st.multiselect(
        "CHAINS",
        ["solana", "ethereum", "bsc"],
        default=["solana"]
    )
    
    st.markdown("---")
    st.markdown("### ⚡ STATUS")
    st.markdown(f"<div class='blink'>● SCANNING</div>", unsafe_allow_html=True)

# Load data
@st.cache_data(ttl=auto_refresh)
def load_token_data():
    if not LOG_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(LOG_FILE)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

@st.cache_data(ttl=auto_refresh)
def load_momentum_data():
    if not MOMENTUM_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(MOMENTUM_FILE)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

tokens_df = load_token_data()
momentum_df = load_momentum_data()

# Apply filters
if not tokens_df.empty:
    if 'score' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['score'] >= min_score]
    
    if 'holders' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['holders'] >= min_holders]
    
    if search_symbol and 'symbol' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['symbol'].str.contains(search_symbol, case=False, na=False)]
    
    if 'chain' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['chain'].isin(chains)]
    
    if show_today_only and 'timestamp' in tokens_df.columns:
        today = datetime.now(timezone.utc).date()
        tokens_df = tokens_df[tokens_df['timestamp'].dt.date == today]

# Game Boy Screen Stats
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("SCANNED", len(tokens_df) if not tokens_df.empty else 0)

with col2:
    if not tokens_df.empty and 'holders' in tokens_df.columns:
        avg_holders = int(tokens_df['holders'].mean())
        st.metric("AVG HOLDERS", f"{avg_holders}")
    else:
        st.metric("AVG HOLDERS", "N/A")

with col3:
    if not tokens_df.empty and 'score' in tokens_df.columns:
        top1_pct = (tokens_df['score'] >= 8).sum() / len(tokens_df) * 100
        st.metric("TOP 1%", f"{top1_pct:.0f}%")
    else:
        st.metric("TOP 1%", "N/A")

with col4:
    if not tokens_df.empty and 'mint_safe' in tokens_df.columns:
        mint_safe_pct = tokens_df['mint_safe'].sum() / len(tokens_df) * 100
        st.metric("MINT SAFE", f"{mint_safe_pct:.0f}%")
    else:
        st.metric("MINT SAFE", "N/A")

with col5:
    if not tokens_df.empty and 'score' in tokens_df.columns:
        high_scores = (tokens_df['score'] >= 7).sum()
        st.metric("HIGH SCORE", high_scores)
    else:
        st.metric("HIGH SCORE", 0)

st.markdown("---")

# Main content area
if tokens_df.empty:
    st.markdown("""
    <div class='status-text'>
        <p>⏳ LOADING...</p>
        <p style='margin-top: 10px;'>NO TOKENS YET</p>
        <p style='margin-top: 10px;'>KEEP BOT RUNNING</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Top Tokens Section
    st.markdown("## 🏆 TOP TOKENS")
    
    # Sort by score
    if 'score' in tokens_df.columns:
        display_df = tokens_df.sort_values('score', ascending=False).head(10)
    else:
        display_df = tokens_df.head(10)
    
    # Display tokens as Game Boy cards
    for idx, row in display_df.iterrows():
        symbol = row.get('symbol', 'UNKNOWN')
        score = row.get('score', 0)
        liquidity = row.get('liquidity_usd', 0)
        holders = row.get('holders', 0)
        age_min = row.get('age_minutes', 0)
        price = row.get('price_usd', 0)
        address = row.get('address', '')
        
        # Score indicator
        if score >= 8:
            score_emoji = "⭐⭐⭐"
        elif score >= 7:
            score_emoji = "⭐⭐"
        elif score >= 6:
            score_emoji = "⭐"
        else:
            score_emoji = "•"
        
        st.markdown(f"""
        <div class='token-card'>
            <p>{score_emoji} ${symbol}</p>
            <p>SCORE: {score:.1f}/10</p>
            <p>LIQ: ${liquidity:,.0f}</p>
            <p>HOLDERS: {holders}</p>
            <p>AGE: {age_min:.0f}M</p>
            <p>PRICE: ${price:.8f}</p>
            <p style='font-size: 7px; margin-top: 8px;'>{address[:16]}...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add link buttons
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if address:
                st.link_button("📊 DEX", f"https://dexscreener.com/solana/{address}", use_container_width=True)
        with col_b:
            st.link_button("🦎 GECKO", f"https://www.coingecko.com/en/coins/{symbol.lower()}", use_container_width=True)
        with col_c:
            st.link_button("𝕏 TWITTER", f"https://twitter.com/search?q=${symbol}", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

# Momentum Section
st.markdown("---")
st.markdown("## 📈 MOMENTUM")

if not momentum_df.empty:
    st.markdown("""
    <div class='status-text'>
        MOMENTUM DATA ACTIVE
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='alert-card'>
        NO MOMENTUM DATA YET
    </div>
    """, unsafe_allow_html=True)

# Alerts Log
st.markdown("---")
st.markdown("## 🔔 ALERTS LOG")

if not tokens_df.empty:
    st.markdown(f"""
    <div class='alert-card'>
        LATEST: ${tokens_df.iloc[0].get('symbol', 'N/A')} - SCORE {tokens_df.iloc[0].get('score', 0):.1f}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='alert-card'>
        NO ALERTS YET
        <br>KEEP BOT RUNNING
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 15px; font-size: 8px; color: #8bac0f;'>
    <p>AUTO-REFRESH: EVERY {0}S</p>
    <p>DATA BY COINGECKO</p>
    <p style='margin-top: 10px;'>🎮 GAME BOY SCOUT V1.0 💎</p>
</div>
""".format(auto_refresh), unsafe_allow_html=True)

# Auto-refresh
import time
time.sleep(auto_refresh)
st.rerun()
