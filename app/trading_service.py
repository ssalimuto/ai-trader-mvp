from sqlmodel import Session, select
from app.models import Trade

def create_trade(session: Session, user_id: int, symbol: str, side: str, quantity: float, price: float):
    trade = Trade(
        user_id=user_id,
        symbol=symbol.upper(),
        side=side.upper(),
        quantity=quantity,
        price=price,
        status="PAPER"
    )
    session.add(trade)
    session.commit()
    session.refresh(trade)
    return trade

def get_user_trades(session: Session, user_id: int):
    return session.exec(select(Trade).where(Trade.user_id == user_id)).all()
