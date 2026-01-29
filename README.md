# **BLOCK BOY SECURITY CONSOLE**

<img width="1869" height="826" alt="Screenshot (302)" src="https://github.com/user-attachments/assets/296b555f-913b-4a24-a880-d20ace146682" />

## Overview

**Block Boy Security Console** is a real-time scanner for newly launched **Solana tokens**.

It detects new trading pairs, applies risk filters, scores momentum and security risks, and surfaces high-signal candidates through a lightweight dashboard.

Designed as a **Solana-focused research and monitoring system**, it provides live on-chain market insights and serves as a foundation for **automation, trading, and security research**.

---

## Core Features

### Solana Token Scanning

* Real-time detection of new Solana pairs (DexScreener, Raydium, Orca, Pump.fun)
* Scans ~96 unique token pairs every 60–90 seconds
* Liquidity and risk-based filtering
* Momentum scoring: liquidity, volume, age, holders
* Tracks processed tokens to avoid duplicates

### Data Management & Alerts

* SQLite database for historical analysis
* Streamlit dashboard for live monitoring
* Optional Telegram alerts for high-scoring tokens
* Modular and extensible architecture

---

## Tech Stack

```
Python · Asyncio · Streamlit · SQLite · Pandas
DexScreener API · Solana RPC · Telegram Bot API
```

---

## Architecture

```
DexScreener → Filters → Scoring → SQLite → Dashboard / Alerts
```

The scanner continuously ingests live Solana market data, filters risks, scores tokens, stores results, and exposes them via a live dashboard.

---

## Filters & Rules

### Solana Filters

| Filter            | Threshold            |
| ----------------- | -------------------- |
| Minimum Liquidity | $1,500               |
| Maximum Liquidity | $1,000,000           |
| Minimum Holders   | 10+                  |
| Token Age         | 5–1440 minutes       |
| Price Range       | Low-priced memecoins |
| Tax/Honeypot      | Detection enabled    |

---

## Installation & Running (Windows)

> **Note:** Commands are for **PowerShell**. Both terminals must remain open.

### Terminal 1 — Start Scanner

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
python app/main.py --live
```

**Expected Output:**

```
[debug] Found 105 Solana pairs
[debug] 3 live solana pairs accepted after filtering
💎 HIDDEN GEM FOUND: ...
```

### Terminal 2 — Start Dashboard

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout
.\.venv\Scripts\Activate.ps1
streamlit run app/dashboard.py
```

* Streamlit will provide a local URL (e.g., `http://localhost:8501`)
* Open in browser for live dashboard

---

## Configuration

**`config.yaml` Settings**

* Liquidity thresholds
* Holder requirements
* Scan intervals
* Risk score thresholds
* Telegram alert settings

**`.env` Environment Variables**

```
SOLANA_RPC_URL=your_rpc_url
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## Why It Matters

* **Async system design** for real-time monitoring
* Solana-native token discovery and analysis
* Practical risk filtering in adversarial memecoin markets
* Live data-driven insights
* Clean separation: scanning → scoring → storage → UI
* Demonstrates real-world **Web3 security skills**
* Foundation for automated Solana trading strategies

---

## Roadmap

**Current Phase: Risk Scoring Optimization**

* Reduce false positives on new Solana launches
* Improve liquidity and holder-based heuristics
* Advanced honeypot and rug-risk detection

**Next Phase: Web Dashboard**

* Enhanced real-time visualizations
* Historical trend analysis
* Token comparison tools

**Future Enhancements**

* Solana wallet tracking and behavior analysis
* Automated alert optimization
* DEX aggregator integration
* Strategy backtesting on historical Solana data

---

## License

MIT License

---

**Built by JA Security | Web3 & DeFi Security Projects**
