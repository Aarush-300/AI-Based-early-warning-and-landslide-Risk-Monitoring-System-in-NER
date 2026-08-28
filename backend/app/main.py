import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.api.routes_gis import router as gis_router
from backend.app.api.routes_predictions import router as predictions_router
from backend.app.api.routes_reports import router as reports_router
from backend.app.api.routes_alerts import router as alerts_router
from backend.app.api.routes_roads import router as roads_router
from backend.app.data.sensors_service import sensors_service

# Active WebSocket connections list
connected_clients: list[WebSocket] = []

async def telemetry_background_ticker():
    """Background simulator task pushing real-time sensor updates to all connected UI clients"""
    while True:
        try:
            await asyncio.sleep(4.0)
            sensors_service.tick_simulation()
            
            if connected_clients:
                payload = {
                    "event": "TELEMETRY_TICK",
                    "sensors": sensors_service.get_all_sensors()
                }
                for ws in list(connected_clients):
                    try:
                        await ws.send_json(payload)
                    except Exception:
                        if ws in connected_clients:
                            connected_clients.remove(ws)
        except asyncio.CancelledError:
            break
        except Exception:
            pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch background sensor telemetry ticker
    ticker_task = asyncio.create_task(telemetry_background_ticker())
    yield
    # Shutdown
    ticker_task.cancel()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Enabled Real-Time Landslide Early Warning, GIS Monitoring & Crowdsourced Reporting Platform for the North Eastern Region of India.",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static uploads directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API Routers
app.include_router(gis_router, prefix=settings.API_V1_STR)
app.include_router(predictions_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(alerts_router, prefix=settings.API_V1_STR)
app.include_router(roads_router, prefix=settings.API_V1_STR)

@app.get("/api/info")
def platform_info():
    return {
        "platform": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "region": "North Eastern Region (NER), India",
        "supported_states": settings.NER_STATES,
        "supported_languages": [l["name"] for l in settings.LANGUAGES],
        "status": "OPERATIONAL",
        "docs_url": "/docs",
        "cap_feed_url": f"{settings.API_V1_STR}/alerts/cap-feed.xml"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "active_iot_nodes": len(sensors_service.get_all_sensors()),
        "connected_ws_clients": len(connected_clients)
    }

@app.websocket("/ws/live")
async def websocket_live_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    # Send initial snapshot immediately
    await websocket.send_json({
        "event": "INITIAL_SNAPSHOT",
        "sensors": sensors_service.get_all_sensors()
    })
    try:
        while True:
            data = await websocket.receive_text()
            if data == "PING":
                await websocket.send_text("PONG")
    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
    except Exception:
        if websocket in connected_clients:
            connected_clients.remove(websocket)

# Mount built frontend assets if present
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api") or full_path.startswith("uploads") or full_path.startswith("ws"):
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

