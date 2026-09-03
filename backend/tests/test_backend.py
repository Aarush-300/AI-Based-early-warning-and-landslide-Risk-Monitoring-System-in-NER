from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import init_db, SessionLocal
from backend.app import seed_data

# Ensure tables and seed data exist for test client
init_db()
db = SessionLocal()
try:
    seed_data.run_seed(db)
finally:
    db.close()

client = TestClient(app)

def test_platform_info():
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "TerrainTrace" in data["platform"]
    assert len(data["supported_states"]) == 8

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_gis_layers():
    res_states = client.get("/api/v1/gis/states")
    assert res_states.status_code == 200
    assert len(res_states.json()) == 8
    
    res_highways = client.get("/api/v1/gis/highways")
    assert res_highways.status_code == 200
    assert len(res_highways.json()) >= 6
    
    res_heatmap = client.get("/api/v1/gis/risk-heatmap")
    assert res_heatmap.status_code == 200
    assert len(res_heatmap.json()) > 10

def test_prediction_engine():
    payload = {
        "lat": 25.1324,
        "lng": 92.3682,
        "slope_deg": 38.0,
        "elevation_m": 1200.0,
        "rainfall_3d_mm": 210.0,
        "rainfall_24h_mm": 85.0,
        "soil_moisture_pct": 89.0,
        "inclinometer_tilt_rate_mm_day": 12.0
    }
    response = client.post("/api/v1/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["ORANGE", "RED"]
    assert data["factor_of_safety"] > 0
    assert len(data["recommendations"]) > 0

def test_alerts_and_cap():
    res_alerts = client.get("/api/v1/alerts/")
    assert res_alerts.status_code == 200
    assert len(res_alerts.json()) >= 2
    
    res_cap = client.get("/api/v1/alerts/cap-feed.xml")
    assert res_cap.status_code == 200
    assert "urn:oasis:names:tc:emergency:cap:1.2" in res_cap.text

def test_reports_and_vision():
    payload = {
        "reporter_name": "BRO Officer Testing",
        "reporter_role": "BRO Engineer",
        "lat": 27.062,
        "lng": 88.432,
        "landmark": "Teesta Highway Marker 28",
        "state": "Sikkim",
        "district": "East Sikkim",
        "hazard_type": "Tension Cracks",
        "road_passable": False,
        "description": "Test crack reported"
    }
    response = client.post("/api/v1/reports/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("REP-") or data["id"].startswith("DB-REP-")
    assert data["ai_analysis"]["hazard_detected"] is True

def test_roads_and_priority():
    res_roads = client.get("/api/v1/roads/")
    assert res_roads.status_code == 200
    roads = res_roads.json()
    assert len(roads) >= 5
    assert "calculated_priority_score" in roads[0]
