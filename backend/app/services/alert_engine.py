import json
from datetime import datetime
from backend.app.models.db_models import Alert

def generate_multilingual_translations(title, severity):
    # Mock translation generator based on severity
    if severity == "CRITICAL":
        return json.dumps({
            "en": f"EMERGENCY: {title}. Immediate action required.",
            "hi": f"आपातकाल: {title}। तत्काल कार्रवाई की आवश्यकता है।",
            "as": f"জৰুৰী অৱস্থা: {title}. লগে লগে ব্যৱস্থা গ্ৰহণৰ প্ৰয়োজন।",
            "bn": f"জরুরী অবস্থা: {title}. অবিলম্বে ব্যবস্থা প্রয়োজন।"
        })
    elif severity == "WARNING":
        return json.dumps({
            "en": f"WARNING: {title}. Please stay alert.",
            "hi": f"चेतावनी: {title}। कृपया सतर्क रहें।",
            "as": f"সতৰ্কবাণী: {title}. অনুগ্ৰহ কৰি সতৰ্ক থাকক।",
            "bn": f"সতর্কতা: {title}. দয়া করে সতর্ক থাকুন।"
        })
    return json.dumps({"en": title})

def evaluate_risk_and_alert(db, lat, lng, risk_score, risk_level, location_name, state, reason):
    severity = None
    if risk_level == "HIGH":
        severity = "WARNING"
    elif risk_level == "CRITICAL":
        severity = "CRITICAL"
        
    if severity:
        title = f"{severity.capitalize()} Alert: {location_name}"
        alert = Alert(
            title=title,
            severity=severity,
            status="ACTIVE",
            state=state,
            latitude=lat,
            longitude=lng,
            radius_km=10.0,
            description=f"Risk Score: {risk_score:.2f}. Reason: {reason}",
            issued_at=datetime.now(datetime.UTC),
            translations_json=generate_multilingual_translations(title, severity)
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
    return None

def get_active_alerts(db):
    return db.query(Alert).filter(Alert.status == "ACTIVE").all()

def acknowledge_alert(db, alert_id):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert and alert.status == "ACTIVE":
        alert.status = "ACKNOWLEDGED"
        db.commit()
        db.refresh(alert)
    return alert

def resolve_alert(db, alert_id):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert and alert.status in ["ACTIVE", "ACKNOWLEDGED"]:
        alert.status = "RESOLVED"
        alert.resolved_at = datetime.now(datetime.UTC)
        db.commit()
        db.refresh(alert)
    return alert
