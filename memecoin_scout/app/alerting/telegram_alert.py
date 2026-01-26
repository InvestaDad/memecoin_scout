
import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_alert(token_data: dict):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[alert] Telegram not configured correctly.")
        return

    message = (
        "New Token Alert:\n"
        f"Name: {token_data.get('name','N/A')}\n"
        f"Chain: {token_data.get('chain','N/A')}\n"
        f"Score: {token_data.get('score','N/A')}\n"
        f"Liquidity: ${token_data.get('liquidity','N/A')}\n"
        f"Volume (1h): ${token_data.get('volume','N/A')}\n"
        f"Holders: {token_data.get('holders','N/A')}\n"
        f"LP Lock: {token_data.get('lp_lock','N/A')}%\n"
        f"Link: {token_data.get('link','N/A')}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(url, data=data)
            if r.status_code == 200:
                print(f"[alert] Telegram message sent for {token_data.get('name','N/A')}")
            else:
                print(f"[alert] Failed to send message: {r.text}")
    except Exception as e:
        print(f"[alert] Error sending Telegram message: {e}")
