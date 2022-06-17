from .database import SessionLocal


def get_db():
    """
    Creates and yields a database session with use of a SQLAlchemy `sessionmaker`.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
