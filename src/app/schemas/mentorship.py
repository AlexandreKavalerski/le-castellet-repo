from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema

class MentorshipBase(BaseModel):
    mentorship_date: Annotated[datetime | None, Field(None, examples=["2024-09-13"])]


class Mentorship(TimestampSchema, MentorshipBase, UUIDSchema, PersistentDeletion):
    recording_location: Annotated[str, Field(default="")]


class MentorshipUpdateWithRecord(BaseModel):
    recording_location: Annotated[str, Field(default="")]


class MentorshipRead(BaseModel):
    id: int
    recording_location: str | None
    # transcription: str | None
    summary: str | None
    main_topics: str | None
    interest_courses: str | None
    main_questions_and_concerns: str | None
    insights: str | None


class MentorshipCreate(MentorshipBase):
    model_config = ConfigDict(extra="forbid")

    mentor_id: int
    student_id: int


class MentorshipCreateInternal(MentorshipCreate):
    transcription: str | None = None
    summary: str | None = None
    main_topics: str | None = None
    interest_courses: str | None = None
    main_questions_and_concerns: str | None = None
    insights: str | None = None

class MentorshipUpdate(MentorshipBase):
    model_config = ConfigDict(extra="forbid")

    main_topics: Annotated[str | None, Field('', max_length=200, example="These are the main topics.")]
    interest_courses: Annotated[str | None, Field('', max_length=200, example="These are the interest courses mentioned in the transcription.")]
    main_questions_and_concerns: Annotated[str | None, Field('', max_length=200, example="These are the main questions and concerns mentioned in the transcription.")]
    insights: Annotated[str | None, Field('', max_length=200, example="These are the insights from the transcription.")]


class MentorshipUpdateInternal(MentorshipUpdate):
    updated_at: datetime


class MentorshipDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class MentorshipRestoreDeleted(BaseModel):
    is_deleted: bool
