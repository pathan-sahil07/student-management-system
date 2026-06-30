"""
API route definitions for student CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status

from app.models import db
from app.schemas import (
    MessageResponse,
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)

router = APIRouter(prefix="/students", tags=["Students"])


@router.get(
    "",
    response_model=StudentListResponse,
    summary="List all students",
    description="Returns all students, optionally filtered by a search query "
    "matching name, email, or course (case-insensitive).",
)
def get_students(
    search: str | None = Query(
        None, description="Search term to filter by name, email, or course"
    )
) -> StudentListResponse:
    students = db.get_all()

    if search:
        term = search.strip().lower()
        students = [
            s
            for s in students
            if term in s.name.lower()
            or term in s.email.lower()
            or term in s.course.lower()
        ]

    # Most recently added first (useful for the dashboard's "recent" view).
    students = sorted(students, key=lambda s: s.id, reverse=True)

    return StudentListResponse(total=len(students), students=students)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get a single student by ID",
    responses={404: {"description": "Student not found"}},
)
def get_student(student_id: int) -> StudentResponse:
    student = db.get_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} was not found",
        )
    return student


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
    responses={409: {"description": "Email already registered"}},
)
def create_student(payload: StudentCreate) -> StudentResponse:
    if db.get_by_email(payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A student with email '{payload.email}' already exists",
        )

    student = db.create(
        name=payload.name,
        email=payload.email,
        course=payload.course,
        year=payload.year,
        phone=payload.phone,
    )
    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update an existing student",
    responses={404: {"description": "Student not found"}, 409: {"description": "Email already registered"}},
)
def update_student(student_id: int, payload: StudentUpdate) -> StudentResponse:
    existing = db.get_by_id(student_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} was not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided to update",
        )

    if "email" in update_data:
        email_owner = db.get_by_email(update_data["email"])
        if email_owner is not None and email_owner.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A student with email '{update_data['email']}' already exists",
            )

    updated_student = db.update(student_id, **update_data)
    return updated_student


@router.delete(
    "/{student_id}",
    response_model=MessageResponse,
    summary="Delete a student",
    responses={404: {"description": "Student not found"}},
)
def delete_student(student_id: int) -> MessageResponse:
    existing = db.get_by_id(student_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} was not found",
        )

    db.delete(student_id)
    return MessageResponse(message=f"Student '{existing.name}' was deleted successfully")
