# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///../data/turo.db"

engine = create_async_engine(
    DATABASE_URL, echo=True
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
