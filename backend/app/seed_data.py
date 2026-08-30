"""
TerrainTrace-NER Database Seed Script
Populates the database with realistic NER demo data.
Idempotent — safe to run multiple times.
"""
import json
import datetime

from backend.app.database import SessionLocal, init_db
from backend.app.models.db_models import User, Location, Shelter, Alert, FieldReport, Road
from backend.app.auth.auth_service import hash_password
from backend.app.data.ner_geodata import NER_STATES_DATA, EMERGENCY_RESOURCES, HIGHWAY_CORRIDORS


def run_seed(db):
    """Seed all demo data. Idempotent."""
    _seed_users(db)
    _seed_locations(db)
    _seed_shelters(db)
    _seed_roads(db)
    _seed_alerts(db)
    _seed_reports(db)
    db.commit()


def _seed_users(db):
    if db.query(User).first():
        return
    users = [
        User(
            username="admin", email="admin@terraintrace.gov.in",
            hashed_password=hash_password("admin123"),
            full_name="Platform Admin", role="admin"
        ),
        User(
            username="officer", email="rajesh.kumar@sdma.gov.in",
            hashed_password=hash_password("officer123"),
            full_name="Dr. Rajesh Kumar", role="officer", state="Meghalaya"
        ),
        User(
            username="field1", email="bikash.nath@sdrf.gov.in",
            hashed_password=hash_password("field123"),
            full_name="Bikash Nath", role="field_officer", state="Assam"
        ),
        User(
            username="citizen", email="aarush@example.com",
            hashed_password=hash_password("citizen123"),
            full_name="Aarush Sharma", role="citizen"
        ),
    ]
    db.add_all(users)
    db.flush()


def _seed_locations(db):
    if db.query(Location).first():
        return
    for st in NER_STATES_DATA:
        db.add(Location(
            name=st["name"],
            location_type="state",
            state=st["name"],
            district=st.get("capital", ""),
            lat=st["center"][0],
            lng=st["center"][1],
            geology=st.get("geology", ""),
            population=st.get("population", 0)
        ))
    db.flush()


def _seed_shelters(db):
    if db.query(Shelter).first():
        return
    for res in EMERGENCY_RESOURCES:
        db.add(Shelter(
            name=res["name"],
            shelter_type=res["type"],
            state=res["state"],
            district=res.get("district", ""),
            lat=res["lat"],
            lng=res["lng"],
            capacity_persons=res.get("capacity_persons", 0),
            contact=res.get("contact", ""),
            is_operational=True
        ))
    db.flush()


def _seed_roads(db):
    if db.query(Road).first():
        return
    for hw in HIGHWAY_CORRIDORS:
        db.add(Road(
            corridor_id=hw["corridor_id"],
            highway_name=hw["highway_name"],
            stretch_name=hw.get("stretch_name", ""),
            state=hw.get("state", ""),
            risk_level=hw.get("risk_level", "GREEN"),
            status=hw.get("status", "OPEN"),
            blockage_cause=hw.get("blockage_cause", ""),
            clearing_eta_hours=hw.get("clearing_eta_hours", 0),
            stranded_vehicles_estimate=hw.get("stranded_vehicles_estimate", 0),
            alternate_route=hw.get("alternate_route", ""),
            priority_score=hw.get("priority_score", 0.0)
        ))
    db.flush()


def _seed_alerts(db):
    if db.query(Alert).first():
        return
    now = datetime.datetime.now(datetime.timezone.utc)
    alerts = [
        Alert(
            title="CRITICAL: Active debris flow detected near Sonapur Tunnel, NH-06",
            severity="EMERGENCY",
            category="Landslide",
            location_name="Sonapur Tunnel, NH-06",
            state="Meghalaya",
            district="East Jaintia Hills",
            lat=25.1324, lng=92.3682,
            risk_score=0.92,
            reason="Heavy 72h rainfall (210mm) combined with steep slope (42°) and high soil saturation (91%)",
            recommended_action="Evacuate 500m radius. Close NH-06 corridor. Deploy BRO clearance team.",
            source="AI Risk Engine",
            status="ACTIVE",
            translations_json=json.dumps({
                "hi": {"title": "गंभीर: सोनापुर सुरंग NH-06 के पास सक्रिय मलबा प्रवाह"},
                "as": {"title": "সংকটজনক: সোণাপুৰ সুৰংগ NH-06 ৰ ওচৰত সক্ৰিয় ধ্বংসাৱশেষ"},
                "bn": {"title": "জরুরি: সোনাপুর টানেল NH-06 এর কাছে সক্রিয় ধ্বসের প্রবাহ"}
            }),
            created_at=now - datetime.timedelta(hours=2)
        ),
        Alert(
            title="WARNING: Increasing slope instability on NH-10 near 29th Mile, Teesta Valley",
            severity="WARNING",
            category="Slope Failure",
            location_name="29th Mile, Teesta Valley, NH-10",
            state="Sikkim",
            district="East Sikkim",
            lat=27.0620, lng=88.4325,
            risk_score=0.71,
            reason="Inclinometer displacement rate exceeding 5mm/day. Soil moisture at 83%.",
            recommended_action="Restrict night travel. Deploy highway patrol. Monitor every 30 min.",
            source="AI Risk Engine",
            status="ACTIVE",
            translations_json=json.dumps({
                "hi": {"title": "चेतावनी: तीस्ता घाटी NH-10 पर ढलान अस्थिरता बढ़ रही है"}
            }),
            created_at=now - datetime.timedelta(hours=5)
        ),
        Alert(
            title="WATCH: Elevated rainfall accumulation in Dima Hasao district",
            severity="WATCH",
            category="Rainfall",
            location_name="Jatinga, Dima Hasao",
            state="Assam",
            district="Dima Hasao",
            lat=25.1215, lng=92.9820,
            risk_score=0.48,
            reason="72h rainfall accumulation of 95mm. Monitor for further intensification.",
            recommended_action="Maintain vigilance. Check drainage infrastructure.",
            source="Weather Monitoring",
            status="ACTIVE",
            created_at=now - datetime.timedelta(hours=8)
        ),
    ]
    db.add_all(alerts)
    db.flush()


def _seed_reports(db):
    if db.query(FieldReport).first():
        return
    now = datetime.datetime.now(datetime.timezone.utc)
    reports = [
        FieldReport(
            reporter_name="Bikash Nath",
            reporter_role="Field Official",
            hazard_type="Tension Cracks",
            state="Meghalaya",
            district="East Jaintia Hills",
            landmark="500m before Sonapur Tunnel entry, near river bend culvert",
            description="Multiple transverse cracks observed across carriageway. Widening visible over last 48h.",
            lat=25.1324, lng=92.3682,
            road_passable=True,
            image_path="/uploads/sample_crack.jpg",
            status="VERIFIED",
            severity="HIGH",
            ai_hazard_classification="Tension Crack Network (Grade III)",
            ai_severity_level="HIGH",
            ai_confidence_score=0.87,
            ai_crack_width_mm=12.5,
            ai_debris_volume="Low (<5 m³)",
            ai_remarks="Multiple sub-parallel extensional fractures. Indicates active crown retreat.",
            created_at=now - datetime.timedelta(hours=3)
        ),
        FieldReport(
            reporter_name="Anonymous Citizen",
            reporter_role="Citizen",
            hazard_type="Active Rockfall",
            state="Sikkim",
            district="East Sikkim",
            landmark="NH-10 near Rangpo bridge, km marker 28",
            description="Rocks falling intermittently from cut slope above road. Traffic slowing.",
            lat=27.1750, lng=88.5265,
            road_passable=True,
            status="VERIFIED",
            severity="MODERATE",
            ai_hazard_classification="Rockfall Zone",
            ai_severity_level="MODERATE",
            ai_confidence_score=0.72,
            created_at=now - datetime.timedelta(hours=6)
        ),
        FieldReport(
            reporter_name="Traffic Police Gangtok",
            reporter_role="Traffic Police",
            hazard_type="Mudslide",
            state="Nagaland",
            district="Kohima",
            landmark="NH-29 Kohima-Dimapur stretch, near Dzudza Bridge",
            description="Mudslide blocking one lane. Heavy equipment needed for clearance.",
            lat=25.7225, lng=93.9230,
            road_passable=False,
            image_path="/uploads/sample_mudslide.jpg",
            status="PENDING",
            severity="HIGH",
            ai_hazard_classification="Debris Flow / Mudslide",
            ai_severity_level="HIGH",
            ai_confidence_score=0.81,
            ai_debris_volume="Medium (5-50 m³)",
            created_at=now - datetime.timedelta(hours=1)
        ),
    ]
    db.add_all(reports)
    db.flush()


if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        run_seed(db)
        print("Database seeded successfully.")
    finally:
        db.close()
