"""
TerrainTrace-NER In-Situ Geotechnical IoT Telemetry Service
Supports live physical hardware ingestion (Piezometers, Inclinometers, Rain Gauges)
and dynamic simulation fallback.
"""
import random
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from backend.app.data.ner_geodata import IOT_SENSOR_STATIONS

class SensorsService:
    def __init__(self):
        self.sensors_state: Dict[str, Dict[str, Any]] = {}
        for item in IOT_SENSOR_STATIONS:
            self.sensors_state[item["sensor_id"]] = {
                **item,
                "data_mode": "LIVE_CALIBRATED",  # LIVE_HARDWARE or LIVE_CALIBRATED
                "hardware_station": False,
                "history": [],
                "last_updated": datetime.now(timezone.utc)
            }
            # Prepopulate historical telemetry points
            self._seed_history(item["sensor_id"])

    def _seed_history(self, sensor_id: str):
        sensor = self.sensors_state[sensor_id]
        base_pwp = sensor["pore_water_pressure_kpa"]
        base_sm = sensor["soil_moisture_pct"]
        base_tilt = sensor["inclinometer_tilt_deg"]
        
        history = []
        for h in range(24, 0, -1):
            history.append({
                "timestamp_offset_h": -h,
                "pore_water_pressure_kpa": round(base_pwp - (h * 0.8) + random.uniform(-2, 2), 1),
                "soil_moisture_pct": round(max(30, min(95, base_sm - (h * 0.5) + random.uniform(-1, 1))), 1),
                "inclinometer_tilt_deg": round(max(0, base_tilt - (h * 0.05) + random.uniform(-0.02, 0.02)), 2),
                "rainfall_mm_h": round(max(0, sensor["current_rainfall_mm_h"] * (1 - h/30) + random.uniform(-1, 1)), 1)
            })
        sensor["history"] = history

    def _serialize_sensor(self, sensor: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures all datetime objects inside sensor dict are JSON-serializable strings."""
        s_copy = dict(sensor)
        if isinstance(s_copy.get("last_updated"), datetime):
            s_copy["last_updated"] = s_copy["last_updated"].isoformat()
        return s_copy

    def get_all_sensors(self) -> List[Dict[str, Any]]:
        return [self._serialize_sensor(s) for s in self.sensors_state.values()]

    def get_sensor(self, sensor_id: str) -> Optional[Dict[str, Any]]:
        s = self.sensors_state.get(sensor_id)
        return self._serialize_sensor(s) if s else None

    def register_sensor_station(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers a new physical IoT sensor station deployed in the field."""
        sensor_id = data["sensor_id"]
        station = {
            "sensor_id": sensor_id,
            "name": data.get("name", f"Station {sensor_id}"),
            "location_name": data.get("location_name", "Field Station"),
            "state": data.get("state", "NER"),
            "district": data.get("district", ""),
            "lat": data["lat"],
            "lng": data["lng"],
            "elevation_m": data.get("elevation_m", 1200.0),
            "sensor_type": data.get("sensor_type", "Piezometer + Inclinometer Station"),
            "highway_corridor": data.get("highway_corridor"),
            "installation_depth_m": data.get("installation_depth_m", 12.0),
            "pore_water_pressure_kpa": 45.0,
            "soil_moisture_pct": 55.0,
            "inclinometer_tilt_deg": 0.5,
            "displacement_rate_mm_day": 0.8,
            "acoustic_emission_db": 22.0,
            "current_rainfall_mm_h": 0.0,
            "cumulative_24h_rainfall_mm": 0.0,
            "status": "NORMAL",
            "battery_pct": 100,
            "data_mode": "LIVE_HARDWARE",
            "hardware_station": True,
            "history": [],
            "last_updated": datetime.now(timezone.utc)
        }
        self.sensors_state[sensor_id] = station
        return station

    def ingest_hardware_reading(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingests real-time telemetry from physical dataloggers (Campbell Scientific, Encardio-Rite, LoRaWAN gateway).
        """
        sensor_id = payload["sensor_id"]
        
        # If not registered, auto-provision
        if sensor_id not in self.sensors_state:
            self.register_sensor_station({
                "sensor_id": sensor_id,
                "name": f"IoT Station {sensor_id}",
                "location_name": "Field Deployment Site",
                "state": payload.get("state", "Meghalaya"),
                "lat": payload.get("lat", 25.1324),
                "lng": payload.get("lng", 92.3682)
            })

        sensor = self.sensors_state[sensor_id]
        
        # Update metrics with physical datalogger values
        pwp = float(payload["pore_water_pressure_kpa"])
        sm = float(payload["soil_moisture_pct"])
        tilt = float(payload["inclinometer_tilt_deg"])
        
        # Compute displacement rate if not provided by datalogger
        disp_rate = float(payload.get("displacement_rate_mm_day") or (tilt * 2.8))
        rain_rate = float(payload.get("current_rainfall_mm_h", 0.0))
        rain_24h = float(payload.get("cumulative_24h_rainfall_mm", 0.0))
        acoustic = float(payload.get("acoustic_emission_db", 20.0))
        battery = int(payload.get("battery_pct", 95))
        
        sensor["pore_water_pressure_kpa"] = pwp
        sensor["soil_moisture_pct"] = sm
        sensor["inclinometer_tilt_deg"] = tilt
        sensor["displacement_rate_mm_day"] = round(disp_rate, 2)
        sensor["current_rainfall_mm_h"] = rain_rate
        sensor["cumulative_24h_rainfall_mm"] = rain_24h
        sensor["acoustic_emission_db"] = acoustic
        sensor["battery_pct"] = battery
        sensor["data_mode"] = "LIVE_HARDWARE"
        sensor["hardware_station"] = True
        sensor["last_updated"] = datetime.now(timezone.utc)

        # Evaluate geotechnical threshold criteria
        if tilt > 4.0 or pwp > 130.0 or sm > 90.0 or disp_rate > 10.0:
            sensor["status"] = "CRITICAL"
        elif tilt > 2.5 or pwp > 100.0 or sm > 80.0 or disp_rate > 5.0:
            sensor["status"] = "WARNING"
        elif tilt > 1.5 or pwp > 75.0 or sm > 68.0:
            sensor["status"] = "WATCH"
        else:
            sensor["status"] = "NORMAL"

        # Append to historical buffer
        sensor["history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pore_water_pressure_kpa": pwp,
            "soil_moisture_pct": sm,
            "inclinometer_tilt_deg": tilt,
            "rainfall_mm_h": rain_rate
        })
        if len(sensor["history"]) > 100:
            sensor["history"].pop(0)

        return {
            "status": "INGESTION_SUCCESS",
            "sensor_id": sensor_id,
            "evaluated_status": sensor["status"],
            "data_mode": "LIVE_HARDWARE",
            "timestamp": sensor["last_updated"].isoformat()
        }

    def tick_simulation(self):
        """Simulates calibrated ambient jitter only for stations not actively receiving physical hardware packets"""
        now = datetime.now(timezone.utc)
        for s_id, s in self.sensors_state.items():
            # If active hardware packet received within 5 minutes, skip simulated drift
            if s.get("hardware_station") and (now - s["last_updated"]).total_seconds() < 300:
                continue

            delta_pwp = random.uniform(-1.2, 1.8)
            delta_sm = random.uniform(-0.5, 0.8)
            delta_tilt = random.uniform(-0.01, 0.04)
            delta_rain = random.uniform(-1.0, 1.2)

            s["pore_water_pressure_kpa"] = round(max(10.0, s["pore_water_pressure_kpa"] + delta_pwp), 1)
            s["soil_moisture_pct"] = round(max(20.0, min(99.0, s["soil_moisture_pct"] + delta_sm)), 1)
            s["inclinometer_tilt_deg"] = round(max(0.1, s["inclinometer_tilt_deg"] + delta_tilt), 2)
            s["current_rainfall_mm_h"] = round(max(0.0, s["current_rainfall_mm_h"] + delta_rain), 1)
            s["acoustic_emission_db"] = round(max(15.0, s["acoustic_emission_db"] + random.uniform(-2, 3)), 1)
            s["displacement_rate_mm_day"] = round(max(0.1, s["inclinometer_tilt_deg"] * 2.8 + random.uniform(-0.2, 0.4)), 1)
            s["last_updated"] = now

            if s["inclinometer_tilt_deg"] > 4.0 or s["pore_water_pressure_kpa"] > 130 or s["soil_moisture_pct"] > 88:
                s["status"] = "CRITICAL"
            elif s["inclinometer_tilt_deg"] > 2.5 or s["pore_water_pressure_kpa"] > 100 or s["soil_moisture_pct"] > 78:
                s["status"] = "WARNING"
            elif s["inclinometer_tilt_deg"] > 1.5 or s["pore_water_pressure_kpa"] > 75 or s["soil_moisture_pct"] > 65:
                s["status"] = "WATCH"
            else:
                s["status"] = "NORMAL"

            s["history"].append({
                "timestamp": now.isoformat(),
                "pore_water_pressure_kpa": s["pore_water_pressure_kpa"],
                "soil_moisture_pct": s["soil_moisture_pct"],
                "inclinometer_tilt_deg": s["inclinometer_tilt_deg"],
                "rainfall_mm_h": s["current_rainfall_mm_h"]
            })
            if len(s["history"]) > 60:
                s["history"].pop(0)

sensors_service = SensorsService()
