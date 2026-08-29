"""Live meteorological data provider for TerraintTrace."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple

import httpx


class LiveWeatherUnavailable(RuntimeError):
    """Raised when the live weather provider cannot be reached."""


class WeatherService:
    """Fetches and briefly caches live weather data from Open-Meteo."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    CACHE_TTL = timedelta(minutes=5)

    def __init__(self):
        self._cache: Dict[Tuple[float, float], Tuple[datetime, Dict[str, Any]]] = {}

    def _fetch(self, lat: float, lng: float) -> Dict[str, Any]:
        key = (round(lat, 4), round(lng, 4))
        now = datetime.now(timezone.utc)
        cached = self._cache.get(key)
        if cached and now - cached[0] < self.CACHE_TTL:
            return cached[1]

        params = {
            "latitude": lat,
            "longitude": lng,
            "current": "temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,cloud_cover,wind_speed_10m",
            "hourly": "precipitation,rain,soil_moisture_0_to_1cm,soil_moisture_9_to_27cm,wind_speed_10m",
            "past_days": 3,
            "forecast_days": 3,
            "timezone": "auto",
        }
        try:
            response = httpx.get(self.BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise LiveWeatherUnavailable("Open-Meteo live weather data is temporarily unavailable") from exc

        if not data.get("current") or not data.get("hourly"):
            raise LiveWeatherUnavailable("Open-Meteo returned an incomplete weather response")

        self._cache[key] = (now, data)
        return data

    @staticmethod
    def _weather_condition(code: int) -> str:
        conditions = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
            55: "Dense drizzle", 61: "Slight rain", 63: "Rain", 65: "Heavy rain",
            80: "Rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Severe thunderstorm with hail",
        }
        return conditions.get(code, "Unknown")

    @staticmethod
    def _risk_level(rainfall_mm: float, soil_moisture: float) -> str:
        if rainfall_mm >= 30 or soil_moisture >= 0.80:
            return "RED"
        if rainfall_mm >= 15 or soil_moisture >= 0.65:
            return "ORANGE"
        if rainfall_mm >= 5 or soil_moisture >= 0.45:
            return "YELLOW"
        return "GREEN"

    @staticmethod
    def _hourly_index(data: Dict[str, Any]) -> int:
        times = data["hourly"]["time"]
        current_time = data["current"]["time"]
        return max((i for i, value in enumerate(times) if value <= current_time), default=0)

    def get_current_weather(self, lat: float, lng: float, location_name: str = "NER Station") -> Dict[str, Any]:
        data = self._fetch(lat, lng)
        current = data["current"]
        hourly = data["hourly"]
        index = self._hourly_index(data)
        recent_24h = slice(max(0, index - 23), index + 1)
        recent_72h = slice(max(0, index - 71), index + 1)

        rain_24h = round(sum(hourly["rain"][recent_24h]), 1)
        rain_3d = round(sum(hourly["rain"][recent_72h]), 1)
        soil_moisture = hourly["soil_moisture_0_to_1cm"][index] or 0.0
        api_30 = round(rain_24h + (0.88 * max(0, rain_3d - rain_24h)), 1)
        warning = self._risk_level(rain_24h, soil_moisture)

        return {
            "location_name": location_name,
            "lat": lat,
            "lng": lng,
            "current_rainfall_rate_mm_h": current["rain"] or current["precipitation"] or 0.0,
            "rainfall_24h_mm": rain_24h,
            "rainfall_3d_mm": rain_3d,
            "rainfall_7d_mm": rain_3d,
            "api_30_mm": api_30,
            "relative_humidity_pct": current["relative_humidity_2m"],
            "soil_moisture_pct": round(soil_moisture * 100, 1),
            "temperature_c": current["temperature_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "cloud_cover_pct": current["cloud_cover"],
            "weather_condition": self._weather_condition(current["weather_code"]),
            "imd_warning_level": warning,
            "timestamp": current["time"],
            "source": "Open-Meteo live weather forecast API",
        }

    def get_72h_forecast(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        data = self._fetch(lat, lng)
        hourly = data["hourly"]
        start = self._hourly_index(data) + 1
        forecast: List[Dict[str, Any]] = []

        for index in range(start, min(start + 72, len(hourly["time"])), 3):
            end = min(index + 3, len(hourly["time"]))
            rainfall = round(sum(hourly["rain"][index:end]), 1)
            soil_moisture = hourly["soil_moisture_0_to_1cm"][index] or 0.0
            forecast.append({
                "time": hourly["time"][index],
                "hours_ahead": index - start + 1,
                "rainfall_3h_mm": rainfall,
                "rainfall_intensity_mm_h": round(rainfall / max(1, end - index), 1),
                "soil_saturation_forecast_pct": round(soil_moisture * 100, 1),
                "predicted_risk_level": self._risk_level(rainfall, soil_moisture),
                "wind_speed_kmh": hourly["wind_speed_10m"][index],
                "source": "Open-Meteo forecast API",
            })
        return forecast


weather_service = WeatherService()
