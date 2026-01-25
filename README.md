# Memecoin Scout Bot

**Automated Solana Memecoin Discovery**

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />


text
# JA Security | Web3 & DeFi Security Projects

**Memecoin Scout** is a real-time scanner for newly launched Solana tokens. It monitors fresh pairs, applies configurable risk filters, scores momentum, and surfaces high-signal candidates through a lightweight dashboard.

The project is designed as a foundation for research, monitoring, and experimentation with live market data, and can be extended toward automated or semi-automated trading strategies.

---

## Key Capabilities

➡ Real-time scanning of new Solana pairs via DexScreener  
➡ Risk filtering to remove obvious rugs and low-liquidity tokens  
➡ Scoring engine combining liquidity, volume, age, holders, and momentum signals  
➡ Momentum detection for volume and price spikes  
➡ SQLite persistence for historical tracking and analysis  
➡ Streamlit dashboard for live exploration and filtering  
➡ Optional Telegram alerts for higher-scoring candidates  
➡ Modular architecture designed for extensibility (auto-trading, multi-chain support)

---

## Tech Stack

➡ **Python 3.11+**  
➡ **Asyncio** for concurrent scanning  
➡ **Streamlit** for the dashboard UI  
➡ **SQLite** for lightweight persistence  
➡ **Pandas** for data handling  
➡ **DexScreener API**  
➡ **Telegram Bot API** (optional alerts)

---

## Project Structure

memecoin_scout/
├── app/
│ ├── main.py # Async scanning loop
│ ├── filters.py # Risk filtering logic
│ ├── scorer.py # Token scoring engine
│ ├── storagedb.py # SQLite operations
│ └── alerting/ # Telegram notifications
├── dashboard.py # Streamlit dashboard
├── utils.py # Helper functions and formatting
├── config.yaml # Filters, thresholds, API keys
├── requirements.txt # Python dependencies
└── README.md # Project documentation

text

---

## How It Works

**High-level flow:**

DexScreener → Filters → Scorer → SQLite → Dashboard / Alerts

text

**Process:**

➡ The scanner continuously polls DexScreener for new Solana pairs  
➡ Tokens are filtered using minimum risk criteria (liquidity, holders, age, etc.)  
➡ Remaining tokens are scored on a 0–1 scale using momentum and risk metrics  
➡ Results are stored in SQLite for analysis and visualization  
➡ The dashboard reads from the database and displays live results  
➡ Optional Telegram alerts trigger for higher-scoring tokens

---

## Quick Start

### Clone and Set Up

```bash
git clone https://github.com/JASecurity/memecoin_scout
cd memecoin_scout
python -m venv .venv
Activate Virtual Environment
Windows (PowerShell):

powershell
.venv\Scripts\Activate.ps1
Windows (Command Prompt):

text
.venv\Scripts\activate.bat
Linux/Mac:

bash
source .venv/bin/activate
Install Dependencies
bash
pip install -r requirements.txt
Configuration
Edit config.yaml to match your setup and risk tolerance:

text
min_liq_usd: 5000
min_vol_5m_usd: 2000
min_score_to_trade: 0.75

telegram_token: "your_bot_token"
telegram_chat_id: "your_chat_id"

paper_mode: true
➡ You can tighten or relax these thresholds depending on how early or conservative you want to be.

Running the Bot and Dashboard
Open the project in VS Code and use two integrated terminals:

Terminal 1 – Start the Scanner
Windows (PowerShell):

powershell
cd memecoin_scout
.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
python app/main.py --live
Windows (Command Prompt):

text
cd memecoin_scout
.venv\Scripts\activate.bat
set PYTHONPATH=%cd%
python app/main.py --live
Linux/Mac:

bash
cd memecoin_scout
source .venv/bin/activate
export PYTHONPATH=$(pwd)
python app/main.py --live
Terminal 2 – Start the Dashboard
Windows (PowerShell):

powershell
cd memecoin_scout
.venv\Scripts\Activate.ps1
streamlit run dashboard.py
Windows (Command Prompt):

text
cd memecoin_scout
.venv\Scripts\activate.bat
streamlit run dashboard.py
Linux/Mac:

bash
cd memecoin_scout
source .venv/bin/activate
streamlit run dashboard.py
Access the Dashboard
➡ Streamlit will output a local URL, typically:

text
http://localhost:8501
➡ Open this in your browser to view the dashboard.

Dashboard Overview
➡ Live table of recently scanned tokens
➡ Token scores and key metrics
➡ Filters for liquidity, volume, age, and score
➡ Focused views on higher-scoring or flagged tokens
➡ Lightweight historical view backed by SQLite

The scanner and dashboard can run continuously to monitor new launches as they appear.

Troubleshooting
"No new tokens found"
➡ Normal during quieter periods
➡ Leave the scanner running
➡ Loosen thresholds in config.yaml if needed

Dashboard does not start
➡ Confirm Streamlit is installed: pip install streamlit
➡ Ensure the virtual environment is activated
➡ Check that port 8501 is free
➡ Confirm you are in the project root directory

Import or module errors
➡ Ensure PYTHONPATH is set
➡ Use Python from .venv
➡ Reinstall dependencies if needed: pip install -r requirements.txt

VS Code Integration (Optional)
For smoother operation, add these as VS Code tasks in .vscode/tasks.json:

json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Scanner",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": ["app/main.py", "--live"],
      "options": {
        "env": {
          "PYTHONPATH": "${workspaceFolder}"
        }
      },
      "problemMatcher": []
    },
    {
      "label": "Run Dashboard",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/Scripts/Activate.ps1; streamlit run dashboard.py",
      "problemMatcher": []
    }
  ]
}
Launch both components from VS Code's Terminal → Run Task menu.

Roadmap
Planned or potential extensions:

➡ Live trading integration (e.g., Jupiter DEX)
➡ Smarter token classification with richer feature sets
➡ Multi-chain support (Base, Ethereum, BSC, etc.)
➡ Backtesting using SQLite history
➡ Additional alert channels (Discord, Webhooks)
➡ More advanced risk and position-sizing logic

Why This Project Matters
➡ End-to-end system design (async ingestion → storage → UI)
➡ Practical risk filtering in noisy, adversarial markets
➡ Operational discipline around configuration and environments
➡ Use of real live market data instead of static examples

License
MIT — free to fork, extend, and deploy.

Built by JA Security
