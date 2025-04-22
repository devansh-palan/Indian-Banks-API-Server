from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connected")
    yield
    await database.disconnect()
    print("Database disconnected")

app = FastAPI(lifespan=lifespan, title="Bank API", description="API for managing bank data")

app.include_router(router, prefix="/api/v1", tags=["banks"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Bank API"}