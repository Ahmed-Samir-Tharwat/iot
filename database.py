from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Boolean, Integer
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session

from datetime import datetime


DATABASE_URL = "postgresql+asyncpg://postgres:25802580@localhost:1234/samir_db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Base class for models
class Base(DeclarativeBase):
    pass

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    encodedImageData = Column(String, nullable=True)


class FireAlarm(Base):
    __tablename__ = "fire_alarms"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    active = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)




# Define the TrashCan model
class TrashCan(Base):
    __tablename__ = "trashcans"
    id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=False)
    level = Column(Integer, default=0)

# Define the Light model
class Light(Base):
    __tablename__ = "lights"
    id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=False)
    state = Column(Boolean, default=False)

# Connect to the database
async def connect_to_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Close the database connection
async def disconnect_from_db():
    await engine.dispose()

# CRUD Operations
async def get_user_by_id(user_id: str):
    async with SessionLocal() as session:
        return await session.get(User, user_id)

async def save_user_image(user_id: str, encoded_image_data: str):
    async with SessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            user.encodedImageData = encoded_image_data
            await session.commit()
            return user
        return None

async def update_user(user_id: str, new_data: dict):
    async with SessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            for key, value in new_data.items():
                setattr(user, key, value)
            await session.commit()
            return user
        return None

async def get_all_users():
    async with SessionLocal() as session:
        result = await session.execute("SELECT * FROM users")
        return result.fetchall()

async def create_trash_can(trash_can_id: str, location: str):
    async with SessionLocal() as session:
        trash_can = TrashCan(id=trash_can_id, location=location, level=0)
        session.add(trash_can)
        await session.commit()
        return trash_can

async def get_trash_can_status(trash_can_id: str):
    async with SessionLocal() as session:
        return await session.get(TrashCan, trash_can_id)

async def update_trash_can(trash_can_id: str, new_data: dict):
    async with SessionLocal() as session:
        trash_can = await session.get(TrashCan, trash_can_id)
        if trash_can:
            for key, value in new_data.items():
                setattr(trash_can, key, value)
            await session.commit()
            return trash_can
        return None

async def delete_trash_can(trash_can_id: str):
    async with SessionLocal() as session:
        trash_can = await session.get(TrashCan, trash_can_id)
        if trash_can:
            await session.delete(trash_can)
            await session.commit()
            return True
        return False

async def get_all_trash_cans():
    async with SessionLocal() as session:
        result = await session.execute("SELECT * FROM trashcans")
        return result.fetchall()

async def create_light(id : str , location: str, state: bool = False):
    async with SessionLocal() as session:
        light = Light(id = id,location=location, state=state)
        session.add(light)
        await session.commit()
        return light

async def get_light(light_id: str):
    async with SessionLocal() as session:
        return await session.get(Light, light_id)

async def update_light(light_id: str, new_data: dict):
    async with SessionLocal() as session:
        light = await session.get(Light, light_id)
        if light:
            for key, value in new_data.items():
                setattr(light, key, value)
            await session.commit()
            return light
        return None

async def delete_light(light_id: str):
    async with SessionLocal() as session:
        light = await session.get(Light, light_id)
        if light:
            await session.delete(light)
            await session.commit()
            return True
        return False

async def get_all_lights():
    async with SessionLocal() as session:
        result = await session.execute("SELECT * FROM lights")
        return result.fetchall()
# Add this function to database.py
async def get_db():
    async with SessionLocal() as session:
        yield session
