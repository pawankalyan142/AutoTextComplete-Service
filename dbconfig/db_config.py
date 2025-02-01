from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select
from contextlib import asynccontextmanager

DATABASE_URL = "mysql+asyncmy://root:Mysql123@localhost:3306/world"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # The application starts here
    await engine.dispose()  # Cleanup on shutdown

app = FastAPI(lifespan=lifespan)