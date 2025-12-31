# Memecoin Scout Bot

**Automated Solana Memecoin Discovery & Paper Trading System**

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />


Real-time token scanner that identifies promising new memecoins on Solana, applies risk filters, scores momentum, simulates paper trades, and visualizes everything via an interactive dashboard. Built as a modular foundation for live trading strategies.

## 🚀 Features

- **Real-time DexScreener Scanning**: Fetches new Solana token pairs every 90 seconds
- **Advanced Scoring Engine**: Combines liquidity, volume, holders, social signals, and code quality metrics
- **Hard Risk Filters**: Enforces minimum liquidity ($5K+), volume, holder count, LP lock (50%+), and age limits
- **Paper Trading Engine**: Simulates buys/sells with position tracking and P&L logging
- **SQLite Persistence**: Stores tokens, trades, and positions for analysis
- **Streamlit Dashboard**: Live views of top tokens, trade logs, and position summaries
- **Telegram Alerts**: Optional notifications for trade entries/exits
- **Sniper Strategy**: Configurable risk-managed entry logic with take-profit/stop-loss levels
- **Modular Architecture**: Easy to extend for live Jupiter swaps or multi-chain support

## 🏗️ Tech Stack

Python 3.11+ | Streamlit | SQLite | Rich | Requests | Pandas
Solana/DexScreener APIs | Telegram Bot API


## 📁 Project Structure

memecoin_scout/
├── app/
│ ├── main.py # Core scanning + trading loop
│ ├── filters.py # Risk filtering logic
│ ├── scorer.py # Momentum scoring engine
│ ├── storagedb.py # SQLite database operations
│ ├── trading/ # Strategy, risk mgmt, paper broker
│ └── alerting/ # Telegram notifications
├── dashboard.py # Streamlit visualization
├── utils.py # Rich table formatting
├── config.yaml # Thresholds & API keys
├── requirements.txt # Dependencies
└── README.md

text

## 🎯 How It Works

DexScreener → Filter (liq/vol/holders) → Score (momentum/risk) →
Paper Trade → SQLite → Dashboard/Alerts

text

1. **Scanner** polls new Solana pairs
2. **Filters** reject rugs/low-liq tokens
3. **Scorer** ranks survivors (0-1.0 scale)
4. **Strategy** decides entry size if score > 0.75
5. **Paper Broker** logs simulated trades
6. **Dashboard** shows real-time insights

## 🛠️ Quick Start

### Prerequisites
git clone <repo>
cd memecoin_scout
python -m venv .venv
.venv\Scripts\activate # Windows
pip install -r requirements.txt


### 1. Run Live Bot (Terminal 1)
& ".venv\Scripts\python.exe" -m app.main --live


### 2. Open Dashboard (Terminal 2)
& ".venv\Scripts\python.exe" -m streamlit run dashboard.py



## ⚙️ Configuration

Edit `config.yaml`:
min_liq_usd: 5000
min_vol_5m_usd: 2000
min_score_to_trade: 0.75
telegram_token: "your_bot_token"
telegram_chat_id: "your_chat_id"
paper_mode: true


## 📊 Dashboard Screenshots

**Latest Tokens Table**
| Rank | Symbol | Score | Liq USD | Vol 1H | Holders | LP Lock |
|------|--------|-------|---------|--------|---------|---------|
| 1    | $MOON  | 0.92  | $12.5K  | $8.2K  | 245     | 87%     |

**Trade Log & Positions**

## 🔮 Future Roadmap

- [ ] Live Jupiter DEX trading
- [ ] AI-powered token classification
- [ ] Multi-chain (Base, ETH, BSC)
- [ ] Backtesting engine
- [ ] Discord webhooks
- [ ] Advanced risk models

💼 Why Employers Should Care
This project demonstrates:

Full-Stack Development: APIs, databases, web UIs, async processing

Financial Engineering: Risk management, position sizing, strategy backtesting

DevOps: Virtualenvs, config management, logging, monitoring

Real-World Data: Live crypto APIs, high-frequency polling

Production-Ready: Error handling, persistence, alerting, dashboards

10+ years construction management → Cybersecurity → Now algorithmic trading

Transitioning from foundation specialist/crew leader to building production trading systems. Self-taught Python, Solana ecosystem, and quant strategies.


## 📄 License
MIT - Free to fork, extend, deploy.

---

⭐ **Star if you find memecoin hunting interesting!**  
💬 **Issues/PRs welcome**  
🔗 **Demo video coming soon**

---

*Built by InvestaDad - Aspiring Cybersecurity Analyst | Google Cybersecurity Cert | Future Smart Contract Auditor*

