from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, text, ForeignKey, JSON, String, DateTime, PickleType
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from .sessionmaker import engine
from ..config import Configuration
from datetime import datetime
Config = Configuration()


class Base(DeclarativeBase):
    pass


class TokenBind(Base):
    __tablename__ = "token_binds"
    token: Mapped[str] = mapped_column(String(255), primary_key=True)
    secret: Mapped[str] = mapped_column(String(255))
    discord_id: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"TokenBind(token={self.token}, discord_id={self.discord_id})"

class Verification(Base):
    __tablename__ = "verifications"
    discord_id: Mapped[int] = mapped_column(primary_key=True)
    wiki_username: Mapped[str] = mapped_column(String(255))
    wiki_id: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Verification(token={self.token}, discord_id={self.discord_id})"
Base.metadata.create_all(engine)