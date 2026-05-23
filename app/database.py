from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.config import settings

engine = create_async_engine(settings.get_db, echo=False, future=True)

session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
