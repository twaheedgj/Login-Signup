from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.main import init_db
from routes.auth import router as auth_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])