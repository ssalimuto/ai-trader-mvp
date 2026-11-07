from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False
    mfa_enabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Trade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    symbol: str
    side: str
    quantity: float
    price: float
    status: str = "PAPER"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MarketSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = None
    action: str
    details: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
