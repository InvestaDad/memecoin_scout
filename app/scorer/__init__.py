from app.schemas import TokenInfo

def score_tokens(token: TokenInfo):
    """
    Assigns a score_total to a TokenInfo object (0–100) based on:
    - liquidity
    - 1h volume
    - age
    """
    try:
        score = 0

        # --- Liquidity weight ---
        liq = token.liquidity.usd
        if liq > 100_000:
            score += 40
        elif liq > 25_000:
            score += 25
        elif liq > 5_000:
            score += 10

        # --- 1h Volume weight ---
        vol = token.volume.usd_1h
        if vol > 100_000:
            score += 30
        elif vol > 25_000:
            score += 20
        elif vol > 5_000:
            score += 10

        # --- Age bonus (newer = better) ---
        age = token.age_minutes
        if age < 10:
            score += 20
        elif age < 60:
            score += 10

        token.score_total = min(score, 100)

    except Exception:
        token.score_total = 0
