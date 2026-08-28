import os
import uuid
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from backend.app.models.schemas import FieldReportCreate, FieldReportResponse
from backend.app.ml.vision_model import vision_engine
from backend.app.core.config import settings

router = APIRouter(prefix="/reports", tags=["Citizen & Field Reporting"])

# In-memory storage for rapid demo with pre-seeded realistic reports
REPORTS_DB: List[Dict[str, Any]] = [
    {
        "id": "REP-2026-001",
        "reporter_name": "Tsering Lepcha",
        "reporter_role": "Border Roads Sub-Engineer",
        "lat": 27.0615,
        "lng": 88.4318,
        "landmark": "29th Mile Sharp Bend, NH-10",
        "state": "Sikkim",
        "district": "East Sikkim",
        "hazard_type": "Tension Cracks",
        "road_passable": False,
        "description": "Longitudinal tension crack expanding rapidly across retaining wall crown. Seepage water spurting through weep holes.",
        "image_url": "/static_demo/sample_crack.jpg",
        "ai_analysis": {
            "hazard_detected": True,
            "hazard_classification": "Tension Crack Network (Structural Precursor)",
            "severity_level": "CRITICAL",
            "confidence_score": 0.94,
            "detected_features": ["High-density linear fracture network", "Retaining wall toe shear displacement"],
            "estimated_crack_width_mm": 68.5,
            "debris_volume_estimate": "Pre-failure tension crack formation (< 50 m³)",
            "action_priority": "IMMEDIATE_INTERVENTION",
            "ai_remarks": "Crack width exceeds critical 50mm safety threshold. Road failure imminent within 6-12 hours under rainfall."
        },
        "status": "VERIFIED",
        "created_at": "2026-08-28T19:30:00Z"
    },
    {
        "id": "REP-2026-002",
        "reporter_name": "Lalthanmawia",
        "reporter_role": "Citizen Commuter",
        "lat": 25.1320,
        "lng": 92.3685,
        "landmark": "Sonapur Tunnel North Approach, NH-06",
        "state": "Meghalaya",
        "district": "East Jaintia Hills",
        "hazard_type": "Mudslide",
        "road_passable": False,
        "description": "Massive torrent of wet mud and boulders has engulfed the road over 100 meters. Both lanes blocked, 4 trucks stranded.",
        "image_url": "/static_demo/sample_mudslide.jpg",
        "ai_analysis": {
            "hazard_detected": True,
            "hazard_classification": "Massive Mudflow / Debris Avalanche",
            "severity_level": "CRITICAL",
            "confidence_score": 0.96,
            "detected_features": ["Extensive exposed saturated mud/colluvium", "Debris boulder / aggregate accumulation on surface"],
            "estimated_crack_width_mm": 110.0,
            "debris_volume_estimate": "High (> 500 m³ estimate)",
            "action_priority": "IMMEDIATE_INTERVENTION",
            "ai_remarks": "Total corridor blockage. Unstable upper scarp requires heavy tracked excavators and safety spotters."
        },
        "status": "VERIFIED",
        "created_at": "2026-08-28T21:15:00Z"
    },
    {
        "id": "REP-2026-003",
        "reporter_name": "Kevichusa Angami",
        "reporter_role": "Traffic Police Kohima",
        "lat": 25.7210,
        "lng": 93.9215,
        "landmark": "Dzüdza River Bridge Ascent, NH-29",
        "state": "Nagaland",
        "district": "Kohima",
        "hazard_type": "Road Sinking",
        "road_passable": True,
        "description": "Pavement sinking by approx 8 inches on downhill side. Single light vehicles passing carefully.",
        "image_url": "/static_demo/sample_subsidence.jpg",
        "ai_analysis": {
            "hazard_detected": True,
            "hazard_classification": "Active Slope Slumping & Subsidence",
            "severity_level": "HIGH",
            "confidence_score": 0.88,
            "detected_features": ["Surface deformation and slope texture irregularities", "Differential asphalt subsidence scarp"],
            "estimated_crack_width_mm": 24.0,
            "debris_volume_estimate": "Moderate (~ 150 - 300 m³)",
            "action_priority": "URGENT_INSPECTION",
            "ai_remarks": "Downhill shoulder destabilized. Heavy multi-axle freight carriers must be diverted to prevent sudden culvert collapse."
        },
        "status": "INVESTIGATING",
        "created_at": "2026-08-29T00:45:00Z"
    }
]

@router.get("/")
def get_reports(state: Optional[str] = None, hazard_type: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    results = REPORTS_DB
    if state:
        results = [r for r in results if r["state"].lower() == state.lower()]
    if hazard_type:
        results = [r for r in results if r["hazard_type"].lower() == hazard_type.lower()]
    if status:
        results = [r for r in results if r["status"].lower() == status.lower()]
    return results

@router.post("/submit")
def submit_report(report_data: FieldReportCreate) -> Dict[str, Any]:
    report_id = f"REP-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:5].upper()}"
    
    ai_result = None
    image_saved_url = None
    
    if report_data.image_base64:
        # Run AI Vision Analysis
        ai_result = vision_engine.analyze_base64(report_data.image_base64, report_data.hazard_type)
        
        # Save image file to upload directory
        try:
            raw_b64 = report_data.image_base64
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",")[1]
            img_bytes = base64.b64decode(raw_b64)
            filename = f"{report_id}.jpg"
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(img_bytes)
            image_saved_url = f"/uploads/{filename}"
        except Exception:
            image_saved_url = None
    else:
        # Generate baseline AI assessment from metadata
        ai_result = {
            "hazard_detected": True,
            "hazard_classification": report_data.hazard_type,
            "severity_level": "HIGH" if not report_data.road_passable else "MODERATE",
            "confidence_score": 0.82,
            "detected_features": ["Citizen reported blockage", "Physical field obstruction"],
            "estimated_crack_width_mm": 20.0,
            "debris_volume_estimate": "Estimated based on report description",
            "action_priority": "URGENT_INSPECTION" if not report_data.road_passable else "ROUTINE_MONITORING",
            "ai_remarks": "Report logged into disaster queue. Verification team notified."
        }

    new_report = {
        "id": report_id,
        "reporter_name": report_data.reporter_name or "Anonymous Citizen",
        "reporter_role": report_data.reporter_role,
        "lat": report_data.lat,
        "lng": report_data.lng,
        "landmark": report_data.landmark,
        "state": report_data.state,
        "district": report_data.district,
        "hazard_type": report_data.hazard_type,
        "road_passable": report_data.road_passable,
        "description": report_data.description,
        "image_url": image_saved_url,
        "ai_analysis": ai_result,
        "status": "VERIFIED" if ai_result and ai_result.get("severity_level") == "CRITICAL" else "INVESTIGATING",
        "created_at": (report_data.offline_created_at.isoformat() + "Z") if report_data.offline_created_at else (datetime.utcnow().isoformat() + "Z")
    }
    
    REPORTS_DB.insert(0, new_report)
    return new_report

@router.post("/sync-offline")
def sync_offline_reports(reports: List[FieldReportCreate]) -> Dict[str, Any]:
    """
    Bulk synchronization endpoint for field reports queued locally in IndexedDB
    during cellular outages in remote hill tracts.
    """
    synced_count = 0
    synced_ids = []
    
    for item in reports:
        res = submit_report(item)
        synced_count += 1
        synced_ids.append(res["id"])
        
    return {
        "message": f"Successfully synchronized {synced_count} offline field reports.",
        "synced_count": synced_count,
        "synced_ids": synced_ids
    }

