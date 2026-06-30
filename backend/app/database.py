"""
Database setup placeholder.

The application currently uses an in-memory Python list (see models.py)
for simplicity and ease of running the project without any setup steps.

To switch to SQLite persistence in the future:

1. Uncomment the SQLAlchemy setup below.
2. Define an ORM model (e.g. `StudentORM`) mirroring the `Student` dataclass.
3. Replace the `StudentDB` class in models.py with a class that performs
   SQLAlchemy queries (session.add, session.query, etc.) instead of
   operating on a Python list.
4. Set `USE_DATABASE = True` in config.py.
5. Run `Base.metadata.create_all(bind=engine)` on startup (see main.py).

Example SQLAlchemy setup (uncomment and adjust when ready):

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    from app.config import settings

    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # needed only for SQLite
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()
"""

# This module intentionally has no active code yet. It exists so the
# project structure already supports a clean migration path to SQLite
# without restructuring the rest of the app.
