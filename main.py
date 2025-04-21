from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db, TrashCan, Light
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()

class TrashCanCreate(BaseModel):
    id: str
    location: str

class TrashCanUpdate(BaseModel):
    location: str | None = None
    level: int | None = None

class LightCreate(BaseModel):
    id: str
    location: str
    state: bool = False

class LightUpdate(BaseModel):
    location: str | None = None
    state: bool | None = None

# Trash Can Endpoints
@app.post("/trashcan")
async def create_trashcan(trashcan: TrashCanCreate, db: AsyncSession = Depends(get_db)):
    new_trashcan = TrashCan(id=trashcan.id, location=trashcan.location)
    db.add(new_trashcan)
    await db.commit()
    return {"message": "Trash can created successfully"}

@app.get("/trashcan/{trash_can_id}")
async def get_trashcan(trash_can_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrashCan).where(TrashCan.id == trash_can_id))
    trashcan = result.scalars().first()
    if not trashcan:
        raise HTTPException(status_code=404, detail="Trash can not found")
    return trashcan

@app.put("/trashcan/{trash_can_id}")
async def update_trashcan(trash_can_id: str, update_data: TrashCanUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrashCan).where(TrashCan.id == trash_can_id))
    trashcan = result.scalars().first()
    if not trashcan:
        raise HTTPException(status_code=404, detail="Trash can not found")

    if update_data.location:
        trashcan.location = update_data.location
    if update_data.level is not None:
        trashcan.level = update_data.level
        if update_data.level == 0:
            trashcan.lastEmptied = datetime.utcnow()

    await db.commit()
    return {"message": "Trash can updated successfully"}

@app.delete("/trashcan/{trash_can_id}")
async def delete_trashcan(trash_can_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrashCan).where(TrashCan.id == trash_can_id))
    trashcan = result.scalars().first()
    if not trashcan:
        raise HTTPException(status_code=404, detail="Trash can not found")

    await db.delete(trashcan)
    await db.commit()
    return {"message": "Trash can deleted successfully"}

# Light Endpoints
@app.post("/light")
async def create_light(light: LightCreate, db: AsyncSession = Depends(get_db)):
    new_light = Light(id=light.id, location=light.location, state=light.state)
    db.add(new_light)
    await db.commit()
    return {"message": "Light created successfully"}

@app.get("/light/{light_id}")
async def get_light(light_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Light).where(Light.id == light_id))
    light = result.scalars().first()
    if not light:
        raise HTTPException(status_code=404, detail="Light not found")
    return light

@app.put("/light/{light_id}")
async def update_light(light_id: str, update_data: LightUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Light).where(Light.id == light_id))
    light = result.scalars().first()
    if not light:
        raise HTTPException(status_code=404, detail="Light not found")

    if update_data.location:
        light.location = update_data.location
    if update_data.state is not None:
        light.state = update_data.state

    await db.commit()
    return {"message": "Light updated successfully"}

@app.delete("/light/{light_id}")
async def delete_light(light_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Light).where(Light.id == light_id))
    light = result.scalars().first()
    if not light:
        raise HTTPException(status_code=404, detail="Light not found")

    await db.delete(light)
    await db.commit()
    return {"message": "Light deleted successfully"}

