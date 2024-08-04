import uuid as uuid_pkg
from datetime import UTC, datetime

from typing import Literal, Sequence
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession


from ..core.db.database import Base
from sqlalchemy import select, and_, or_

ACCEPTED_FILE_TYPES: Literal = ("mp4", "mov", "mp3")


class Mentorship(Base):
    __tablename__ = "mentorship"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    mentor_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    transcription: Mapped[str] = mapped_column(Text, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    main_topics: Mapped[str] = mapped_column(Text, nullable=True)
    interest_courses: Mapped[str] = mapped_column(Text, nullable=True)
    main_questions_and_concerns: Mapped[str] = mapped_column(
        Text, nullable=True
    )
    insights: Mapped[str] = mapped_column(Text, nullable=True)

    recording_location: Mapped[str] = mapped_column(String(length=200), default="")
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

    mentorship_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=None
    )

    # Relationships
    mentor = relationship("User", foreign_keys=[mentor_id])
    student = relationship("User", foreign_keys=[student_id])

    @classmethod
    async def get_all_missing_transcription(
        cls, session: AsyncSession
    ) -> Sequence["Mentorship"]:
        return (
            (
                await session.execute(
                    select(cls).where(
                        and_(
                            cls.is_deleted == False,
                            cls.recording_location != "",
                            cls.recording_location != None,
                            or_(
                                cls.transcription == None,
                                cls.transcription == "",
                            ),
                        )
                    )
                )
            )
            .scalars()
            .all()
        )

    @classmethod
    async def get_all_missing_summary(
        cls, session: AsyncSession
    ) -> Sequence["Mentorship"]:
        return (
            (
                await session.execute(
                    select(cls).where(
                        and_(
                            cls.is_deleted == False,
                            cls.recording_location != "",
                            cls.recording_location != None,
                            cls.transcription != "",
                            cls.transcription != None,
                            or_(
                                cls.summary == None,
                                cls.summary == "",
                            ),
                        )
                    )
                )
            )
            .scalars()
            .all()
        )


    @classmethod
    async def get_all_missing_details(
        cls, session: AsyncSession
    ) -> Sequence["Mentorship"]:
        return (
            (
                await session.execute(
                    select(cls).where(
                        and_(
                            cls.is_deleted == False,
                            cls.recording_location != "",
                            cls.recording_location != None,
                            cls.transcription != "",
                            cls.transcription != None,
                            cls.summary != None,
                            cls.summary != "",
                            or_(
                                cls.insights == None,
                                cls.insights == "",
                                cls.main_questions_and_concerns == None,
                                cls.main_questions_and_concerns == "",
                                cls.interest_courses == None,
                                cls.interest_courses == "",
                                cls.main_topics == None,
                                cls.main_topics == "",
                            ),
                        )
                    )
                )
            )
            .scalars()
            .all()
        )
