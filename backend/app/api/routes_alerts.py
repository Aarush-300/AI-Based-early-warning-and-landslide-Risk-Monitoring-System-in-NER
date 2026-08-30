from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import datetime
import json

from backend.app.database import get_db
from backend.app.models.db_models import Alert
from backend.app.models.schemas import AlertCreate, AlertItem
from backend.app.auth.auth_service import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts & CAP"])

@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()
    result = []
    for a in alerts:
        translations = {}
        if a.translations_json:
            try:
                translations = json.loads(a.translations_json)
            except Exception:
                pass
        
        result.append({
            "id": str(a.id),
            "title": a.title,
            "severity": a.severity,
            "location_name": a.location_name,
            "state": a.state,
            "risk_score": a.risk_score,
            "reason": a.reason,
            "recommended_action": a.recommended_action,
            "source": a.source,
            "status": a.status,
            "created_at": a.created_at.isoformat() + "Z" if a.created_at else None,
            "translations": translations,
            "category": a.category,
            "district": a.district
        })
    return result

@router.post("/broadcast")
def broadcast_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    translations_json = "{}"
    if alert.translations:
        translations_json = json.dumps(alert.translations)
        
    db_alert = Alert(
        title=alert.title,
        severity=alert.severity,
        category=alert.category,
        location_name=alert.location_name,
        state=alert.state,
        district=alert.district,
        lat=alert.lat,
        lng=alert.lng,
        risk_score=alert.risk_score,
        reason=alert.reason or alert.description,
        recommended_action=alert.recommended_action or (", ".join(alert.instructions) if alert.instructions else ""),
        source=alert.source,
        translations_json=translations_json,
        status="ACTIVE"
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    translations = {}
    if db_alert.translations_json:
        try:
            translations = json.loads(db_alert.translations_json)
        except:
            pass
            
    return {
        "id": str(db_alert.id),
        "title": db_alert.title,
        "severity": db_alert.severity,
        "location_name": db_alert.location_name,
        "state": db_alert.state,
        "risk_score": db_alert.risk_score,
        "reason": db_alert.reason,
        "recommended_action": db_alert.recommended_action,
        "source": db_alert.source,
        "status": db_alert.status,
        "created_at": db_alert.created_at.isoformat() + "Z" if db_alert.created_at else None,
        "translations": translations,
        "category": db_alert.category,
        "district": db_alert.district
    }

@router.patch("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "ACKNOWLEDGED"
    alert.acknowledged_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Alert acknowledged", "id": alert_id}

@router.patch("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "RESOLVED"
    alert.resolved_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Alert resolved", "id": alert_id}

@router.get("/cap-feed.xml")
def cap_feed(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.status == "ACTIVE").all()
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<alerts xmlns="urn:oasis:names:tc:emergency:cap:1.2">')
    for a in alerts:
        xml.append('  <alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">')
        xml.append(f'    <identifier>{a.id}</identifier>')
        xml.append(f'    <sender>{a.source or "TerrainTrace-NER"}</sender>')
        xml.append(f'    <sent>{a.created_at.isoformat() if a.created_at else ""}</sent>')
        xml.append(f'    <status>Actual</status>')
        xml.append(f'    <msgType>Alert</msgType>')
        xml.append('    <info>')
        xml.append(f'      <category>{a.category}</category>')
        xml.append(f'      <event>{a.title}</event>')
        xml.append(f'      <urgency>Immediate</urgency>')
        xml.append(f'      <severity>{a.severity}</severity>')
        xml.append(f'      <certainty>Observed</certainty>')
        xml.append(f'      <headline>{a.title}</headline>')
        xml.append(f'      <description>{a.reason}</description>')
        xml.append(f'      <instruction>{a.recommended_action}</instruction>')
        xml.append('      <area>')
        xml.append(f'        <areaDesc>{a.location_name}, {a.district}, {a.state}</areaDesc>')
        xml.append('      </area>')
        xml.append('    </info>')
        xml.append('  </alert>')
    xml.append('</alerts>')
    
    return Response(content="\n".join(xml), media_type="application/xml")
