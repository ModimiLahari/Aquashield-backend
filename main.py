from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.sensor import router as sensor_router
from routers.ai import router as ai_router

app = FastAPI(title="AquaShield Backend - Phase 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensor_router)
app.include_router(ai_router)