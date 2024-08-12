import os
from datetime import datetime, timezone

from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request, File, UploadFile
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import (
    DuplicateValueException,
    BadRequestException,
    NotFoundException,
)
from ...core.logger import logger
from ...core.utils.timer_tracker import tracktime
from ...models.mentorship import ACCEPTED_FILE_TYPES
from ...crud.crud_mentorships import crud_mentorships
from ...schemas.user import UserRead
from ...schemas.mentorship import (
    MentorshipCreate,
    MentorshipRead,
    MentorshipUpdateWithRecord,
    MentorshipCreateInternal,
)
from ...core.trace_manager import trace_and_timeit, timing_and_trace_context

DIRNAME = os.path.dirname(__file__)


router = APIRouter(tags=["mentorships"])


@router.post("/mentorship", response_model=MentorshipRead, status_code=201)
async def write_mentorship(
    request: Request,
    mentorship: MentorshipCreate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> MentorshipRead:
    mentorship_row = await crud_mentorships.exists(
        db=db,
        student_id=mentorship.student_id,
        mentor_id=mentorship.mentor_id,
        mentorship_date=mentorship.mentorship_date,
    )
    if mentorship_row:
        raise DuplicateValueException(
            "Mentorship already exists for given date for student and mentor"
        )
    mentorship_internal_dict = mentorship.model_dump()
    mentorship_internal = MentorshipCreateInternal(**mentorship_internal_dict)
    created_mentorship: MentorshipRead = await crud_mentorships.create(
        db=db, object=mentorship_internal
    )
    logger.info(f"Created mentorship. mentor={mentorship.mentor_id}; student={mentorship.student_id}; date={mentorship.mentorship_date}")
    return created_mentorship



@trace_and_timeit
@router.get("/mentorships", response_model=PaginatedListResponse[MentorshipRead])
async def read_mentorships(
    request: Request,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    mentorships_data = await crud_mentorships.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=MentorshipRead,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(
        crud_data=mentorships_data, page=page, items_per_page=items_per_page
    )
    return response


@router.get("/mentorship/{mentorship_id}", response_model=MentorshipRead)
async def read_mentorship_by_id(
    request: Request,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    mentorship_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> MentorshipRead:
    mentorship_db = await crud_mentorships.get(
        db=db,
        schema_to_select=MentorshipRead,
        is_deleted=False,
        id=mentorship_id
    )
    if mentorship_db is not None:
        return mentorship_db
    raise NotFoundException("Mentorship not found")


@router.delete("/mentorship/{mentorship_id}")
async def delete_mentorship(
    request: Request,
    mentorship_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_mentorship = await crud_mentorships.get(db=db, schema_to_select=MentorshipRead, id=mentorship_id)
    if not db_mentorship:
        raise NotFoundException("Mentorship not found")

    await crud_mentorships.delete(db=db, id=mentorship_id)
    return {"message": "Mentorship deleted"}


@tracktime
@router.post("/mentorship/{mentorship_id}/upload_record/")
async def upload_video(
    request: Request,
    mentorship_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    record_file: UploadFile = File(
        ...,
        description=f"Mentorship recording video or audio file ({', '.join(ACCEPTED_FILE_TYPES)})",
    ),
) -> dict:
    db_mentorship = await crud_mentorships.get(db=db, schema_to_select=MentorshipRead, id=mentorship_id)
    if db_mentorship is None:
        raise NotFoundException("Mentorship not found")

    file_extension = record_file.filename.split(".")[-1]
    file_name = record_file.filename.split(".")[0]
    if file_extension not in ACCEPTED_FILE_TYPES:
        raise BadRequestException("File format not supported")
    logger.info(f"Added mentorship record. file_type={file_extension}; file_size={record_file.size} B")

    file_path = os.path.join(DIRNAME, f"../../../tmp/uploads/{file_name}_{datetime.now(timezone.utc).timestamp()}.{file_extension}")
    with timing_and_trace_context("Writing file in directory"):
        with open(file_path, "wb") as f:
            f.write(record_file.file.read())
    with timing_and_trace_context("Updating mentorship record in db"):
        values = MentorshipUpdateWithRecord(recording_location=file_path)
        await crud_mentorships.update(db=db, object=values, id=mentorship_id)
    return {"message": "Record file added to the mentorship"}
