import uuid as uuid_pkg
import enum
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class UserTypeValues(str, enum.Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    STAFF = "staff"
    COLLEGE_REPRESENTATIVE = "college_representative"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    name: Mapped[str] = mapped_column(String(length=30))
    phone_number: Mapped[int] = mapped_column(BigInteger)
    user_type: Mapped[UserTypeValues] = mapped_column(String(length=30), nullable=True)
    username: Mapped[str] = mapped_column(String(length=20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(length=50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=200))

    profile_image_url: Mapped[str] = mapped_column(String(length=200), default="https://profileimageurl.com")
    profile_short_bio: Mapped[str] = mapped_column(String(length=255), default='', nullable=True)
    profile_is_graduated: Mapped[bool] = mapped_column(default=False)
    profile_age: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(default_factory=uuid_pkg.uuid4, primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    tier_id: Mapped[int | None] = mapped_column(ForeignKey("tier.id"), index=True, default=None, init=False)
