import httpx
from app.config import settings

async def ask_ai(question: str) -> str:
    if not settings.OPENAI_API_KEY:
        return "AI is not configured. Add OPENAI_API_KEY to .env."

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a cautious trading research assistant. Provide fact-based analysis, mention uncertainty, and avoid guarantees of profits."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.4
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
