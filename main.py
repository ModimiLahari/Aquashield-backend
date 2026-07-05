from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

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

# --- LIVE WEBSOCKET MANAGER FOR DYNAMIC ALERTS ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # क्लाइंट से आने वाले किसी भी मैसेज को रीड करने के लिए
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- INCLUDE ROUTERS ---
app.include_router(sensor_router)
app.include_router(ai_router)
