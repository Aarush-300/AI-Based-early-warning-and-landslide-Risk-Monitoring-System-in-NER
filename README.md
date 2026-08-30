# TerrainTrace-NER (भू-दृष्टि / TerrainTrace)

> **AI-Powered Real-Time Landslide Early Warning, Geotechnical Risk Modeling & GIS Disaster Management Platform for India's North Eastern Region (NER)**  
> *Smart India Hackathon (SIH 2026) Prototype*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Leaflet](https://img.shields.io/badge/Leaflet-GIS_Mapping-199900?logo=leaflet&logoColor=white)](https://leafletjs.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML_Engine-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0_ORM-D71F00?logo=sqlite&logoColor=white)](https://www.sqlalchemy.org)
[![CAP 1.2](https://img.shields.io/badge/OASIS_CAP-1.2_XML_Feed-orange)](https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2.html)
[![Accuracy](https://img.shields.io/badge/Model_Accuracy-94.44%25-brightgreen)](models/training_metrics.json)

---

## 1. Executive Summary & Regional Context

India's **North Eastern Region (NER)**—comprising *Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, and Tripura*—is characterized by young, tectonically active Himalayan and Indo-Burman fold belts, steep slopes, highly weathered splintery shales, and torrential monsoon downpours. These conditions frequently trigger catastrophic landslides that sever critical lifeline highways (**NH-10, NH-06, NH-29, NH-27, NH-13, NH-54**), isolate remote tribal villages for weeks, damage infrastructure, and cause severe loss of life.

**TerrainTrace-NER** is an end-to-end AI and GIS decision-support early warning platform designed to shift disaster management from reactive response to **real-time predictive mitigation**.

```
                           TERRAINTRACE SYSTEM ARCHITECTURE
                           
  +-----------------------------------------------------------------------------------+
  |                           1. DATA INGESTION & SENSING                             |
  |  +---------------------+  +---------------------+  +---------------------------+  |
  |  | GSI NLSM & Bhukosh  |  | ISRO-NRSC Atlas     |  | NASA Global Landslide Cat |  |
  |  +----------+----------+  +----------+----------+  +-------------+-------------+  |
  |             |                        |                           |                |
  |             +------------------------+---------------------------+                |
  |                                      |                                            |
  |      +-------------------------------+-------------------------------+            |
  |      |                                                               |            |
  |  +---v----------------------------+             +--------------------v---------+  |
  |  | Live Copernicus / Open-Meteo   |             | In-Situ IoT Ground Sensors   |  |
  |  | Autonomous Weather Grids (AWS) |             | Piezometer, Tilt, Moisture   |  |
  |  +---------------+----------------+             +--------------------+---------+  |
  +------------------|---------------------------------------------------|------------+
                     |                                                   |
  +------------------v---------------------------------------------------v------------+
  |                        2. HYBRID PREDICTIVE RISK ENGINE                           |
  |  +--------------------------------+  +-----------------------------------------+  |
  |  | 1. Empirical Hydrological      |  | 2. Geotechnical Limit Equilibrium       |  |
  |  |    Caine I-D Threshold Curve   |  |    Infinite Slope Factor of Safety (Fs) |  |
  |  +--------------------------------+  +-----------------------------------------+  |
  |  +--------------------------------+  +-----------------------------------------+  |
  |  | 3. Ensemble ML Classifier      |  | 4. Explainable AI (XAI)                 |  |
  |  |    Random Forest (94.4% Acc)   |  |    Ranked Contributing Factors & Weights|  |
  |  +--------------------------------+  +-----------------------------------------+  |
  +--------------------------------------|--------------------------------------------+
                                         |
  +--------------------------------------v--------------------------------------------+
  |                        3. FASTAPI CORE APPLICATION BACKEND                        |
  |  - SQLAlchemy 2.0 ORM (SQLite / PostgreSQL)     - JWT Role-Based Access Control   |
  |  - WebSocket Telemetry Ticker (4s Sensor Stream) - Multi-Criteria Highway Priority |
  |  - OASIS CAP 1.2 XML Alert Feed                 - Field Report Upload & Validation|
  |  - IoT Datalogger Ingestion Gateway              - Autonomous Cloud Weather Sync  |
  +--------------------------------------|--------------------------------------------+
                                         |
  +--------------------------------------v--------------------------------------------+
  |                        4. INTERACTIVE FRONTEND GIS DASHBOARD                      |
  |  - Fullscreen Leaflet GIS Map with Layer Toggles- Real-Time Sensor Telemetry View |
  |  - 72h Weather Forecast & What-If Simulator     - Highway Connectivity Matrix     |
  |  - PWA Offline Vault (IndexedDB Auto-Sync)      - Multilingual CAP Alert Broadcast|
  +-----------------------------------------------------------------------------------+
```

---

## 2. Official Scientific Data & ML Engine Provenance

The predictive engine (`v2.0-official-ner`) is trained directly on curated historical landslide disaster records paired with real climate reanalysis data:

1. **Geological Survey of India (GSI) - NLSM & Bhukosh**: Verified historical disaster sites across all 8 NER states, fault proximity (*Dauki Fault, Main Boundary Thrust, Naga Thrust*), and lithological classification (*Disang Flysch, Tipam Sandstone, Daling Schists, Splintery Shales*).
2. **ISRO / NRSC Landslide Atlas of India (1998–2023)**: Vulnerability cluster density and regional district rankings.
3. **NASA Global Landslide Catalog (GLC) & COOLR**: Rainfall-triggered event classifications across the Eastern Himalayas.
4. **India Meteorological Department (IMD) / Copernicus ERA5 Climate Reanalysis**: Automated coordinate-based historical precipitation queries yielding exact 3-day cumulative rainfall ($R_{3d}$), 24-hour peak hourly intensity ($I_{24h}$), and soil saturation ($\theta_{soil}$) on the recorded disaster dates.

### Model Evaluation Performance (Stratified Out-of-Sample Test)

```
Overall Accuracy:   94.44%
Macro F1-Score:     0.9458
Macro ROC-AUC:      0.9957
5-Fold CV Mean F1:  0.9402 (+/- 0.0141)

Classification Breakdown:
┌──────────────┬───────────┬────────┬──────────┬─────────┐
│ Risk Tier    │ Precision │ Recall │ F1-Score │ Samples │
├──────────────┼───────────┼────────┼──────────┼─────────┤
│ GREEN (Safe) │   1.0000  │ 0.9560 │  0.9775  │    91   │
│ YELLOW (Adv) │   0.9495  │ 0.9216 │  0.9353  │   102   │
│ ORANGE (Wrn) │   0.8981  │ 0.9510 │  0.9238  │   102   │
│ RED (Danger) │   0.9394  │ 0.9538 │  0.9466  │    65   │
└──────────────┴───────────┴────────┴──────────┴─────────┘
```

#### Feature Importance Ranking:
1. **3-Day Cumulative Rainfall ($R_{3d}$)**: `19.14%`
2. **Slope Gradient Angle ($\alpha$)**: `16.82%`
3. **Distance to Tectonic Fault ($d_{\text{fault}}$)**: `11.96%`
4. **24h Peak Rainfall Intensity ($I_{24h}$)**: `11.25%`
5. **Inclinometer Displacement Rate**: `11.20%`
6. **Lithology Fragility Index**: `11.17%`
7. **Soil Moisture Saturation ($\theta_{\text{soil}}$)**: `9.90%`
8. **Elevation Above Sea Level ($z$)**: `8.56%`

---

## 3. Real-World Historical Benchmark Validations

The model has been validated against documented post-disaster field investigations:

| Incident & Location | Documented Real-World Outcome (GSI / NASA / SDMA) | TerrainTrace AI Prediction | Factor of Safety ($F_s$) & Risk Score | Concordance |
| :--- | :--- | :--- | :---: | :---: |
| **1. Sonapur Tunnel** *(NH-06, Meghalaya — June 16, 2023)* | **Catastrophic Debris Flow & Road Cut-Off**<br>342.3 mm 3-day rainfall, 100% soil saturation, completely blocked NH-06 for 4 days. | 🔴 **RED (Critical Alert)**<br>*Dominant Trigger: Antecedent Rain Saturation & Active Inclinometer Drift* | **$F_s = 0.82$**<br>Risk: `82.4%` | **100% Match** |
| **2. 29th Mile Teesta Valley** *(NH-10, Sikkim — Oct 4, 2023)* | **Major Roadway Washout & Shear Slip**<br>Teesta flash flood toe-erosion combined with 48° steep Daling phyllite slope failure. | 🔴 **RED (Critical Alert)**<br>*Dominant Trigger: Subsurface Shear & Over-steepened Slope* | **$F_s = 0.80$**<br>Risk: `64.6%` | **100% Match** |
| **3. Tupul Railway Yard** *(Noney, Manipur — June 30, 2022)* | **Catastrophic Debris Avalanche**<br>GSI scientific report recorded 46° steep cut-slope failure on Disang flysch damming the Ijei river. | 🔴 **RED (Critical Alert)**<br>*Dominant Trigger: Prolonged Rain Saturation & Steep Cut Geometry* | **$F_s = 0.80$**<br>Risk: `72.9%` | **100% Match** |
| **4. Hunthar Veng Slopes** *(Aizawl, Mizoram — Aug 2023)* | **Active Urban Creep & Sinking Zone**<br>Mizoram SDMA recorded structural road cracking and slow-moving translational creep. | 🟠 **ORANGE (High Warning)**<br>*Dominant Trigger: Subsurface Drift & Fragile Shale Lithology* | **$F_s = 1.07$**<br>Risk: `48.6%` | **100% Match** |
| **5. Guwahati Plains** *(Kamrup Metro, Assam — Dec 2023)* | **Completely Stable & Safe**<br>Flat alluvium plain, 8° slope, dry winter season (2 mm rain). | 🟢 **GREEN (Normal Safe)**<br>*Dominant Trigger: Baseline Hydrostatic Load (No Hazard)* | **$F_s = 3.50$**<br>Risk: `5.3%` | **100% Match** |

---

## 4. Mathematical Formulations

### 1. Empirical Regional Caine Intensity-Duration ($I-D$) Threshold
Evaluates whether rainfall intensity $I$ (mm/h) exceeds critical regional triggering limits over duration $D$ (hours):

$$I = \alpha \cdot D^{-\beta}$$

*   **Eastern Himalayan Regime** ($\text{Lat} \ge 26.8^\circ\text{N}$, Sikkim / Northern Assam / Arunachal): $\alpha = 14.82, \beta = 0.42$
*   **Indo-Burman Regime** ($\text{Lat} < 26.8^\circ\text{N}$, Meghalaya / Nagaland / Manipur / Mizoram / Tripura): $\alpha = 18.50, \beta = 0.48$

### 2. Infinite Slope Limit Equilibrium Factor of Safety ($F_s$)
Computes geotechnical slope stability incorporating pore-water pressure ($u$) and groundwater level:

$$F_s = \frac{c' + (\gamma_{\text{sat}} z - \gamma_w h_w) \cos^2\alpha \tan\phi'}{\gamma_{\text{sat}} z \sin\alpha \cos\alpha}$$

Where $c'$ is effective cohesion (kPa), $\phi'$ is friction angle ($^\circ$), $\gamma_{\text{sat}}$ is saturated unit weight ($19.5\text{ kN/m}^3$), $\gamma_w$ is water unit weight ($9.81\text{ kN/m}^3$), $z$ is regolith depth, and $\alpha$ is slope gradient.

### 3. Highway Clearance Prioritization Index ($V_i$)
Ranks blocked lifeline corridors for multi-agency emergency clearance:

$$V_i = w_1 \cdot \text{RiskLevel}_i + w_2 \cdot \text{TrafficVolume}_i + w_3 \cdot \text{DetourTimePenalty}_i + w_4 \cdot \text{StrategicLifelineWeight}_i$$

---

## 5. In-Situ IoT Ground Sensors & Autonomous Sensing

TerrainTrace operates with **zero physical setup required**, while also providing a plug-and-play gateway for physical field dataloggers:

1. **Autonomous Online Sensing (No Hardware Needed)**:
   - TerrainTrace continuously queries live satellite grids and atmospheric stations (Open-Meteo & Copernicus multi-depth soil moisture grids) for all mountain coordinates in North East India.
   - Automatically derives geotechnical pore-water pressure ($u = \gamma_w \cdot z_w$) and inclinometer drift without manual user configuration.
2. **Physical IoT Datalogger Ingestion Gateway**:
   - Field engineers deploying physical hardware (vibrating-wire piezometers, biaxial inclinometers, tipping-bucket rain gauges) can stream telemetry directly into:
     - `POST /api/v1/sensors/ingest`
     - `POST /api/v1/sensors/sync-online`
     - `POST /api/v1/sensors/register`
3. **Physical Datalogger Testing Client**:
   ```bash
   python scripts/send_physical_sensor_packet.py --station-id SONAPUR-HW-01 --pwp 145.0 --tilt 5.1 --soil 96.0 --rain 35.0
   ```

---

## 6. Key Platform Features

- **Interactive GIS Command Center**: Fullscreen Leaflet map displaying real-time risk heatmaps, monitored highway corridors (NH-10, NH-06, NH-29, NH-27, NH-13, NH-54), emergency shelters, SDRF/BRO staging bases, IoT sensors, and citizen field reports.
- **AI Terrain Probe**: Click any coordinate in North East India to immediately extract terrain features, calculate live $F_s$, check Caine $I-D$ curves, and view explainable contributing factors.
- **72-Hour Predictive Hydro-Meteorological Forecast**: Real-time hourly precipitation forecast and "What-If" geotechnical parameter simulator.
- **Crowdsourced Field Hazard Reporting (PWA Offline-First)**: IndexedDB offline vault allows field officials and citizens to capture geo-tagged hazard photos in zero-connectivity mountain zones and automatically synchronizes upon network recovery.
- **Multilingual Emergency Alerts & OASIS CAP 1.2 Feed**: Dynamic alerts rendered in 8 regional languages (*English, Assamese, Bengali, Hindi, Khasi, Mizo, Manipuri, Nagamese*) with automated OASIS Common Alerting Protocol 1.2 XML output.
- **Role-Based Access Control (RBAC)**: Secure JWT authentication with dedicated views for Platform Admins, Disaster Management Officers, Field Staff, and Citizens.

---

## 7. Quick Start & Installation

### Prerequisites
- Python 3.10+ (Anaconda or Standard Python)
- Node.js 18+ & npm

### Step 1: Clone and Install Backend Dependencies

```bash
# Clone the repository
git clone https://github.com/Aarush-300/AI-Based-early-warning-and-landslide-Risk-Monitoring-System-in-NER.git
cd AI-Based-early-warning-and-landslide-Risk-Monitoring-System-in-NER

# Install Python requirements
pip install -r requirements.txt
```

### Step 2: Build the Frontend Dashboard

```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 3: Launch TerrainTrace

```bash
python start_platform.py
```

*   **Interactive Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
*   **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **CAP 1.2 XML Feed**: [http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml](http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml)

---

## 8. Demo Credentials

| Role | Username | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Platform Administrator** | `admin` | `admin123` | Full access, system broadcast, model retraining |
| **Disaster Management Officer** | `officer` | `officer123` | SDMA / BRO corridor management, alert issuance |
| **Field Engineer / SDRF** | `field1` | `field123` | Ground report verification, clearance logging |
| **Citizen / Public** | `citizen` | `citizen123` | Hazard reporting, public alerts, detour routes |

---

## 9. Retraining the Model with Official Data

To re-harvest official disaster events, query live climate reanalysis data, and retrain the machine learning model:

```bash
# Run the official data harvester & training pipeline
python -m backend.app.ml.train_with_official_data

# Run benchmark verification against GSI/NASA cases
python -m backend.app.ml.benchmark_validation
```

---

## 10. Running Automated Tests

```bash
# Execute backend test suite (FastAPI TestClient + Pytest)
python -m pytest backend/tests/test_backend.py -v
```

---

## 11. API Reference Summary

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/auth/login` | `POST` | Authenticate and obtain JWT bearer token |
| `/api/v1/auth/register` | `POST` | Register a new citizen or field officer account |
| `/api/v1/predict/` | `POST` | Run AI slope failure risk prediction |
| `/api/v1/predict/weather-forecast` | `GET` | Get live 72-hour precipitation forecast |
| `/api/v1/predict/model-provenance` | `GET` | Retrieve official GSI/ISRO/NASA training metrics |
| `/api/v1/gis/states` | `GET` | GeoJSON state boundaries and capital centers |
| `/api/v1/gis/highways` | `GET` | Strategic lifeline highway corridor polylines |
| `/api/v1/gis/risk-heatmap` | `GET` | Dynamic regional landslide susceptibility points |
| `/api/v1/sensors/` | `GET` | Real-time in-situ telemetry from all mountain stations |
| `/api/v1/sensors/ingest` | `POST` | Ingest physical field datalogger telemetry packet |
| `/api/v1/sensors/sync-online` | `POST` | Trigger cloud synchronization with live satellite observations |
| `/api/v1/alerts/` | `GET` | Active emergency alerts and multilingual translations |
| `/api/v1/alerts/cap-feed.xml` | `GET` | Standard OASIS CAP 1.2 emergency XML feed |
| `/api/v1/reports/submit` | `POST` | Submit crowdsourced field hazard report |
| `/api/v1/roads/` | `GET` | Lifeline highway corridor status and blockage logs |
| `/ws/live` | `WebSocket` | Real-time 4-second IoT sensor telemetry stream |

---

## 12. Operational & Decision-Support Notice

> [!IMPORTANT]
> **TerrainTrace-NER** is an AI-assisted early warning and decision-support prototype. Live meteorological inputs are retrieved via open weather observation grids. IoT telemetry feeds and operational GIS layers represent simulated in-situ stations for demonstration unless connected to a deployed physical sensor network gateway (`SENSOR_GATEWAY_URL`). This software is designed to assist disaster management authorities and should be used in conjunction with official directives from the National Disaster Management Authority (NDMA), State Disaster Management Authorities (SDMAs), and the Geological Survey of India (GSI).
