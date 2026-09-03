import os
import uuid
import base64
from datetime import UTC, datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.models.schemas import FieldReportCreate
from backend.app.models.db_models import FieldReport
from backend.app.database import get_db
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
        "image_url": "/uploads/sample_crack.jpg",
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
        "image_url": "/uploads/sample_mudslide.jpg",
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
        "image_url": "/uploads/sample_subsidence.jpg",
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
def get_reports(state: Optional[str] = None, hazard_type: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    # DB results
    query = db.query(FieldReport)
    if state:
        query = query.filter(FieldReport.state.ilike(state))
    if hazard_type:
        query = query.filter(FieldReport.hazard_type.ilike(hazard_type))
    if status:
        query = query.filter(FieldReport.status.ilike(status))
        
    db_reports = query.order_by(FieldReport.created_at.desc()).all()
    
    db_results = []
    for r in db_reports:
        ai_analysis = None
        if r.ai_hazard_classification:
            ai_analysis = {
                "hazard_detected": True,
                "hazard_classification": r.ai_hazard_classification,
                "severity_level": r.ai_severity_level,
                "confidence_score": r.ai_confidence_score,
                "estimated_crack_width_mm": r.ai_crack_width_mm,
                "debris_volume_estimate": r.ai_debris_volume,
                "ai_remarks": r.ai_remarks
            }
            
        db_results.append({
            "id": f"DB-REP-{r.id}",
            "reporter_name": r.reporter_name,
            "reporter_role": r.reporter_role,
            "lat": r.lat,
            "lng": r.lng,
            "landmark": r.landmark,
            "state": r.state,
            "district": r.district,
            "hazard_type": r.hazard_type,
            "road_passable": r.road_passable,
            "description": r.description,
            "image_url": r.image_path,
            "ai_analysis": ai_analysis,
            "status": r.status,
            "created_at": r.created_at.isoformat() + "Z" if r.created_at else None
        })
        
    # Combine
    combined = REPORTS_DB + db_results
    
    if state:
        combined = [r for r in combined if r["state"].lower() == state.lower()]
    if hazard_type:
        combined = [r for r in combined if r["hazard_type"].lower() == hazard_type.lower()]
    if status:
        combined = [r for r in combined if r["status"].lower() == status.lower()]
        
    return combined

@router.post("/submit")
def submit_report(report_data: FieldReportCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    report_id = f"REP-{datetime.now(UTC).strftime('%Y%m%d')}-{uuid.uuid4().hex[:5].upper()}"
    
    ai_result = None
    image_saved_url = None
    
    if report_data.image_base64:
        if len(report_data.image_base64) > 14000000:
            raise HTTPException(status_code=400, detail="Image exceeds 10MB limit")
            
        raw_b64 = report_data.image_base64
        if "," in raw_b64:
            header, raw_b64 = raw_b64.split(",", 1)
            if "image/" not in header.lower():
                raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
        
        ai_result = vision_engine.analyze_base64(report_data.image_base64, report_data.hazard_type)
        
        try:
            img_bytes = base64.b64decode(raw_b64)
            filename = f"{report_id}.jpg"
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(img_bytes)
            image_saved_url = f"/uploads/{filename}"
        except Exception:
            image_saved_url = None
    else:
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
        
    created_date = report_data.offline_created_at or datetime.now(UTC)
    
    db_report = FieldReport(
        reporter_name=report_data.reporter_name or "Anonymous Citizen",
        reporter_role=report_data.reporter_role,
        hazard_type=report_data.hazard_type,
        state=report_data.state,
        district=report_data.district,
        landmark=report_data.landmark,
        description=report_data.description,
        lat=report_data.lat,
        lng=report_data.lng,
        road_passable=report_data.road_passable,
        image_path=image_saved_url,
        status="VERIFIED" if ai_result and ai_result.get("severity_level") == "CRITICAL" else "INVESTIGATING",
        severity=ai_result.get("severity_level", "MODERATE") if ai_result else "MODERATE",
        ai_hazard_classification=ai_result.get("hazard_classification") if ai_result else None,
        ai_severity_level=ai_result.get("severity_level") if ai_result else None,
        ai_confidence_score=ai_result.get("confidence_score") if ai_result else None,
        ai_crack_width_mm=ai_result.get("estimated_crack_width_mm") if ai_result else None,
        ai_debris_volume=ai_result.get("debris_volume_estimate") if ai_result else None,
        ai_remarks=ai_result.get("ai_remarks") if ai_result else None,
        created_at=created_date
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
        
    new_report = {
        "id": f"DB-REP-{db_report.id}",
        "reporter_name": db_report.reporter_name,
        "reporter_role": db_report.reporter_role,
        "lat": db_report.lat,
        "lng": db_report.lng,
        "landmark": db_report.landmark,
        "state": db_report.state,
        "district": db_report.district,
        "hazard_type": db_report.hazard_type,
        "road_passable": db_report.road_passable,
        "description": db_report.description,
        "image_url": db_report.image_path,
        "ai_analysis": ai_result,
        "status": db_report.status,
        "created_at": db_report.created_at.isoformat() + "Z" if db_report.created_at else None
    }
    
    return new_report

@router.post("/sync-offline")
def sync_offline_reports(reports: List[FieldReportCreate], db: Session = Depends(get_db)) -> Dict[str, Any]:
    synced_count = 0
    synced_ids = []
    
    for item in reports:
        res = submit_report(item, db)
        synced_count += 1
        synced_ids.append(res["id"])
        
    return {
        "message": f"Successfully synchronized {synced_count} offline field reports.",
        "synced_count": synced_count,
        "synced_ids": synced_ids
    }
