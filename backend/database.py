"""Async SQLAlchemy engine, session, and Base for Veterinary Site Template.

Uses Postgres when DATABASE_URL is present. For prospecting/demo deployments,
falls back to a local SQLite database so a static demo can publish without
provisioning a paid/managed database first.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv(Path(__file__).parent / ".env")


def _normalize_database_url(url: str) -> str:
    """Railway exposes postgresql:// URLs; SQLAlchemy async needs asyncpg."""
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://") :]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://") :]
    return url


def _default_sqlite_url() -> str:
    db_path = Path(os.environ.get("SQLITE_DB_PATH", "/tmp/vet-demo.sqlite3"))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{db_path.as_posix()}"


DATABASE_URL = _normalize_database_url(os.environ.get("DATABASE_URL") or _default_sqlite_url())

engine_kwargs = {"echo": False, "future": True}
if not DATABASE_URL.startswith("sqlite+"):
    engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(DATABASE_URL, **engine_kwargs)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
