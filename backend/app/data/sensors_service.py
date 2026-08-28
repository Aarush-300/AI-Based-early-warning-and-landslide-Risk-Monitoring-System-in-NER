import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.app.data.ner_geodata import IOT_SENSOR_STATIONS

class SensorsService:
    def __init__(self):
        self.sensors_state: Dict[str, Dict[str, Any]] = {}
        for item in IOT_SENSOR_STATIONS:
            self.sensors_state[item["sensor_id"]] = {
                **item,
                "history": [],
                "last_updated": datetime.utcnow()
            }
            # Prepopulate 20 historical telemetry points
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

    def get_all_sensors(self) -> List[Dict[str, Any]]:
        return list(self.sensors_state.values())

    def get_sensor(self, sensor_id: str) -> Optional[Dict[str, Any]]:
        return self.sensors_state.get(sensor_id)

    def tick_simulation(self):
        """Simulates micro-movements and dynamic sensor updates for live stream"""
        for s_id, s in self.sensors_state.items():
            # Add dynamic jitter/drift
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
            s["last_updated"] = datetime.utcnow()

            # Dynamic status update
            if s["inclinometer_tilt_deg"] > 4.0 or s["pore_water_pressure_kpa"] > 130 or s["soil_moisture_pct"] > 88:
                s["status"] = "CRITICAL"
            elif s["inclinometer_tilt_deg"] > 2.5 or s["pore_water_pressure_kpa"] > 100 or s["soil_moisture_pct"] > 78:
                s["status"] = "WARNING"
            elif s["inclinometer_tilt_deg"] > 1.5 or s["pore_water_pressure_kpa"] > 75 or s["soil_moisture_pct"] > 65:
                s["status"] = "WATCH"
            else:
                s["status"] = "NORMAL"

            # Add to history
            s["history"].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "pore_water_pressure_kpa": s["pore_water_pressure_kpa"],
                "soil_moisture_pct": s["soil_moisture_pct"],
                "inclinometer_tilt_deg": s["inclinometer_tilt_deg"],
                "rainfall_mm_h": s["current_rainfall_mm_h"]
            })
            if len(s["history"]) > 60:
                s["history"].pop(0)

sensors_service = SensorsService()

