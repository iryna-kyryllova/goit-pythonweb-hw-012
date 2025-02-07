import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.conf.config import settings


class DatabaseSessionManager:
    """
    Manages database sessions using SQLAlchemy's async engine.
    """

    def __init__(self, url: str):
        """
        Initialize the database session manager.

        Args:
            url: The database connection URL.
        """
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """
        Provide a database session using an async context manager.

        Yields:
            An active database session.

        Raises:
            Exception: If the database session is not initialized.
            SQLAlchemyError: If an error occurs during session operations.
        """
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise  # Re-raise the original error
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.DB_URL)


async def get_db():
    """
    Dependency function to get a database session.

    Yields:
        An active database session.
    """
    async with sessionmanager.session() as session:
        yield session
