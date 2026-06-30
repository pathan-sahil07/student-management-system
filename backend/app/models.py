"""
Data models for the application.

This module defines the internal representation of a Student and an
in-memory "database" backed by a Python list. It is intentionally kept
separate from the Pydantic request/response schemas (see schemas.py) so
that the storage layer can later be swapped for a real database (SQLite,
PostgreSQL, etc.) with minimal changes to the rest of the application.

To switch to SQLite later:
1. Implement SQLAlchemy models in database.py
2. Replace the `StudentDB` class methods below with SQLAlchemy queries
3. The routes.py file will not need to change since it only depends on
   the public interface of `StudentDB` (get_all, get_by_id, create, update, delete)
"""

from dataclasses import dataclass, field
from itertools import count
from threading import Lock
from typing import Optional


@dataclass
class Student:
    """Internal representation of a Student record."""
    id: int
    name: str
    email: str
    course: str
    year: int
    phone: str


class StudentDB:
    """
    Thread-safe in-memory data store for Student records.

    Uses a simple Python list as the backing store. A lock protects
    mutations since FastAPI may handle requests concurrently.
    """

    def __init__(self) -> None:
        self._students: list[Student] = []
        self._id_counter = count(1)
        self._lock = Lock()
        self._seed_data()

    def _seed_data(self) -> None:
        """Pre-populate with sample students so the app is usable immediately."""
        sample_students = [
            {"name": "Aarav Sharma", "email": "aarav.sharma@example.com", "course": "Computer Science", "year": 2, "phone": "9876543210"},
            {"name": "Diya Patel", "email": "diya.patel@example.com", "course": "Electronics Engineering", "year": 3, "phone": "9876543211"},
            {"name": "Vihaan Reddy", "email": "vihaan.reddy@example.com", "course": "Mechanical Engineering", "year": 1, "phone": "9876543212"},
            {"name": "Ananya Iyer", "email": "ananya.iyer@example.com", "course": "Information Technology", "year": 4, "phone": "9876543213"},
            {"name": "Kabir Singh", "email": "kabir.singh@example.com", "course": "Computer Science", "year": 2, "phone": "9876543214"},
        ]
        for data in sample_students:
            self.create(**data)

    def get_all(self) -> list[Student]:
        return list(self._students)

    def get_by_id(self, student_id: int) -> Optional[Student]:
        return next((s for s in self._students if s.id == student_id), None)

    def get_by_email(self, email: str) -> Optional[Student]:
        return next((s for s in self._students if s.email.lower() == email.lower()), None)

    def create(self, name: str, email: str, course: str, year: int, phone: str) -> Student:
        with self._lock:
            student = Student(
                id=next(self._id_counter),
                name=name,
                email=email,
                course=course,
                year=year,
                phone=phone,
            )
            self._students.append(student)
            return student

    def update(self, student_id: int, **kwargs) -> Optional[Student]:
        with self._lock:
            student = self.get_by_id(student_id)
            if student is None:
                return None
            for key, value in kwargs.items():
                if value is not None and hasattr(student, key):
                    setattr(student, key, value)
            return student

    def delete(self, student_id: int) -> bool:
        with self._lock:
            student = self.get_by_id(student_id)
            if student is None:
                return False
            self._students.remove(student)
            return True


# Singleton instance used across the application.
db = StudentDB()
