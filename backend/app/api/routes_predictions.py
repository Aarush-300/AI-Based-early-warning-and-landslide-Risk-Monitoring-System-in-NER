from fastapi import APIRouter, Query
from typing import Dict, Any, List, Optional
from backend.app.models.schemas import LandslideRiskPredictionRequest, LandslideRiskPredictionResponse
from backend.app.ml.landslide_model import landslide_engine
from backend.app.data.weather_service import weather_service
from backend.app.data.sensors_service import sensors_service
from backend.app.data.ner_geodata import HIGHWAY_CORRIDORS

router = APIRouter(prefix="/predict", tags=["AI Predictive Analytics"])

@router.post("/", response_model=LandslideRiskPredictionResponse)
def predict_landslide_risk(req: LandslideRiskPredictionRequest) -> Dict[str, Any]:
    # If parameters not supplied, enrich with weather service
    if req.rainfall_24h_mm is None or req.rainfall_3d_mm is None:
        weather = weather_service.get_current_weather(req.lat, req.lng)
        rain_24h = weather["rainfall_24h_mm"]
        rain_3d = weather["rainfall_3d_mm"]
        soil_m = weather["relative_humidity_pct"] * 0.85
    else:
        rain_24h = req.rainfall_24h_mm
        rain_3d = req.rainfall_3d_mm
        soil_m = req.soil_moisture_pct or 70.0

    slope = req.slope_deg or 32.0
    elev = req.elevation_m or 1400.0
    tilt = req.inclinometer_tilt_rate_mm_day or 2.5
    litho = req.lithology or "Shale & Siltstone (Fragile)"

    result = landslide_engine.predict_risk(
        lat=req.lat,
        lng=req.lng,
        slope_deg=slope,
        elevation_m=elev,
        rainfall_3d_mm=rain_3d,
        rainfall_24h_mm=rain_24h,
        soil_moisture_pct=soil_m,
        inclinometer_tilt_rate_mm_day=tilt,
        lithology_type=litho
    )
    return result

@router.get("/weather-forecast")
def get_weather_forecast(lat: float = Query(25.5788), lng: float = Query(91.8933), location_name: str = Query("Shillong Plateau")) -> Dict[str, Any]:
    current_wx = weather_service.get_current_weather(lat, lng, location_name)
    forecast_72h = weather_service.get_72h_forecast(lat, lng)
    return {
        "current": current_wx,
        "forecast_72h": forecast_72h
    }

@router.get("/overview")
def get_regional_overview() -> Dict[str, Any]:
    sensors = sensors_service.get_all_sensors()
    highways = HIGHWAY_CORRIDORS
    
    red_corridors = [h for h in highways if h["risk_level"] == "RED"]
    orange_corridors = [h for h in highways if h["risk_level"] == "ORANGE"]
    blocked_corridors = [h for h in highways if "BLOCKED" in h["status"]]
    
    critical_sensors = [s for s in sensors if s["status"] == "CRITICAL"]
    warning_sensors = [s for s in sensors if s["status"] == "WARNING"]
    
    avg_soil_moisture = round(sum(s["soil_moisture_pct"] for s in sensors) / len(sensors), 1) if sensors else 72.0
    avg_rain_intensity = round(sum(s["current_rainfall_mm_h"] for s in sensors) / len(sensors), 1) if sensors else 14.5
    
    total_stranded_vehicles = sum(h["stranded_vehicles_estimate"] for h in highways)
    
    return {
        "system_status": "ACTIVE_MONITORING",
        "red_alert_zones_count": len(red_corridors) + len(critical_sensors),
        "orange_alert_zones_count": len(orange_corridors) + len(warning_sensors),
        "blocked_highways_count": len(blocked_corridors),
        "total_monitored_corridors": len(highways),
        "total_active_iot_nodes": len(sensors),
        "avg_soil_moisture_pct": avg_soil_moisture,
        "avg_rainfall_rate_mm_h": avg_rain_intensity,
        "total_stranded_vehicles_ner": total_stranded_vehicles,
        "highest_risk_sector": "Sonapur Tunnel (NH-06) & Teesta Valley (NH-10)"
    }

