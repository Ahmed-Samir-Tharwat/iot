from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel, field_validator
from datetime import datetime
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from database import (
    connect_to_db, disconnect_from_db, create_trash_can, get_trash_can_status, 
    update_trash_can, delete_trash_can, get_all_trash_cans, create_light, 
    get_light, update_light, delete_light, get_all_lights, get_db, FireAlarm
)
from sqlalchemy.orm import Session
import uvicorn

load_dotenv()

# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    await connect_to_db()
    yield  # This allows the app to run
    # Shutdown tasks
    await disconnect_from_db()

app = FastAPI(lifespan=lifespan)

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Smart Campus IoT API"}

# Trash Can Models
class TrashCanCreate(BaseModel):
    location: str
    id: str
    
    @field_validator('location')
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v

class TrashCanUpdate(BaseModel):
    location: str | None = None
    current_height: float | None = None
    max_height: float | None = None
    
    @field_validator('current_height', 'max_height')
    def validate_heights(cls, v):
        if v is not None and v < 0:
            raise ValueError('Height cannot be negative')
        return v

@app.post("/trashcan", response_model=dict)
async def create_trashcan(trashcan: TrashCanCreate):
    try:
        trash_can = await create_trash_can(trashcan.id, trashcan.location)
        if trash_can:
            return {
                "status": "success",
                "message": "Trash can created successfully",
                "data": {
                    "id": trash_can.id,
                    "location": trash_can.location,
                    "level": trash_can.level,
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create trash can")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trashcan/{trash_can_id}/status")
async def get_trashcan_status(trash_can_id: str):
    try:
        trash_can = await get_trash_can_status(trash_can_id)
        if not trash_can:
            raise HTTPException(status_code=404, detail="Trash can not found")
        return {
            "status": "success",
            "data": {
                "id": trash_can.id,
                "location": trash_can.location,
                "level": trash_can.level,
                "lastEmptied": trash_can.lastEmptied
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trashcans")
async def get_all_trashcans():
    try:
        trash_cans = await get_all_trash_cans()
        if not trash_cans:
            raise HTTPException(status_code=500, detail="Failed to fetch trash cans")
        return {
            "status": "success",
            "data": [
                {"id": can.id, "location": can.location, "level": can.level, "lastEmptied": can.lastEmptied}
                for can in trash_cans
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/trashcan/{trash_can_id}")
async def update_trashcan(trash_can_id: str, update_data: TrashCanUpdate):
    try:
        update_dict = update_data.dict(exclude_none=True)
        if not update_dict:
            raise HTTPException(status_code=400, detail="No valid update data provided")

        if update_dict.get('level') == 0:
            update_dict['lastEmptied'] = datetime.now()

        trash_can = await update_trash_can(trash_can_id, update_dict)

        if not trash_can:
            raise HTTPException(status_code=404, detail="Trash can not found")
        
        return {
            "status": "success",
            "message": "Trash can updated successfully",
            "data": {
                "id": trash_can.id,
                "location": trash_can.location,
                "level": trash_can.level,
                "lastEmptied": trash_can.lastEmptied
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/trashcan/{trash_can_id}")
async def delete_trashcan(trash_can_id: str):
    try:
        success = await delete_trash_can(trash_can_id)
        if not success:
            raise HTTPException(status_code=404, detail="Trash can not found")
        return {"status": "success", "message": "Trash can deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Light Models
class LightCreate(BaseModel):
    id: str
    location: str
    state: bool = False
    
    @field_validator('location')
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v

@app.post("/light")
async def create_light_endpoint(light: LightCreate):
    try:
        new_light = await create_light(light.id, light.location, light.state)
        if not new_light:
            raise HTTPException(status_code=500, detail="Failed to create light")
        return {
            "status": "success",
            "message": "Light created successfully",
            "data": new_light
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/light/{light_id}")
async def get_light_endpoint(light_id: str):
    try:
        light = await get_light(light_id)
        if not light:
            raise HTTPException(status_code=404, detail="Light not found")
        return {"status": "success", "data": light}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lights")
async def get_all_lights_endpoint():
    try:
        lights = await get_all_lights()
        if not lights:
            raise HTTPException(status_code=500, detail="Failed to fetch lights")
        return {"status": "success", "data": lights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/light/{light_id}")
async def update_light_endpoint(light_id: str, light: LightCreate):
    try:
        updated_light = await update_light(light_id, state=light.state, location=light.location)
        if not updated_light:
            raise HTTPException(status_code=404, detail="Light not found")
        return {"status": "success", "message": "Light updated successfully", "data": updated_light}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/light/{light_id}")
async def delete_light_endpoint(light_id: str):
    try:
        success = await delete_light(light_id)
        if not success:
            raise HTTPException(status_code=404, detail="Light not found")
        return {"status": "success", "message": "Light deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fire Alarm Models
class FireAlarmCreate(BaseModel):
    location: str

@app.post("/fire-alarm/")
def create_fire_alarm(data: FireAlarmCreate, db: Session = Depends(get_db)):
    alarm = FireAlarm(location=data.location, active=True)
    db.add(alarm)
    db.commit()
    db.refresh(alarm)
    return {"message": "Fire alarm triggered!", "alarm": alarm}

@app.get("/fire-alarms/")
def get_fire_alarms(db: Session = Depends(get_db)):
    alarms = db.query(FireAlarm).all()
    return alarms

@app.put("/fire-alarm/{alarm_id}")
def deactivate_fire_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = db.query(FireAlarm).filter(FireAlarm.id == alarm_id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    alarm.active = False
    db.commit()
    return {"message": "Fire alarm deactivated!", "alarm": alarm}

@app.post("/esp/fire-alarm/")
def esp_trigger_fire_alarm(location: str, db: Session = Depends(get_db)):
    return create_fire_alarm(location, db)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)
