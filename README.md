# ssalimuto bot

A simple AI-assisted trading research and paper trading app MVP.

## What it does
- AI market research assistant
- Paper trading workflow
- Secure login using hashed passwords
- Simple dashboard UI
- Local SQLite database
- Update-check stub for signed releases

## IMPORTANT
This project is a safe MVP only. It does not place real orders or connect to live broker accounts. Use it for testing and research.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your own secret values before running.

## Run the app

```bash
uvicorn app.main:app --reload
```

Open in browser:
- http://localhost:8000
- API docs: http://localhost:8000/docs

## Notes
- Use strong secret keys and rotate them regularly.
- Do not expose real credentials in code or chat.
- Add MFA / passkeys in production.
- Only allow signed software updates.
