import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class WeatherService:
    def __init__(self):
        # Base decay factor for Antecedent Precipitation Index in Himalayan/NER terrain
        self.k_factor = 0.88

    def get_current_weather(self, lat: float, lng: float, location_name: str = "NER Station") -> Dict[str, Any]:
        """
        Synthesizes real-time meteorological parameters calibrated to latitude/longitude
        and micro-climate zones in the North Eastern Region.
        """
        # Meghalaya / South Sikkim / Dima Hasao have higher rainfall coefficients
        is_high_rain_belt = (24.8 <= lat <= 26.0 and 91.0 <= lng <= 93.5) or (27.0 <= lat <= 27.8 and 88.0 <= lng <= 89.0)
        
        base_intensity = 18.5 if is_high_rain_belt else 6.5
        # Add realistic variability
        jitter = random.uniform(0.7, 1.4)
        current_intensity = round(base_intensity * jitter, 1)
        
        rain_24h = round(current_intensity * random.uniform(5.5, 9.0), 1)
        rain_3d = round(rain_24h * random.uniform(1.8, 2.6), 1)
        rain_7d = round(rain_3d * random.uniform(1.4, 2.2), 1)
        
        # Calculate API (Antecedent Precipitation Index)
        api_30 = round(rain_24h + (self.k_factor * (rain_3d - rain_24h)) + ((self.k_factor ** 2) * (rain_7d - rain_3d)), 1)
        
        humidity = min(100, int(75 + (current_intensity * 0.9) + random.randint(0, 8)))
        temp_c = round(24.5 - (lat - 24.0) * 1.8 + random.uniform(-1.5, 1.5), 1)
        wind_speed_kmh = round(12.0 + random.uniform(0, 18.0), 1)
        
        return {
            "location_name": location_name,
            "lat": lat,
            "lng": lng,
            "current_rainfall_rate_mm_h": current_intensity,
            "rainfall_24h_mm": rain_24h,
            "rainfall_3d_mm": rain_3d,
            "rainfall_7d_mm": rain_7d,
            "api_30_mm": api_30,
            "relative_humidity_pct": humidity,
            "temperature_c": temp_c,
            "wind_speed_kmh": wind_speed_kmh,
            "cloud_cover_pct": min(100, int(humidity * 1.05)),
            "weather_condition": "Heavy Monsoonal Downpour" if current_intensity > 15 else ("Moderate Rain" if current_intensity > 5 else "Light Drizzle"),
            "imd_warning_level": "RED" if current_intensity > 20 or rain_24h > 120 else ("ORANGE" if current_intensity > 10 or rain_24h > 70 else ("YELLOW" if current_intensity > 3 else "GREEN")),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def get_72h_forecast(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Generates 72-hour hourly / 3-hour interval predictive rainfall and saturation forecast.
        """
        now = datetime.utcnow()
        forecast = []
        
        # Determine wave pattern for monsoon front
        peak_offset_hours = random.randint(8, 24)
        
        for i in range(0, 72, 3):
            step_time = now + timedelta(hours=i)
            # Simulated storm pulse curve
            time_factor = math.exp(-((i - peak_offset_hours) ** 2) / (2 * (10 ** 2)))
            step_intensity = round(random.uniform(2.0, 6.0) + (24.0 * time_factor), 1)
            step_rainfall = round(step_intensity * 3.0, 1)
            
            saturation = min(98.0, round(50.0 + (step_intensity * 1.8) + (i * 0.3), 1))
            
            if step_intensity > 18 or saturation > 85:
                risk_lvl = "RED"
            elif step_intensity > 10 or saturation > 75:
                risk_lvl = "ORANGE"
            elif step_intensity > 4 or saturation > 65:
                risk_lvl = "YELLOW"
            else:
                risk_lvl = "GREEN"
                
            forecast.append({
                "time": step_time.strftime("%Y-%m-%d %H:%M"),
                "hours_ahead": i,
                "rainfall_3h_mm": step_rainfall,
                "rainfall_intensity_mm_h": step_intensity,
                "soil_saturation_forecast_pct": saturation,
                "predicted_risk_level": risk_lvl,
                "wind_speed_kmh": round(10 + step_intensity * 0.8, 1)
            })
            
        return forecast

weather_service = WeatherService()

