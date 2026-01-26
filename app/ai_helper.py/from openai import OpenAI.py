from openai import OpenAI

client = OpenAI()

def analyze_tokens_with_ai(tokens):
    if not tokens:
        return "No tokens to analyze."

    # Create a summary list of the first 10 tokens
    token_list = "\n".join([
        f"{t.symbol} on {t.chain} | liquidity: {t.liquidity_usd}"
        for t in tokens[:10]
    ])

    prompt = f"""
    You are a crypto trading assistant. Here are the top new tokens:

    {token_list}

    Which ones look the riskiest and which might have the highest upside (x1000 potential)?
    Provide reasoning in simple terms for a beginner trader.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in crypto and token analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
