from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .redis_client import get_redis
from .models import Base
from .controllers import auth_controller, bill_data_controller, user_controller,report_controller,search_controller
from .controllers.webhook import router as webhook_router
import asyncio
from app.scheduler import reset_khach_moi
app = FastAPI(title="FastAPI Project")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://localhost:3002",
        "http://45.32.104.37:3002",
        "https://bill.buivankien.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_controller.router, tags=["authentication"])
app.include_router(user_controller.router, prefix="/user", tags=["users"])
app.include_router(bill_data_controller.router, prefix="/hoa-don", tags=["hoadon"])
app.include_router(report_controller.router, prefix="/report", tags=["report"])
app.include_router(search_controller.router, prefix="/seacrhsocial", tags=["seacrhsocial"])
app.include_router(webhook_router)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    redis = await get_redis()
    pong = await redis.ping()
    if pong:
        print("✅ Redis connected")
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Project"} 

@app.on_event("startup")
async def startup():
    asyncio.create_task(reset_khach_moi())