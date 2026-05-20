"""
Database connection and session management.
Uses asyncpg with SQLAlchemy async for PostgreSQL + pgvector.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://taxai:taxai_secure_2026@localhost:5432/taxai"
)

# Convert postgresql:// to postgresql+asyncpg:// if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Verify database connection on startup."""
    async with engine.begin() as conn:
        # Simple connectivity check
        await conn.execute("SELECT 1")
    print("✅ Database connected successfully")


async def get_session() -> AsyncSession:
    """Get an async database session."""
    async with async_session() as session:
        yield session
