# MemeCoin Scout — 0.1 (experimental)

> **High risk disclaimer**: This tool surfaces *extremely speculative* meme tokens. Nothing here is financial advice. 
> Many new tokens are scams or designed to rapidly dump (aka "rug pulls"). **Never invest more than you can afford to lose.**

## What it does
- Watches **newly listed** tokens (sources pluggable), applies **hard-risk filters**, then **scores** survivors on momentum + social/on-chain signals.
- (Optional) Uses an LLM to summarize risks and produce a **structured verdict** for each candidate.
- Can push alerts to a **Telegram** channel/chat (optional).

## Quick start (Demo mode — no API keys)
```bash
python -m app.main --demo
```
This loads `app/demo/sample_new_listings.json`, runs filters + scoring, and prints a ranked table.

## Setup
1. Python 3.10+ recommended.
2. Create a virtualenv and install deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
3. Copy config and tweak thresholds:
```bash
cp config.example.yaml config.yaml
```
4. (Optional) Set environment variables if you plan to use an LLM or Telegram:
- `LLM_PROVIDER` (e.g., `"openai"` or `"openrouter"`)
- `LLM_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

> ⚠️ The data-source modules include **clearly marked TODOs** where you can connect real feeds such as DexScreener, GeckoTerminal, Birdeye, pump.fun, DEXTools, Etherscan/Solscan APIs. Endpoints change; consult each service's documentation.

## How it works
- **Data sources** ingest raw new listings → normalized `TokenInfo` objects.
- **Hard filters** reject obvious rug/sybil/illicit patterns (honeypot flags, insane taxes, owner powers, etc.).
- **Scorer** assigns a 0–100 **Opportunity Score** from momentum/liquidity/holder distribution/social traction.
- **LLM (optional)** compresses everything into a JSON verdict: `watchlist | speculative | avoid` with a short rationale.
- **Alerting (optional)** Telegram push for top-N.
- **Config** controls thresholds per chain (Solana/EVM/BSC/etc.).

## Caution & guardrails
- Consider **paper trading/backtests** first; past performance ≠ future returns.
- Always manually verify contract code, LP lock/burn, mint authorities, taxes, and tradeability (no honeypot) *yourself* before buying.
- Treat LLM outputs as **summaries**, not truths.

## Commands
```bash
# Demo
python -m app.main --demo

# Live (after wiring sources + config.yaml)
python -m app.main --live

# Send alerts (requires Telegram setup)
python -m app.main --demo --alerts
```
