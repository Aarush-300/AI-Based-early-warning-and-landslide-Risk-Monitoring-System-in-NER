# BhooDrishti-NER (भू-दृष्टि)
### AI-Powered Real-Time Landslide Early Warning, GIS Monitoring & Crowdsourced Reporting Platform for India's North Eastern Region

---

## 🏔️ Background & Problem Statement
The **North Eastern Region (NER)** of India—spanning **Sikkim, Assam, Meghalaya, Arunachal Pradesh, Nagaland, Manipur, Mizoram, and Tripura**—is one of the most landslide-prone zones in the world due to extreme monsoon rainfall, young folded Himalayan & Indo-Burman geology, fragile Disang/Daling schists, and unplanned hill cutting. 

**BhooDrishti-NER** bridges this gap with an AI-driven, real-time early warning and geospatial decision-support platform designed for State Disaster Management Authorities (SDMAs), Border Roads Organisation (BRO), National Highways Authority of India (NHAI), district administrations, and local hill communities.

---

## ⚡ Key Capabilities & Architecture

```
+-----------------------------------------------------------------------------------------------+
|                                      DATA INGESTION LAYER                                     |
|  - IMD Weather Radar & Forecast Feeds (Dynamic Intensity & Antecedent Precipitation API-30)   |
|  - In-Situ Geotechnical IoT Telemetry (Pore Pressure, Soil Saturation, Inclinometer Tilt)     |
|  - NASA/ISRO Satellite DEM Slope Gradients & Geological Thrust Line Buffers                   |
|  - GSI Historical Landslide Inventory Catalogs                                                |
+-----------------------------------------------+-----------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
|                                     AI / ML ANALYTICS CORE                                    |
|  1. Hydro-Meteorological Failure Model: Calibrated Caine I-D Thresholds (Eastern Himalayas)   |
|  2. Geotechnical Risk ML: Random Forest & Gradient Boosting Classifier with Factor of Safety  |
|  3. Edge Computer Vision Engine: Tension Crack & Debris Volume Classification from Photos     |
|  4. Emergency Priority Engine: Vulnerability Index ($V_i$) & Detour Optimization             |
+-----------------------------------------------+-----------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
|                                      APPLICATION SERVICES                                     |
|  - FastAPI Backend (REST & WebSocket /ws/live for dynamic 4s sensor telemetry streaming)      |
|  - Multilingual Alert Engine (English, Assamese, Bengali, Hindi, Khasi, Mizo, Manipuri, etc.)  |
|  - OASIS Common Alerting Protocol (CAP v1.2) XML compliant broadcasting                       |
|  - Offline-First PWA Vault (IndexedDB local queue for remote mountain area blackout sync)     |
+-----------------------------------------------+-----------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
|                                  INTERACTIVE GIS COMMAND CENTER                               |
|  - Leaflet Dynamic 2D GIS Map (Susceptibility Heatmap, Corridors, Sensors, Shelters, Reports) |
|  - Click-anywhere AI Slope Risk Probe: Instant geotechnical evaluation at any coordinate       |
|  - 72-Hour Predictive Hydro-Meteorological Forecast Graph & What-If Parameter Simulator        |
|  - Strategic Highway Matrix (NH-10, NH-29, NH-06, NH-102, NH-13, NH-54, NH-27) & Detour Plan  |
|  - Web Speech API Native Audio Alert Announcer in local languages                             |
+-----------------------------------------------------------------------------------------------+
```

---

## 🚀 Quick Start Guide

### 1. Launch Platform
```bash
python start_platform.py
```
This starts the backend and automatically opens the interactive GIS dashboard at:
👉 **`http://127.0.0.1:8000`**

### 2. API Documentation & CAP Feeds
- **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`
- **OASIS CAP 1.2 XML Feed**: `http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml`

### 3. Run Automated Tests
```bash
python -m pytest backend/tests/test_backend.py -v
```

---

## 🧪 AI & Geotechnical Models Implemented

### 1. Hydro-Meteorological Rainfall Threshold ($I-D$ Curve)
Uses empirical Caine equations calibrated for North East India:
$$I = \alpha \cdot D^{-\beta}$$
- **Eastern Himalayas (Sikkim / Arunachal / North Assam)**: $\alpha = 14.82, \beta = 0.42$
- **Indo-Burman Range (Nagaland / Manipur / Mizoram / Meghalaya)**: $\alpha = 18.50, \beta = 0.48$

### 2. Infinite Slope Factor of Safety ($F_s$)
Computes limit equilibrium slope stability:
$$F_s = \frac{c' + (\gamma_{sat} \cdot z - \gamma_w \cdot h_w) \cos^2 \alpha \tan \phi'}{\gamma_{sat} \cdot z \cdot \sin \alpha \cos \alpha}$$
Where:
- $\alpha$: Slope angle ($10^\circ - 65^\circ$)
- $c'$: Effective soil cohesion ($18.0 \text{ kPa}$)
- $\phi'$: Internal friction angle ($28.0^\circ$)
- $h_w / z$: Normalized saturation depth based on in-situ moisture sensors.

### 3. Computer Vision Field Inspection
Analyzes user-uploaded photos for:
- Tension crack aperture width estimation ($\text{mm}$)
- Surface edge gradient density & scarp identification
- Colluvium/debris volume classification ($> 500\text{ m}^3$ vs $< 50\text{ m}^3$)
- Auto-generates prioritized mitigation actions.

### 4. Emergency Response Prioritization Index ($V_i$)
$$V_i = w_{sev} \cdot \text{Severity} + w_{traf} \cdot \text{StrandedTraffic} + w_{pop} \cdot \text{IsolatedSettlement} + w_{infra} \cdot \text{LifelineCutoff}$$
Calculates priority rankings ($0 - 100$) to dispatch heavy machinery (excavators, rock breakers, SDRF teams) to critical highway choke points.

---

## 🌐 Supported Multilingual Alert Languages
- **English** (`en`)
- **Assamese** (`as` - অসমীয়া)
- **Bengali** (`bn` - বাংলা)
- **Hindi** (`hi` - हिन्दी)
- **Khasi** (`kha` - Ka Ktien Khasi)
- **Mizo** (`lus` - Mizo ṭawng)
- **Manipuri** (`mni` - মৈতৈলোন্)
- **Nagamese** (`nag` - Nagamese)

---

## 📴 Offline Resilience (PWA Architecture)
In remote mountain valleys where 4G/cellular networks drop during monsoon landslides:
1. Field officers and citizens can still log photo reports with GPS coordinates.
2. Reports are saved in **IndexedDB** (`bhoodrishti_offline_vault`).
3. When connectivity is restored, the application automatically synchronizes all pending records to the central disaster response database.

