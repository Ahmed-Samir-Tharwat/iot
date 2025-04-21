from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import shutil
from contextlib import asynccontextmanager
import uuid
from database import connect_to_db, disconnect_from_db, save_user_image
import auto_attendance.ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    await connect_to_db()
    yield  # This allows the app to run
    # Shutdown tasks
    await disconnect_from_db()

app = FastAPI(lifespan=lifespan)

router = APIRouter()