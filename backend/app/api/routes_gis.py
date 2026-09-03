import logging
from fastapi import APIRouter
from typing import Dict, Any, List
from typing import Dict, Any, List, Optional
from backend.app.data.ner_geodata import (
    NER_STATES_DATA,
    HIGHWAY_CORRIDORS,
    IOT_SENSOR_STATIONS,
    HISTORICAL_LANDSLIDES,
    EMERGENCY_RESOURCES
)
from backend.app.data.sensors_service import sensors_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gis", tags=["GIS Data Layers"])

# ---------------------------------------------------------------------------
#  In-memory cache for predicted risk locations (computed once per server run)
# ---------------------------------------------------------------------------
_predicted_risk_cache: Dict[str, Any] | None = None
_predicted_risk_cache: Optional[Dict[str, Any]] = None


def _build_predicted_risk_geojson() -> Dict[str, Any]:
    """
    For every demo location, fabricate *only* the environmental inputs and
    then pass them through LandslidePredictiveEngine.predict_risk().
    The returned risk_level / risk_score is determined entirely by the model.
    """
    from backend.app.data.demo_risk_locations import DEMO_RISK_LOCATIONS
    from backend.app.ml.landslide_model import landslide_engine

    features: List[Dict[str, Any]] = []

    for loc in DEMO_RISK_LOCATIONS:
        try:
            prediction = landslide_engine.predict_risk(
                lat=loc["lat"],
                lng=loc["lng"],
                slope_deg=loc["slope_deg"],
                elevation_m=loc["elevation_m"],
                rainfall_3d_mm=loc["rainfall_3d_mm"],
                rainfall_24h_mm=loc["rainfall_24h_mm"],
                soil_moisture_pct=loc["soil_moisture_pct"],
                inclinometer_tilt_rate_mm_day=loc["inclinometer_tilt_rate_mm_day"],
                lithology_type=loc["lithology_type"],
            )
        except Exception as exc:
            logger.warning("predict_risk failed for %s: %s", loc["location_name"], exc)
            continue

        # Merge location metadata into the prediction properties
        properties = {
            "location_name": loc["location_name"],
            "state": loc["state"],
            # Simulated inputs (for display in popup)
            "slope_deg": loc["slope_deg"],
            "elevation_m": loc["elevation_m"],
            "rainfall_3d_mm": loc["rainfall_3d_mm"],
            "rainfall_24h_mm": loc["rainfall_24h_mm"],
            "soil_moisture_pct": loc["soil_moisture_pct"],
            "inclinometer_tilt_rate_mm_day": loc["inclinometer_tilt_rate_mm_day"],
            "lithology_type": loc["lithology_type"],
            # Model-produced outputs
            **prediction,
            # Transparency disclaimer
            "data_source": "SIMULATED_DEMO",
        }

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [loc["lng"], loc["lat"]],
            },
            "properties": properties,
        })

    logger.info(
        "Generated predicted risk for %d / %d demo locations.",
        len(features),
        len(DEMO_RISK_LOCATIONS),
    )

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "total": len(features),
            "disclaimer": (
                "Environmental and sensor values are SIMULATED for prototype "
                "demonstration. They do not represent live sensor measurements. "
                "In production, replace with real IoT / weather API data."
            ),
        },
    }


@router.get("/predicted-risk-locations")
def get_predicted_risk_locations() -> Dict[str, Any]:
    """
    Returns a GeoJSON FeatureCollection of demo locations across all 8 NER
    states, each with a landslide-risk prediction computed by
    LandslidePredictiveEngine.predict_risk().

    Results are cached in-memory after the first call (invalidated on restart).
    """
    global _predicted_risk_cache
    if _predicted_risk_cache is None:
        _predicted_risk_cache = _build_predicted_risk_geojson()
    return _predicted_risk_cache


@router.get("/states")
def get_ner_states() -> List[Dict[str, Any]]:
    return NER_STATES_DATA


@router.get("/highways")
def get_highways() -> List[Dict[str, Any]]:
    return HIGHWAY_CORRIDORS


@router.get("/sensors")
def get_sensors() -> List[Dict[str, Any]]:
    return sensors_service.get_all_sensors()


@router.get("/historical")
def get_historical_landslides() -> List[Dict[str, Any]]:
    return HISTORICAL_LANDSLIDES


@router.get("/resources")
def get_emergency_resources() -> List[Dict[str, Any]]:
    return EMERGENCY_RESOURCES


@router.get("/risk-heatmap")
def get_risk_heatmap_points() -> List[Dict[str, Any]]:
    """
    Returns spatial points with risk intensities across NER for heatmapping.
    """
    points = []
    
    # 1. Add highway points
    for hw in HIGHWAY_CORRIDORS:
        multiplier = 0.95 if hw["risk_level"] == "RED" else (0.75 if hw["risk_level"] == "ORANGE" else 0.45)
        for coord in hw["coordinates"]:
            points.append({
                "lat": coord[0],
                "lng": coord[1],
                "intensity": multiplier,
                "label": f"{hw['highway_name']} - {hw['stretch_name']}",
                "risk_level": hw["risk_level"]
            })
        multiplier = 0.95 if hw.get("risk_level") == "RED" else (0.75 if hw.get("risk_level") == "ORANGE" else 0.45)
        coords = hw.get("coordinates", [])
        if isinstance(coords, list):
            for coord in coords:
                points.append({
                    "lat": coord[0],
                    "lng": coord[1],
                    "intensity": multiplier,
                    "label": f"{hw.get('highway_name')} - {hw.get('stretch_name')}",
                    "risk_level": hw.get("risk_level")
                })
            
    # 2. Add sensor stations
    for s in sensors_service.get_all_sensors():
        s_mult = 1.0 if s["status"] == "CRITICAL" else (0.8 if s["status"] == "WARNING" else (0.5 if s["status"] == "WATCH" else 0.2))
        points.append({
            "lat": s["lat"],
            "lng": s["lng"],
            "intensity": s_mult,
            "label": f"IoT Station: {s['name']}",
            "risk_level": s["status"]
        })
        
    # 3. Add historical hot spots
    for h in HISTORICAL_LANDSLIDES:
        points.append({
            "lat": h["lat"],
            "lng": h["lng"],
            "intensity": 0.85,
            "label": f"Historical Zone: {h['location']}",
            "risk_level": "ORANGE"
        })
        
    return points

