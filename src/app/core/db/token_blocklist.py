from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    token: Mapped[str] = mapped_column(String(length=100), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
