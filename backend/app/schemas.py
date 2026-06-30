"""
Pydantic schemas used for request validation and response serialization.

Keeping these separate from the internal `models.py` dataclasses allows the
API contract to remain stable even if the internal storage implementation
changes (e.g. moving to SQLAlchemy ORM models).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    """Shared fields/validation rules for student create & update."""

    name: str = Field(..., min_length=2, max_length=100, description="Full name of the student")
    email: EmailStr = Field(..., description="Unique email address of the student")
    course: str = Field(..., min_length=2, max_length=100, description="Enrolled course/program")
    year: int = Field(..., ge=1, le=6, description="Current year of study (1-6)")
    phone: str = Field(..., min_length=7, max_length=15, description="Contact phone number")

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return value.strip()

    @field_validator("course")
    @classmethod
    def course_must_be_valid(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Course cannot be empty or whitespace")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def phone_must_be_digits(cls, value: str) -> str:
        cleaned = value.replace(" ", "").replace("-", "").replace("+", "")
        if not cleaned.isdigit():
            raise ValueError("Phone number must contain only digits, spaces, dashes, or a leading +")
        return value.strip()


class StudentCreate(StudentBase):
    """Schema for creating a new student (POST /students)."""
    pass


class StudentUpdate(BaseModel):
    """
    Schema for updating an existing student (PUT /students/{id}).
    All fields are optional to support partial updates, but at least
    one field should be supplied (enforced in the route handler).
    """

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    course: Optional[str] = Field(None, min_length=2, max_length=100)
    year: Optional[int] = Field(None, ge=1, le=6)
    phone: Optional[str] = Field(None, min_length=7, max_length=15)


class StudentResponse(StudentBase):
    """Schema returned to the client for a single student."""

    id: int = Field(..., description="Unique identifier of the student")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Aarav Sharma",
                "email": "aarav.sharma@example.com",
                "course": "Computer Science",
                "year": 2,
                "phone": "9876543210",
            }
        }
    }


class StudentListResponse(BaseModel):
    """Schema returned for paginated/list endpoints."""

    total: int
    students: list[StudentResponse]


class MessageResponse(BaseModel):
    """Generic message response, e.g. for DELETE confirmations."""

    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    detail: str
