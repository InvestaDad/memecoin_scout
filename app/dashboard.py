import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import streamlit_autorefresh



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


# SOLANA CRYPTO COLORS THEME
# Primary: Purple (#9945FF, #14F195) - Solana's signature gradient
# Accent: Cyan (#14F195), Magenta (#DC1FFF)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    /* Solana Purple-to-Teal Gradient Background */
    .main {
        background: linear-gradient(135deg, #1a0d2e 0%, #16213e 50%, #0f3443 100%);
        font-family: 'Press Start 2P', monospace;
    }
    
    /* Solana base colors */
    .stApp {
        background-color: #0a0015;
        color: #14F195;
    }
    
    /* Headers - Solana Cyan Glow */
    h1, h2, h3 {
        color: #14F195 !important;
        font-family: 'Press Start 2P', monospace !important;
        text-shadow: 0 0 15px #14F195, 0 0 30px #9945FF, 2px 2px #000;
        font-size: 16px !important;
        line-height: 1.8 !important;
    }
    
    h1 { 
        font-size: 20px !important;
        text-transform: uppercase;
    }
    
    /* Token cards - Solana Purple BG + Cyan Border */
    .token-card {
        background: linear-gradient(135deg, #16213e 0%, #1a0d2e 100%);
        border: 4px solid #14F195;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        line-height: 1.8;
        color: #14F195;
        box-shadow: 0 0 25px rgba(20, 241, 149, 0.5), 0 0 40px rgba(153, 69, 255, 0.3), 4px 4px 0px #000;
    }
    
    /* Alert box - Solana Magenta */
    .alert-card {
        background: linear-gradient(135deg, #2e1a3d 0%, #1a0d2e 100%);
        border: 4px solid #DC1FFF;
        padding: 12px;
        margin: 8px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
        line-height: 1.6;
        color: #DC1FFF;
        box-shadow: 0 0 25px rgba(220, 31, 255, 0.5), 0 0 40px rgba(153, 69, 255, 0.3);
    }
    
    /* Secure box - Solana Cyan/Teal */
    .secure-card {
        background: linear-gradient(135deg, #0f3443 0%, #16213e 100%);
        border: 4px solid #14F195;
        padding: 12px;
        margin: 8px 0;
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
        line-height: 1.6;
        color: #14F195;
        box-shadow: 0 0 25px rgba(20, 241, 149, 0.5);
    }
    
    /* Metric boxes - Solana gradient */
    .stMetric {
        background: linear-gradient(135deg, #16213e, #1a0d2e) !important;
        border: 3px solid #14F195 !important;
        padding: 10px !important;
        font-family: 'Press Start 2P', monospace !important;
        color: #14F195 !important;
        box-shadow: 0 0 20px rgba(20, 241, 149, 0.4), 0 0 30px rgba(153, 69, 255, 0.2);
    }
    
    .stMetric label {
        color: #9945FF !important;
        font-size: 8px !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #14F195 !important;
        font-size: 18px !important;
        text-shadow: 0 0 10px #14F195;
    }
    
    /* Sidebar - Solana gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0d2e 0%, #0f3443 100%);
        border-right: 5px solid #14F195;
        box-shadow: 5px 0 20px rgba(20, 241, 149, 0.3);
    }
    
    section[data-testid="stSidebar"] * {
        color: #14F195 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }
    
    /* Buttons - Solana Purple to Cyan gradient */
    .stButton button {
        background: linear-gradient(135deg, #9945FF, #14F195) !important;
        color: #000000 !important;
        border: 3px solid #14F195 !important;
        border-radius: 0px !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 10px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        box-shadow: 0 0 15px rgba(20, 241, 149, 0.6), 0 0 25px rgba(153, 69, 255, 0.4), 3px 3px 0px #000 !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #DC1FFF, #14F195) !important;
        transform: translate(2px, 2px);
        box-shadow: 0 0 25px rgba(20, 241, 149, 0.9), 0 0 35px rgba(220, 31, 255, 0.6), 1px 1px 0px #000 !important;
    }
    
    /* Link buttons - Solana themed */
    a {
        color: #14F195 !important;
        text-shadow: 0 0 5px #14F195;
    }
    
    /* Input fields - Solana colors */
    .stTextInput input, .stNumberInput input {
        background-color: #1a0d2e !important;
        color: #14F195 !important;
        border: 2px solid #9945FF !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #14F195 !important;
        box-shadow: 0 0 10px rgba(20, 241, 149, 0.5) !important;
    }
    
    /* Sliders - Solana purple */
    .stSlider {
        font-family: 'Press Start 2P', monospace !important;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: linear-gradient(90deg, #9945FF, #14F195) !important;
    }
    
    /* Divider - Solana cyan */
    hr {
        border-color: #14F195 !important;
        border-width: 2px !important;
        box-shadow: 0 0 10px rgba(20, 241, 149, 0.5);
    }
    
    /* Status text */
    .status-text {
        background: linear-gradient(135deg, #16213e, #1a0d2e);
        border: 3px solid #14F195;
        padding: 10px;
        text-align: center;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        color: #14F195;
        margin: 20px 0;
        box-shadow: 0 0 20px rgba(20, 241, 149, 0.4);
    }
    
    /* Blink animation - Solana cyan */
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    .blink {
        animation: blink 1s infinite;
    }
    
    /* Multiselect - Solana colors */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #9945FF !important;
        color: #ffffff !important;
    }
    
    /* Checkbox - Solana purple */
    .stCheckbox {
        color: #14F195 !important;
    }
</style>
""", unsafe_allow_html=True)


# Title with Solana-themed Security Console aesthetic
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #9945FF, #14F195); border: 5px solid #14F195; margin-bottom: 20px; box-shadow: 0 0 35px rgba(20, 241, 149, 0.6), 0 0 50px rgba(153, 69, 255, 0.4);'>
    <h1 style='color: #000000 !important; text-shadow: 0 0 10px #14F195, 2px 2px #000 !important;'>🔒 BLOCK BOY SECURITY CONSOLE</h1>
    <p style='color: #000000; font-size: 10px; font-family: "Press Start 2P", monospace; font-weight: bold;'>
        SOLANA BLOCKCHAIN SCANNER V2.0
    </p>
    <p style='color: #1a0d2e; font-size: 8px; font-family: "Press Start 2P", monospace; margin-top: 10px; font-weight: bold;'>
        [ CLASSIFIED: THREAT INTELLIGENCE PROTOCOL ]
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
    min_holders = st.number_input("MIN HOLDERS", 0, 1000, 0)
    
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
    
    # Bot status indicator - Solana cyan
    st.markdown(f"<div class='blink' style='color: #14F195;'>● ACTIVE</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #9945FF; font-size: 8px; margin-top: 10px;'>UPTIME: CONTINUOUS</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #9945FF; font-size: 8px;'>REFRESH: {auto_refresh}S</div>", unsafe_allow_html=True)


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
    
    if min_holders > 0 and 'holders' in tokens_df.columns:
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
        age_days = age_min / 1440
        price = row.get('price_usd', 0)
        address = row.get('address', '')
        
        # Threat level indicator - using Solana colors
        if score >= 8:
            threat_level = "[CRITICAL]"
            threat_color = "#DC1FFF"  # Solana magenta
        elif score >= 7:
            threat_level = "[HIGH]"
            threat_color = "#ff6b9d"  # Lighter magenta
        elif score >= 6:
            threat_level = "[MEDIUM]"
            threat_color = "#9945FF"  # Solana purple
        else:
            threat_level = "[LOW]"
            threat_color = "#14F195"  # Solana cyan
        
        st.markdown(f"""
        <div class='token-card'>
            <p style='color: {threat_color}; text-shadow: 0 0 10px {threat_color};'>{threat_level} ${symbol}</p>
            <p>THREAT SCORE: {score:.1f}/10</p>
            <p>LIQUIDITY: ${liquidity:,.0f}</p>
            <p>HOLDERS: {holders if holders > 0 else 'N/A'}</p>
            <p>AGE: {age_days:.1f}D ({age_min:.0f}M)</p>
            <p>PRICE: ${price:.8f}</p>
            <p style='font-size: 7px; margin-top: 8px; color: #9945FF;'>ADDR: {address[:16]}...</p>
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


# Footer - Solana themed
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 15px; font-size: 8px; color: #9945FF;'>
    <p>AUTO-SCAN: EVERY {auto_refresh}S | SECURE CONNECTION ESTABLISHED</p>
    <p>DATA SOURCES: DEXSCREENER | COINGECKO | BIRDEYE</p>
    <p style='margin-top: 10px; color: #14F195; text-shadow: 0 0 10px #14F195;'>🔒 BLOCK BOY SECURITY CONSOLE V2.0</p>
    <p style='margin-top: 5px; color: #9945FF;'>POWERED BY SOLANA BLOCKCHAIN</p>
</div>
""", unsafe_allow_html=True)

