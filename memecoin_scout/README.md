
# 💎 Memecoin Scout Auto-Trader Bot  
### 🚀 Solana Real-Time Scanner • Momentum Scorer • Paper & Live Trader

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange?logo=streamlit)
![Solana](https://img.shields.io/badge/Chain-Solana-purple?logo=solana)
![Status](https://img.shields.io/badge/Mode-Paper%20Trading-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

### ⚡ Overview

**Memecoin Scout Auto-Trader** is an intelligent, fully automated trading bot that scans **new Solana tokens in real time**, scores them using liquidity, momentum, and risk signals, and executes **paper or live trades** based on custom strategy rules.

The goal:  
> Detect early gems before they trend, simulate (or execute) quick buy/sell trades, and compound small wins into larger growth — safely and transparently.

It combines:
- 🔍 **Real-time token detection** from DexScreener  
- 🧠 **Smart scoring** via Birdeye data and momentum metrics  
- 💾 **SQLite logging** for trades and tokens  
- 🤖 **Paper trading** with optional live execution  
- 📈 **Streamlit dashboard** for live visualization  
- 📱 **Telegram alerts** for instant notifications  

---

## 🧩 Core Features

| Feature | Description |
|----------|--------------|
| 🧭 **Live Token Scanning** | Continuously pulls new Solana pairs from DexScreener using async requests. |
| 🧠 **Intelligent Scoring** | Combines liquidity, volume, age, holders, and risk signals to rank new tokens. |
| 🚫 **Rug Filter Engine** | Filters out unverified or high-risk contracts and fake liquidity pools. |
| 💾 **SQLite Data Store** | Logs every discovered token, trade, and position for full transparency. |
| 🧮 **Risk Manager** | Dynamically sizes positions and enforces per-trade and daily loss limits. |
| 🧑‍💻 **Paper & Live Modes** | Simulate trades safely or execute via Jupiter Aggregator API (optional). |
| 💬 **Telegram Alerts** | Sends trade entries/exits and token discoveries directly to your Telegram bot. |
| 📊 **Streamlit Dashboard** | Visualize live trades, token data, and scores in your browser. |
| 🛑 **Kill Switch** | Create a `KILL.TXT` file at any time to instantly stop trading. |

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.13 |
| **APIs** | DexScreener / Birdeye / Jupiter (optional) |
| **Frontend** | Streamlit + Plotly |
| **Storage** | SQLite via `app/storage/db.py` |
| **Alerts** | Telegram Bot API |
| **Data Handling** | Pandas, HTTPX, Requests |
| **Deployment** | Local / Streamlit Cloud / VPS |
| **Version Control** | Git + GitHub |

---

## 🏗️ Project Structure
memecoin_scout/
├── app/
│ ├── alerting/ # Telegram alerts
│ ├── data_sources/ # DexScreener + Birdeye integrations
│ ├── execution/ # Jupiter executor (stub / live)
│ ├── storage/ # SQLite database + persistence
│ ├── trading/ # Strategy, risk, broker, safety, guard
│ ├── main.py # Paper trading loop
│ ├── settings.py # Environment configuration
│ └── init.py
├── dashboard_trades.py # Streamlit dashboard
├── requirements.txt # Dependencies
└── README.md # (this file)


