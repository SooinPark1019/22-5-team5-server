from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nickname: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(20))

    blogs: Mapped["Blog"] = relationship("Blog", back_populates="user", uselist=False)

class BlockedToken(Base):
    __tablename__ = "blocked_token"

    token_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime)
