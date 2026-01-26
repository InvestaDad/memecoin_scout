# **BLOCK BOY SECURITY CONSOLE**


<img width="1889" height="837" alt="gameboy console style" src="https://github.com/user-attachments/assets/5659406a-7bad-485c-aad2-7e3ccbe08309" />

---

## Overview

**Block Boy Security Console** is a real-time scanner for newly launched **Solana tokens** with integrated **Ethereum smart contract security analysis**.

It detects new trading pairs, applies risk filters, scores momentum and security risks, and surfaces high-signal candidates through a lightweight dashboard.

Designed as a **multi-chain research and monitoring system**, it provides live on-chain market insights and serves as a foundation for **automation, trading, and security research**.

---

## Core Features

### Solana Token Scanning

* Real-time detection of new Solana pairs (DexScreener, Raydium, Orca, Pump.fun)
* Scans ~96 unique token pairs every 60–90 seconds
* Liquidity and risk-based filtering
* Momentum scoring: liquidity, volume, age, holders
* Tracks processed tokens to avoid duplicates

### Ethereum Smart Contract Security

* Security scanning via **GoPlus Security API**
* Honeypot detection & buy/sell tax analysis
* Risk scoring system (0–100 scale)
* Detects mintable tokens, hidden owners, suspicious patterns
* Integrates **Alchemy API** for Ethereum mainnet access

### Data Management & Alerts

* SQLite database for historical analysis
* Streamlit dashboard for live monitoring
* Optional Telegram alerts for high-scoring tokens
* Modular and extensible architecture

---

## Tech Stack

```
Python · Asyncio · Streamlit · SQLite · Pandas
DexScreener API · GoPlus Security API · Alchemy API · Telegram Bot API
```

---

## Architecture

```
DexScreener → Filters → Scoring → SQLite → Dashboard / Alerts
                    ↓
        GoPlus Security (Ethereum)
```

The scanner continuously ingests live data from Solana & Ethereum, filters risks, scores tokens, stores results, and exposes them via a live dashboard.

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

### Ethereum Security Checks

| Check                 | Description                            |
| --------------------- | -------------------------------------- |
| Honeypot Detection    | Detect malicious contracts             |
| Buy/Sell Tax Analysis | Flags high tax tokens                  |
| Holder Distribution   | Detects abnormal holder patterns       |
| Mintable Token        | Detects contracts that can mint tokens |
| Hidden Owner          | Checks for non-transparent ownership   |
| Verification Status   | Confirms verified contract on Ethereum |

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

### Testing Ethereum Scanner (Optional)

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout\app
python -c "from ethereum_scanner import scan_ethereum_contract; import json; print(json.dumps(scan_ethereum_contract('0xdac17f958d2ee523a2206206994597c13d831ec7'), indent=2))"
```

---

## Configuration

**`config.yaml` Settings**

* Liquidity thresholds
* Holder requirements
* Scan intervals
* Risk score thresholds
* Telegram alert settings
* Ethereum/Solana chain priorities

**`.env` Environment Variables**

```
ALCHEMY_URL=your_alchemy_url
GOPLUS_API_KEY=your_goplus_key
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## Why It Matters

* **Async system design** for real-time monitoring
* Multi-chain security analysis (Solana + Ethereum)
* Practical risk filtering in adversarial markets
* Live data-driven insights
* Clean separation: scanning → scoring → storage → UI
* Demonstrates real-world **Web3 security skills**
* Foundation for automated trading strategies

---

## Roadmap

**Current Phase: Risk Scoring Optimization**

* Fine-tune Ethereum scoring to reduce false positives
* Expand whitelist for legitimate contracts
* Advanced honeypot detection

**Next Phase: Web Dashboard**

* Unified Solana + Ethereum interface
* Real-time risk visualization
* Historical data analysis

**Future Enhancements**

* Additional EVM chains (BSC, Polygon, Arbitrum)
* Wallet tracking and analysis
* Automated alert optimization
* DEX aggregator integration

---

## License

MIT License

---

**Built by JA Security | Web3 & DeFi Security Projects**

---





>>>>>>> d406194208f8b93f0d1376c14dc41ddd74d000fc


