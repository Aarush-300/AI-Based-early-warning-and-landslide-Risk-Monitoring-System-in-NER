# TerraintTrace

TerraintTrace is an AI-assisted geospatial decision-support platform for landslide-risk monitoring, live weather intelligence, GIS visualization, and field reporting across India's North Eastern Region.

## Data sources and current data mode

TerraintTrace explicitly separates live sources from demonstration layers.

| Layer | Source | Status |
| --- | --- | --- |
| Current weather, rainfall, wind, cloud cover, and soil moisture | [Open-Meteo Weather API](https://open-meteo.com/en/docs) | Live; requested by coordinate and cached for 5 minutes |
| Basemap | [OpenStreetMap](https://www.openstreetmap.org/copyright) | Live map tiles; no API key required |
| Sensor telemetry | Local demo sensor stations and simulation | Not live; connect `SENSOR_GATEWAY_URL` to use deployed hardware |
| Roads, shelters, alerts, risk zones, and historical landslides | Seeded local SQLite data and curated demo GIS records | Not a live official feed |
| Field reports | Application users | Live after submission, stored in the application database |

Live-weather endpoints:

- `GET /api/v1/predict/weather-forecast?lat=<latitude>&lng=<longitude>`
- `POST /api/v1/predict/` without rainfall fields; the service enriches the prediction with live weather data.

If the live provider is unavailable, these endpoints return HTTP `503` instead of fabricating weather values.

## Capabilities

- Live coordinate-based weather and 72-hour forecast data.
- Leaflet GIS map with highway, report, resource, sensor, and historical-landslide layers.
- AI landslide-risk prediction using rainfall, soil moisture, slope, elevation, and geotechnical assumptions.
- Field reporting with offline queueing and later synchronization.
- Multilingual emergency alerts and CAP XML feed.

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
```

### 2. Launch the platform

```bash
python start_platform.py
```

Open the dashboard at `http://127.0.0.1:8000`.

### 3. API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- CAP feed: `http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml`

### 4. Run tests

```bash
python -m pytest backend/tests/test_backend.py -v
```

## Configuration

Copy `.env.example` to `.env` and set production values for the database and `SECRET_KEY`.

Open-Meteo does not require an API key for this integration. To replace the simulated sensor data with a real deployment, configure a compatible sensor gateway through `SENSOR_GATEWAY_URL` and map its readings to the telemetry schema.

## Important operational note

TerraintTrace is a decision-support application. Its current live input is meteorological data; the local sensor telemetry and operational GIS layers are demonstration data unless an approved upstream feed is connected. Do not use the demo layers as the sole basis for emergency or safety-critical decisions.
