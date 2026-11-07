from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.auth import authenticate_user, create_access_token, get_current_user, hash_password, get_user_by_email, get_user_by_username
from app.config import settings
from app.db import init_db, get_session
from app.models import User
from app.ai_service import ask_ai
from app.market_service import get_mock_market_snapshot
from app.trading_service import create_trade, get_user_trades
from app.update_service import check_for_updates

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
async def home():
    return {"app": settings.APP_NAME, "status": "ok"}

@app.post("/signup")
async def signup(data: dict, session: Session = Depends(get_session)):
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Missing fields")

    if get_user_by_email(session, email):
        raise HTTPException(status_code=400, detail="Email already exists")
    if get_user_by_username(session, username):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
        is_active=True,
        mfa_enabled=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User created successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "mfa_enabled": current_user.mfa_enabled
    }

@app.post("/ai/query")
async def ai_query(data: dict, current_user: User = Depends(get_current_user)):
    question = data.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    answer = await ask_ai(question)
    return {"answer": answer}

@app.get("/market/{symbol}")
async def market(symbol: str):
    return await get_mock_market_snapshot(symbol)

@app.post("/paper-trade")
async def paper_trade(data: dict, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = float(data.get("quantity", 0))
    price = float(data.get("price", 0))

    if not symbol or not side:
        raise HTTPException(status_code=400, detail="symbol and side required")

    trade = create_trade(session, current_user.id, symbol, side, quantity, price)
    return {"trade": trade}

@app.get("/trades")
async def trades(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return {"trades": get_user_trades(session, current_user.id)}

@app.get("/updates/check")
async def updates():
    return await check_for_updates()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
