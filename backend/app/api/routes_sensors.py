"""
TerrainTrace-NER In-Situ IoT Hardware Telemetry & Sensor Ingestion Router
Provides endpoints for physical dataloggers (Campbell Scientific, Encardio-Rite, LoRaWAN)
to stream real-time geotechnical slope sensor readings directly into the platform.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import datetime

from backend.app.database import get_db
from backend.app.models.db_models import Sensor, SensorReading
from backend.app.models.schemas import HardwareSensorIngestPayload, HardwareSensorRegisterPayload
from backend.app.data.sensors_service import sensors_service

router = APIRouter(prefix="/sensors", tags=["In-Situ IoT Ground Sensors"])


@router.get("/")
def get_all_sensors_telemetry() -> List[Dict[str, Any]]:
    """Returns real-time telemetry from all registered physical and calibrated ground stations."""
    return sensors_service.get_all_sensors()


@router.get("/{sensor_id}")
def get_single_sensor_telemetry(sensor_id: str) -> Dict[str, Any]:
    """Returns detailed real-time telemetry and historical buffer for a specific sensor node."""
    sensor = sensors_service.get_sensor(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor station not found")
    return sensor


@router.post("/ingest")
def ingest_physical_sensor_telemetry(
    payload: HardwareSensorIngestPayload,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Direct Hardware Ingestion Endpoint for deployed field dataloggers (4G / NB-IoT / Ethernet).
    Accepts pore pressure (kPa), biaxial tilt (°), displacement rate, soil moisture, and rainfall.
    """
    result = sensors_service.ingest_hardware_reading(payload.model_dump())
    
    # Also persist reading into SQL database for audit logs
    try:
        # Find or create DB sensor record
        db_sensor = db.query(Sensor).filter(Sensor.sensor_id == payload.sensor_id).first()
        if not db_sensor:
            sensor_obj = sensors_service.get_sensor(payload.sensor_id)
            db_sensor = Sensor(
                sensor_id=payload.sensor_id,
                name=sensor_obj.get("name", payload.sensor_id) if sensor_obj else payload.sensor_id,
                sensor_type="Piezometer + Inclinometer",
                location_name=sensor_obj.get("location_name", "Field Station") if sensor_obj else "Field Station",
                state=sensor_obj.get("state", "NER") if sensor_obj else "NER",
                district=sensor_obj.get("district", "") if sensor_obj else "",
                lat=sensor_obj.get("lat", 25.1324) if sensor_obj else 25.1324,
                lng=sensor_obj.get("lng", 92.3682) if sensor_obj else 92.3682,
                status=result["evaluated_status"],
                battery_pct=payload.battery_pct or 100,
                last_reading_at=datetime.datetime.now(datetime.timezone.utc)
            )
            db.add(db_sensor)
            db.commit()
            db.refresh(db_sensor)
        else:
            db_sensor.status = result["evaluated_status"]
            db_sensor.battery_pct = payload.battery_pct or db_sensor.battery_pct
            db_sensor.last_reading_at = datetime.datetime.now(datetime.timezone.utc)
            
        reading = SensorReading(
            sensor_db_id=db_sensor.id,
            pore_water_pressure_kpa=payload.pore_water_pressure_kpa,
            soil_moisture_pct=payload.soil_moisture_pct,
            inclinometer_tilt_deg=payload.inclinometer_tilt_deg,
            displacement_rate_mm_day=payload.displacement_rate_mm_day or (payload.inclinometer_tilt_deg * 2.8),
            rainfall_mm_h=payload.current_rainfall_mm_h or 0.0,
            acoustic_emission_db=payload.acoustic_emission_db or 20.0,
            temperature_c=payload.temperature_c or 22.0
        )
        db.add(reading)
        db.commit()
    except Exception as exc:
        db.rollback()
        # Non-blocking for real-time telemetry loop
        print(f"DB sensor persistence warning: {exc}")
        
    return result


@router.post("/register")
def register_new_physical_sensor(
    payload: HardwareSensorRegisterPayload,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Registers a new physical IoT ground sensor station into the active monitoring network."""
    station = sensors_service.register_sensor_station(payload.model_dump())
    
    # Save to database
    try:
        existing = db.query(Sensor).filter(Sensor.sensor_id == payload.sensor_id).first()
        if not existing:
            new_s = Sensor(
                sensor_id=payload.sensor_id,
                name=payload.name,
                sensor_type=payload.sensor_type,
                location_name=payload.location_name,
                state=payload.state,
                district=payload.district,
                lat=payload.lat,
                lng=payload.lng,
                elevation_m=payload.elevation_m,
                status="NORMAL",
                battery_pct=100
            )
            db.add(new_s)
            db.commit()
    except Exception as exc:
        db.rollback()
        print(f"DB sensor register warning: {exc}")
        
    return {
        "status": "REGISTERED_SUCCESS",
        "station": station
    }

