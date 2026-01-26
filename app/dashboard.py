import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# Page config MUST be first
st.set_page_config(
    page_title="🔒 Block Boy Security Console",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Paths
ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT.parent / "token_logs.csv"
MOMENTUM_FILE = ROOT.parent / "momentum_logs.csv"


# Block Boy Security Console CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    /* Security Console Shell */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
        font-family: 'Press Start 2P', monospace;
    }
    
    /* Block Boy Screen - Security Green */
    .stApp {
        background-color: #0a0e0a;
        color: #00ff00;
    }
    
    /* Headers - Security Terminal Style */
    h1, h2, h3 {
        color: #00ff00 !important;
        font-family: 'Press Start 2P', monospace !important;
        text-shadow: 0 0 10px #00ff00, 2px 2px #0a0e0a;
        font-size: 16px !important;
        line-height: 1.8 !important;
    }
    
    h1 { 
        font-size: 20px !important;
        text-transform: uppercase;
    }
    
    /* Pixel borders - Security Style */
    .token-card {
        background-color: #1a2f1a;
        border: 4px solid #00ff00;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        line-height: 1.8;
        color: #00ff00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3), 4px 4px 0px #0a0e0a;
    }
    
    /* Alert box - Warning red */
    .alert-card {
        background-color: #2f1a1a;
        border: 4px solid #ff0000;
        padding: 12px;
        margin: 8px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
        line-height: 1.6;
        color: #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
    }
    
    /* Secure box - Blue info */
    .secure-card {
        background-color: #1a1a2f;
        border: 4px solid #00ffff;
        padding: 12px;
        margin: 8px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
        line-height: 1.6;
        color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Metric boxes */
    .stMetric {
        background-color: #1a2f1a !important;
        border: 3px solid #00ff00 !important;
        padding: 10px !important;
        font-family: 'Press Start 2P', monospace !important;
        color: #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }
    
    .stMetric label {
        color: #00cc00 !important;
        font-size: 8px !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 18px !important;
    }
    
    /* Sidebar - Dark Security Console */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
        border-right: 5px solid #00ff00;
    }
    
    section[data-testid="stSidebar"] * {
        color: #00ff00 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }
    
    /* Buttons - Security Terminal style */
    .stButton button {
        background-color: #00cc00 !important;
        color: #0a0e0a !important;
        border: 3px solid #00ff00 !important;
        border-radius: 0px !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 10px !important;
        padding: 10px 20px !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5), 3px 3px 0px #0a0e0a !important;
    }
    
    .stButton button:hover {
        background-color: #00ff00 !important;
        transform: translate(2px, 2px);
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.8), 1px 1px 0px #0a0e0a !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input {
        background-color: #1a2f1a !important;
        color: #00ff00 !important;
        border: 2px solid #00ff00 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }
    
    /* Sliders */
    .stSlider {
        font-family: 'Press Start 2P', monospace !important;
    }
    
    /* Divider */
    hr {
        border-color: #00ff00 !important;
        border-width: 2px !important;
    }
    
    /* Status text */
    .status-text {
        background-color: #0a0e0a;
        border: 3px solid #00ff00;
        padding: 10px;
        text-align: center;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        color: #00cc00;
        margin: 20px 0;
    }
    
    /* Blink animation for security alerts */
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    .blink {
        animation: blink 1s infinite;
    }
    
    /* Scan line effect */
    @keyframes scan {
        0% { top: 0%; }
        100% { top: 100%; }
    }
</style>
""", unsafe_allow_html=True)


# Title with Block Boy Security Console aesthetic
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #1a2f1a; border: 5px solid #00ff00; margin-bottom: 20px; box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);'>
    <h1>🔒 BLOCK BOY SECURITY CONSOLE</h1>
    <p style='color: #00cc00; font-size: 10px; font-family: "Press Start 2P", monospace;'>
        SOLANA BLOCKCHAIN SCANNER V2.0
    </p>
    <p style='color: #00cc00; font-size: 8px; font-family: "Press Start 2P", monospace; margin-top: 10px;'>
        [ CLASSIFIED: SECURITY LEVEL ALPHA ]
    </p>
</div>
""", unsafe_allow_html=True)


# Sidebar - Security Console Controls
with st.sidebar:
    st.markdown("### 🛡️ SECURITY")
    
    # Check if .env exists
    env_path = Path(".env")
    if env_path.exists():
        st.markdown("<div class='secure-card'>API KEYS: SECURED</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-card'>WARNING: NO .ENV</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ CONTROLS")
    auto_refresh = st.slider("SCAN RATE (SEC)", 5, 60, 15)
    
    st.markdown("---")
    st.markdown("### 🎯 FILTERS")
    
    min_score = st.slider("MIN THREAT LVL", 0, 10, 6)
    min_holders = st.number_input("MIN HOLDERS", 0, 1000, 10)
    
    st.markdown("---")
    
    require_momentum = st.checkbox("MOMENTUM > +20%", False)
    show_today_only = st.checkbox("TODAY ONLY", False)
    
    st.markdown("---")
    
    search_symbol = st.text_input("SEARCH TOKEN", "").upper()
    
    st.markdown("---")
    
    chains = st.multiselect(
        "CHAINS",
        ["solana", "ethereum", "bsc"],
        default=["solana"]
    )
    
    st.markdown("---")
    st.markdown("### ⚡ STATUS")
    
    # Bot status indicator
    if not tokens_df.empty if 'tokens_df' in locals() else False:
        st.markdown(f"<div class='blink' style='color: #00ff00;'>● ACTIVE</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color: #ffff00;'>○ STANDBY</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='color: #00cc00; font-size: 8px; margin-top: 10px;'>UPTIME: CONTINUOUS</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #00cc00; font-size: 8px;'>REFRESH: {auto_refresh}S</div>", unsafe_allow_html=True)


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


# Security Console Stats
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
        st.metric("THREAT: HIGH", f"{top1_pct:.0f}%")
    else:
        st.metric("THREAT: HIGH", "N/A")


with col4:
    if not tokens_df.empty and 'mint_safe' in tokens_df.columns:
        mint_safe_pct = tokens_df['mint_safe'].sum() / len(tokens_df) * 100
        st.metric("MINT SECURE", f"{mint_safe_pct:.0f}%")
    else:
        st.metric("MINT SECURE", "N/A")


with col5:
    if not tokens_df.empty and 'score' in tokens_df.columns:
        high_scores = (tokens_df['score'] >= 7).sum()
        st.metric("FLAGGED", high_scores)
    else:
        st.metric("FLAGGED", 0)


st.markdown("---")


# Main content area
if tokens_df.empty:
    st.markdown("""
    <div class='status-text'>
        <p>[ INITIALIZING SCAN ]</p>
        <p style='margin-top: 10px;'>NO TOKENS DETECTED</p>
        <p style='margin-top: 10px;'>AWAITING DATA STREAM</p>
        <p style='margin-top: 15px; font-size: 8px;'>ENSURE BOT IS ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Top Tokens Section
    st.markdown("## 🎯 DETECTED TOKENS")
    
    # Sort by score
    if 'score' in tokens_df.columns:
        display_df = tokens_df.sort_values('score', ascending=False).head(10)
    else:
        display_df = tokens_df.head(10)
    
    # Display tokens as Security Console cards
    for idx, row in display_df.iterrows():
        symbol = row.get('symbol', 'UNKNOWN')
        score = row.get('score', 0)
        liquidity = row.get('liquidity_usd', 0)
        holders = row.get('holders', 0)
        age_min = row.get('age_minutes', 0)
        price = row.get('price_usd', 0)
        address = row.get('address', '')
        
        # Threat level indicator
        if score >= 8:
            threat_level = "[CRITICAL]"
            threat_color = "#ff0000"
        elif score >= 7:
            threat_level = "[HIGH]"
            threat_color = "#ffaa00"
        elif score >= 6:
            threat_level = "[MEDIUM]"
            threat_color = "#ffff00"
        else:
            threat_level = "[LOW]"
            threat_color = "#00ff00"
        
        st.markdown(f"""
        <div class='token-card'>
            <p style='color: {threat_color};'>{threat_level} ${symbol}</p>
            <p>THREAT SCORE: {score:.1f}/10</p>
            <p>LIQUIDITY: ${liquidity:,.0f}</p>
            <p>HOLDERS: {holders}</p>
            <p>AGE: {age_min:.0f}M</p>
            <p>PRICE: ${price:.8f}</p>
            <p style='font-size: 7px; margin-top: 8px; color: #00cc00;'>ADDR: {address[:16]}...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add link buttons
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if address:
                st.link_button("SCAN DEXSCREENER", f"https://dexscreener.com/solana/{address}", use_container_width=True)
        with col_b:
            st.link_button("VERIFY COINGECKO", f"https://www.coingecko.com/en/coins/{symbol.lower()}", use_container_width=True)
        with col_c:
            st.link_button("SOCIAL INTEL", f"https://twitter.com/search?q=${symbol}", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)


# Momentum Section
st.markdown("---")
st.markdown("## 📊 MOMENTUM ANALYSIS")


if not momentum_df.empty:
    st.markdown("""
    <div class='secure-card'>
        MOMENTUM TRACKING: ACTIVE
        <br>ANALYZING PRICE MOVEMENTS
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='status-text'>
        MOMENTUM DATA: PENDING
        <br>AWAITING SUFFICIENT SCANS
    </div>
    """, unsafe_allow_html=True)


# Alerts Log
st.markdown("---")
st.markdown("## 🚨 SECURITY ALERTS")


if not tokens_df.empty:
    latest_token = tokens_df.iloc[0]
    latest_score = latest_token.get('score', 0)
    
    if latest_score >= 8:
        alert_style = "alert-card"
    else:
        alert_style = "secure-card"
    
    st.markdown(f"""
    <div class='{alert_style}'>
        LATEST DETECTION: ${latest_token.get('symbol', 'N/A')}
        <br>THREAT LEVEL: {latest_score:.1f}/10
        <br>TIMESTAMP: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='status-text'>
        NO ALERTS
        <br>SYSTEM MONITORING
    </div>
    """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 15px; font-size: 8px; color: #00cc00;'>
    <p>AUTO-SCAN: EVERY {0}S | SECURE CONNECTION ESTABLISHED</p>
    <p>DATA SOURCES: DEXSCREENER | COINGECKO | BIRDEYE</p>
    <p style='margin-top: 10px; color: #00ff00;'>🔒 BLOCK BOY SECURITY CONSOLE V2.0</p>
    <p style='margin-top: 5px;'>BLOCKCHAIN INTELLIGENCE SYSTEM</p>
</div>
""".format(auto_refresh), unsafe_allow_html=True)


# Auto-refresh
import time
time.sleep(auto_refresh)
st.rerun()
