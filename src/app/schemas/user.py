from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema
from ..models.user import UserTypeValues

class UserBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["User Userson"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    phone_number: Annotated[int | None, Field(examples=[5563999476209], default=None)]
    user_type: Annotated[UserTypeValues | None, Field(None, example=UserTypeValues.STUDENT.value)]
    profile_age: Annotated[int | None, Field(None, example=25)]


class User(TimestampSchema, UserBase, UUIDSchema, PersistentDeletion):
    profile_image_url: Annotated[str, Field(default="https://www.profileimageurl.com")]
    hashed_password: str
    is_superuser: bool = False


class UserRead(BaseModel):
    id: int

    name: Annotated[str, Field(min_length=2, max_length=30, examples=["User Userson"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    phone_number: Annotated[int | None, Field(examples=[5563999476209], default=None)]
    user_type: Annotated[UserTypeValues | None, Field(None, example=UserTypeValues.STUDENT.value)]
    profile_age: Annotated[int | None, Field(None, example=25)]
    profile_image_url: str
    profile_short_bio: Annotated[str | None, Field('', max_length=255, example="This is a short bio.")]
    profile_is_graduated: Annotated[bool | None, Field(False, example=True)]


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")

    password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]


class UserCreateInternal(UserBase):
    hashed_password: str


class UserUpdate(UserBase):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=2, max_length=30, examples=["User Userberg"], default=None)]
    username: Annotated[
        str | None, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userberg"], default=None)
    ]
    email: Annotated[EmailStr | None, Field(examples=["user.userberg@example.com"], default=None)]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.profileimageurl.com"], default=None
        ),
    ]
    profile_short_bio: Annotated[str | None, Field('', max_length=255, example="This is a short bio.")]
    profile_is_graduated: Annotated[bool | None, Field(False, example=True)]


class UserUpdateInternal(UserUpdate):
    updated_at: datetime


class UserDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class UserRestoreDeleted(BaseModel):
    is_deleted: bool
