
---
# Memecoin Scout

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />


**Real-Time Solana Token Scanner**
Built by **JA Security**

---

## Overview

**Memecoin Scout** is a real-time scanner for newly launched Solana tokens.
It detects new trading pairs, applies risk filters, scores momentum, and surfaces higher-signal candidates through a lightweight dashboard.

The project is designed as a **research and monitoring system** for live on-chain market data and serves as a foundation for future automation and security-focused experimentation.

---

## Core Capabilities

* Real-time scanning of new Solana pairs (DexScreener)
* Risk filtering to remove low-liquidity and high-risk tokens
* Momentum-based scoring (liquidity, volume, age, holders)
* SQLite persistence for historical analysis
* Streamlit dashboard for live monitoring
* Optional Telegram alerts for high-scoring tokens
* Modular, extensible architecture

---

## Tech Stack

Python · Asyncio · Streamlit · SQLite · Pandas · DexScreener API · Telegram Bot API

---

## How It Works

```
DexScreener → Filters → Scoring → SQLite → Dashboard / Alerts
```

The scanner continuously ingests live market data, filters obvious risk, scores remaining tokens on a 0–1 scale, stores results, and exposes them through a live dashboard.

---

## Running the Project (Windows)

> **Note:**
> The commands below are written for **Windows PowerShell**.
> They will not work as-is in Command Prompt or Git Bash.

Open **two PowerShell terminals**. Both must stay running.

---

### Terminal 1 — Start the Scanner (Bot)

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
python app/main.py --live
```

**Expected output:**

```
[debug] Found 105 Solana pairs
[debug] 3 live solana pairs accepted after filtering
💎 HIDDEN GEM FOUND: ...
```

The scanner will continue running and monitoring new Solana pairs in real time.

---

### Terminal 2 — Start the Dashboard

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout
.\.venv\Scripts\Activate.ps1
streamlit run app/dashboard.py
```

Streamlit will output a local URL, typically:

```
http://localhost:8501
```

Open this URL in your browser to view the live dashboard.

---

### Notes

* Both terminals must remain running
* The scanner writes data to SQLite
* The dashboard reads live data from the database
* New tokens appear automatically as they are detected
* Thresholds and alerts are configurable via `config.yaml`

---

## Why It Matters

* End-to-end async system design
* Practical risk filtering in adversarial markets
* Uses **live market data**, not static samples
* Clean separation of scanning, scoring, storage, and UI

---

## License

MIT

---

**Built by JA Security | Web3 & DeFi Security Projects**

---




