"""
Simulated Demo Risk Locations for GIS Visualization
====================================================

This module defines predefined geographic locations across all 8 NER states
with *simulated* environmental / geotechnical input parameters.

IMPORTANT — Transparency Notice
--------------------------------
All environmental and sensor values in this module are **simulated for prototype
demonstration purposes only**. They do NOT represent live sensor measurements,
real-time weather data, or actual field observations. In a production deployment,
these values would be replaced by real IoT sensor feeds, weather APIs (e.g.,
Open-Meteo / IMD), and field survey data.

Design Rationale (Avoiding an "All-Red" Map)
---------------------------------------------
- ~65 % of locations have LOW / MODERATE environmental conditions
  (gentle slopes 8-25°, low rainfall, stable lithology).
- ~20 % have ELEVATED conditions producing YELLOW/ORANGE predictions.
- ~15 % are HIGH-RISK CLUSTERS near known vulnerable corridors
  (Sonapur Tunnel, Teesta Valley, Dzüdza, Jatinga, Tupul) with steep slopes,
  heavy rainfall, saturated soil, and fragile lithology.

This module does NOT assign risk_level, risk_score, or map colours.
Those are determined solely by LandslidePredictiveEngine.predict_risk().
"""

from typing import List, Dict, Any


DEMO_RISK_LOCATIONS: List[Dict[str, Any]] = [
    # ====================================================================
    #  SIKKIM  (8 locations)
    # ====================================================================
    {
        "location_name": "Gangtok Ridge Viewpoint",
        "state": "Sikkim",
        "lat": 27.3389, "lng": 88.6065,
        "slope_deg": 18.0, "elevation_m": 1650.0,
        "rainfall_3d_mm": 45.0, "rainfall_24h_mm": 12.0,
        "soil_moisture_pct": 48.0,
        "inclinometer_tilt_rate_mm_day": 0.4,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Singtam Bazaar Slope",
        "state": "Sikkim",
        "lat": 27.2351, "lng": 88.4983,
        "slope_deg": 22.0, "elevation_m": 980.0,
        "rainfall_3d_mm": 65.0, "rainfall_24h_mm": 20.0,
        "soil_moisture_pct": 55.0,
        "inclinometer_tilt_rate_mm_day": 0.8,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Teesta Valley 29th Mile",
        "state": "Sikkim",
        "lat": 27.0620, "lng": 88.4325,
        "slope_deg": 48.0, "elevation_m": 620.0,
        "rainfall_3d_mm": 195.0, "rainfall_24h_mm": 72.0,
        "soil_moisture_pct": 91.0,
        "inclinometer_tilt_rate_mm_day": 9.2,
        "lithology_type": "Weathered Schist / Disang Flysch"
    },
    {
        "location_name": "Rangpo Check-Post Hill",
        "state": "Sikkim",
        "lat": 27.1762, "lng": 88.5284,
        "slope_deg": 15.0, "elevation_m": 520.0,
        "rainfall_3d_mm": 38.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 42.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Mangan Town Terrace",
        "state": "Sikkim",
        "lat": 27.5098, "lng": 88.5320,
        "slope_deg": 28.0, "elevation_m": 1280.0,
        "rainfall_3d_mm": 82.0, "rainfall_24h_mm": 30.0,
        "soil_moisture_pct": 63.0,
        "inclinometer_tilt_rate_mm_day": 1.8,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Lachung Valley Foot",
        "state": "Sikkim",
        "lat": 27.6870, "lng": 88.7430,
        "slope_deg": 12.0, "elevation_m": 2700.0,
        "rainfall_3d_mm": 35.0, "rainfall_24h_mm": 8.0,
        "soil_moisture_pct": 40.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Sevoke Road Cutting",
        "state": "Sikkim",
        "lat": 26.8821, "lng": 88.4735,
        "slope_deg": 35.0, "elevation_m": 250.0,
        "rainfall_3d_mm": 120.0, "rainfall_24h_mm": 48.0,
        "soil_moisture_pct": 74.0,
        "inclinometer_tilt_rate_mm_day": 3.8,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Pelling Helipad Escarpment",
        "state": "Sikkim",
        "lat": 27.2950, "lng": 88.2370,
        "slope_deg": 20.0, "elevation_m": 2150.0,
        "rainfall_3d_mm": 55.0, "rainfall_24h_mm": 15.0,
        "soil_moisture_pct": 50.0,
        "inclinometer_tilt_rate_mm_day": 0.6,
        "lithology_type": "Sandstone"
    },

    # ====================================================================
    #  ASSAM  (8 locations)
    # ====================================================================
    {
        "location_name": "Guwahati Kamakhya Hill",
        "state": "Assam",
        "lat": 26.1670, "lng": 91.7050,
        "slope_deg": 14.0, "elevation_m": 240.0,
        "rainfall_3d_mm": 42.0, "rainfall_24h_mm": 14.0,
        "soil_moisture_pct": 45.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Haflong Town Plateau",
        "state": "Assam",
        "lat": 25.1800, "lng": 93.0200,
        "slope_deg": 26.0, "elevation_m": 680.0,
        "rainfall_3d_mm": 90.0, "rainfall_24h_mm": 35.0,
        "soil_moisture_pct": 68.0,
        "inclinometer_tilt_rate_mm_day": 2.5,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Jatinga Valley Cleft",
        "state": "Assam",
        "lat": 25.1215, "lng": 92.9820,
        "slope_deg": 42.0, "elevation_m": 750.0,
        "rainfall_3d_mm": 175.0, "rainfall_24h_mm": 65.0,
        "soil_moisture_pct": 87.0,
        "inclinometer_tilt_rate_mm_day": 6.5,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Lumding Junction Embankment",
        "state": "Assam",
        "lat": 25.7500, "lng": 93.1700,
        "slope_deg": 10.0, "elevation_m": 120.0,
        "rainfall_3d_mm": 30.0, "rainfall_24h_mm": 8.0,
        "soil_moisture_pct": 38.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Maibang Road Shoulder",
        "state": "Assam",
        "lat": 25.3021, "lng": 93.1610,
        "slope_deg": 30.0, "elevation_m": 420.0,
        "rainfall_3d_mm": 105.0, "rainfall_24h_mm": 40.0,
        "soil_moisture_pct": 72.0,
        "inclinometer_tilt_rate_mm_day": 3.0,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Karbi Anglong Plateau Edge",
        "state": "Assam",
        "lat": 25.9500, "lng": 93.4800,
        "slope_deg": 16.0, "elevation_m": 580.0,
        "rainfall_3d_mm": 48.0, "rainfall_24h_mm": 12.0,
        "soil_moisture_pct": 50.0,
        "inclinometer_tilt_rate_mm_day": 0.5,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Silchar Riverbank Terrace",
        "state": "Assam",
        "lat": 24.8333, "lng": 92.7789,
        "slope_deg": 8.0, "elevation_m": 30.0,
        "rainfall_3d_mm": 25.0, "rainfall_24h_mm": 6.0,
        "soil_moisture_pct": 55.0,
        "inclinometer_tilt_rate_mm_day": 0.1,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Harangajao Rail Cut",
        "state": "Assam",
        "lat": 24.9500, "lng": 92.8500,
        "slope_deg": 33.0, "elevation_m": 350.0,
        "rainfall_3d_mm": 130.0, "rainfall_24h_mm": 50.0,
        "soil_moisture_pct": 78.0,
        "inclinometer_tilt_rate_mm_day": 4.2,
        "lithology_type": "Weathered Schist / Disang Flysch"
    },

    # ====================================================================
    #  MEGHALAYA  (8 locations)
    # ====================================================================
    {
        "location_name": "Shillong Peak Observation",
        "state": "Meghalaya",
        "lat": 25.5500, "lng": 91.8800,
        "slope_deg": 20.0, "elevation_m": 1960.0,
        "rainfall_3d_mm": 60.0, "rainfall_24h_mm": 18.0,
        "soil_moisture_pct": 52.0,
        "inclinometer_tilt_rate_mm_day": 0.6,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Sonapur Tunnel North Portal",
        "state": "Meghalaya",
        "lat": 25.1324, "lng": 92.3682,
        "slope_deg": 52.0, "elevation_m": 480.0,
        "rainfall_3d_mm": 220.0, "rainfall_24h_mm": 85.0,
        "soil_moisture_pct": 93.0,
        "inclinometer_tilt_rate_mm_day": 11.5,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Jowai Market Road",
        "state": "Meghalaya",
        "lat": 25.4484, "lng": 92.2038,
        "slope_deg": 15.0, "elevation_m": 1320.0,
        "rainfall_3d_mm": 50.0, "rainfall_24h_mm": 15.0,
        "soil_moisture_pct": 46.0,
        "inclinometer_tilt_rate_mm_day": 0.4,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Cherrapunji East Slope",
        "state": "Meghalaya",
        "lat": 25.2740, "lng": 91.7200,
        "slope_deg": 32.0, "elevation_m": 1380.0,
        "rainfall_3d_mm": 160.0, "rainfall_24h_mm": 60.0,
        "soil_moisture_pct": 82.0,
        "inclinometer_tilt_rate_mm_day": 4.0,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Dawki Border Road",
        "state": "Meghalaya",
        "lat": 25.1850, "lng": 92.0130,
        "slope_deg": 12.0, "elevation_m": 200.0,
        "rainfall_3d_mm": 35.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 44.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Nongstoin Bypass Cut",
        "state": "Meghalaya",
        "lat": 25.5170, "lng": 91.2640,
        "slope_deg": 24.0, "elevation_m": 1100.0,
        "rainfall_3d_mm": 70.0, "rainfall_24h_mm": 22.0,
        "soil_moisture_pct": 58.0,
        "inclinometer_tilt_rate_mm_day": 1.2,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Mawsynram Escarpment",
        "state": "Meghalaya",
        "lat": 25.2970, "lng": 91.5830,
        "slope_deg": 38.0, "elevation_m": 1400.0,
        "rainfall_3d_mm": 185.0, "rainfall_24h_mm": 70.0,
        "soil_moisture_pct": 88.0,
        "inclinometer_tilt_rate_mm_day": 5.2,
        "lithology_type": "Weathered Schist / Disang Flysch"
    },
    {
        "location_name": "Tura Peak Saddle",
        "state": "Meghalaya",
        "lat": 25.5130, "lng": 90.2150,
        "slope_deg": 19.0, "elevation_m": 870.0,
        "rainfall_3d_mm": 40.0, "rainfall_24h_mm": 12.0,
        "soil_moisture_pct": 47.0,
        "inclinometer_tilt_rate_mm_day": 0.5,
        "lithology_type": "Granite / Gneiss"
    },

    # ====================================================================
    #  ARUNACHAL PRADESH  (8 locations)
    # ====================================================================
    {
        "location_name": "Itanagar Naharlagun Hill",
        "state": "Arunachal Pradesh",
        "lat": 27.1020, "lng": 93.6150,
        "slope_deg": 22.0, "elevation_m": 350.0,
        "rainfall_3d_mm": 55.0, "rainfall_24h_mm": 16.0,
        "soil_moisture_pct": 50.0,
        "inclinometer_tilt_rate_mm_day": 0.7,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Bomdila Pass Approach",
        "state": "Arunachal Pradesh",
        "lat": 27.2645, "lng": 92.4230,
        "slope_deg": 30.0, "elevation_m": 2520.0,
        "rainfall_3d_mm": 95.0, "rainfall_24h_mm": 35.0,
        "soil_moisture_pct": 65.0,
        "inclinometer_tilt_rate_mm_day": 2.2,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Sela Pass Descent Hairpin",
        "state": "Arunachal Pradesh",
        "lat": 27.5020, "lng": 92.1050,
        "slope_deg": 44.0, "elevation_m": 4170.0,
        "rainfall_3d_mm": 140.0, "rainfall_24h_mm": 55.0,
        "soil_moisture_pct": 80.0,
        "inclinometer_tilt_rate_mm_day": 5.5,
        "lithology_type": "Weathered Schist / Disang Flysch"
    },
    {
        "location_name": "Tawang Monastery Road",
        "state": "Arunachal Pradesh",
        "lat": 27.5861, "lng": 91.8656,
        "slope_deg": 18.0, "elevation_m": 3050.0,
        "rainfall_3d_mm": 42.0, "rainfall_24h_mm": 12.0,
        "soil_moisture_pct": 45.0,
        "inclinometer_tilt_rate_mm_day": 0.4,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Bhalukpong Forest Entry",
        "state": "Arunachal Pradesh",
        "lat": 27.0142, "lng": 92.6468,
        "slope_deg": 14.0, "elevation_m": 220.0,
        "rainfall_3d_mm": 32.0, "rainfall_24h_mm": 8.0,
        "soil_moisture_pct": 40.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Dirang Valley Shoulder",
        "state": "Arunachal Pradesh",
        "lat": 27.3562, "lng": 92.2410,
        "slope_deg": 25.0, "elevation_m": 1600.0,
        "rainfall_3d_mm": 75.0, "rainfall_24h_mm": 25.0,
        "soil_moisture_pct": 58.0,
        "inclinometer_tilt_rate_mm_day": 1.5,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Tenga Valley Bridge",
        "state": "Arunachal Pradesh",
        "lat": 27.1812, "lng": 92.4285,
        "slope_deg": 10.0, "elevation_m": 760.0,
        "rainfall_3d_mm": 28.0, "rainfall_24h_mm": 7.0,
        "soil_moisture_pct": 38.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Ziro Plateau Edge",
        "state": "Arunachal Pradesh",
        "lat": 27.5380, "lng": 93.8310,
        "slope_deg": 16.0, "elevation_m": 1620.0,
        "rainfall_3d_mm": 40.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 44.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Sandstone"
    },

    # ====================================================================
    #  NAGALAND  (8 locations)
    # ====================================================================
    {
        "location_name": "Kohima War Cemetery Hill",
        "state": "Nagaland",
        "lat": 25.6751, "lng": 94.1086,
        "slope_deg": 20.0, "elevation_m": 1460.0,
        "rainfall_3d_mm": 55.0, "rainfall_24h_mm": 18.0,
        "soil_moisture_pct": 52.0,
        "inclinometer_tilt_rate_mm_day": 0.7,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Dzüdza Bridge Approach",
        "state": "Nagaland",
        "lat": 25.7225, "lng": 93.9230,
        "slope_deg": 45.0, "elevation_m": 880.0,
        "rainfall_3d_mm": 165.0, "rainfall_24h_mm": 62.0,
        "soil_moisture_pct": 86.0,
        "inclinometer_tilt_rate_mm_day": 6.8,
        "lithology_type": "Weathered Schist / Disang Flysch"
    },
    {
        "location_name": "Dimapur Foothills Station",
        "state": "Nagaland",
        "lat": 25.9068, "lng": 93.7270,
        "slope_deg": 8.0, "elevation_m": 150.0,
        "rainfall_3d_mm": 28.0, "rainfall_24h_mm": 7.0,
        "soil_moisture_pct": 40.0,
        "inclinometer_tilt_rate_mm_day": 0.1,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Chumukedima Road Cut",
        "state": "Nagaland",
        "lat": 25.8124, "lng": 93.7741,
        "slope_deg": 25.0, "elevation_m": 520.0,
        "rainfall_3d_mm": 78.0, "rainfall_24h_mm": 28.0,
        "soil_moisture_pct": 62.0,
        "inclinometer_tilt_rate_mm_day": 1.6,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Mokokchung Town Slope",
        "state": "Nagaland",
        "lat": 26.3234, "lng": 94.5210,
        "slope_deg": 22.0, "elevation_m": 1350.0,
        "rainfall_3d_mm": 60.0, "rainfall_24h_mm": 20.0,
        "soil_moisture_pct": 55.0,
        "inclinometer_tilt_rate_mm_day": 0.9,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Wokha Ridge Path",
        "state": "Nagaland",
        "lat": 26.1020, "lng": 94.2550,
        "slope_deg": 18.0, "elevation_m": 1310.0,
        "rainfall_3d_mm": 45.0, "rainfall_24h_mm": 14.0,
        "soil_moisture_pct": 48.0,
        "inclinometer_tilt_rate_mm_day": 0.5,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Tuensang East Terrace",
        "state": "Nagaland",
        "lat": 26.2710, "lng": 94.8280,
        "slope_deg": 15.0, "elevation_m": 1420.0,
        "rainfall_3d_mm": 38.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 43.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Phek Valley Rim",
        "state": "Nagaland",
        "lat": 25.6690, "lng": 94.4780,
        "slope_deg": 28.0, "elevation_m": 1580.0,
        "rainfall_3d_mm": 88.0, "rainfall_24h_mm": 32.0,
        "soil_moisture_pct": 65.0,
        "inclinometer_tilt_rate_mm_day": 2.0,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },

    # ====================================================================
    #  MANIPUR  (7 locations)
    # ====================================================================
    {
        "location_name": "Imphal Valley East Ridge",
        "state": "Manipur",
        "lat": 24.8170, "lng": 93.9368,
        "slope_deg": 12.0, "elevation_m": 790.0,
        "rainfall_3d_mm": 35.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 42.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Tupul Railway Yard Zone",
        "state": "Manipur",
        "lat": 24.7120, "lng": 93.6820,
        "slope_deg": 50.0, "elevation_m": 650.0,
        "rainfall_3d_mm": 210.0, "rainfall_24h_mm": 80.0,
        "soil_moisture_pct": 94.0,
        "inclinometer_tilt_rate_mm_day": 10.0,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Maram Bazaar Escarpment",
        "state": "Manipur",
        "lat": 25.3210, "lng": 94.0320,
        "slope_deg": 14.0, "elevation_m": 1100.0,
        "rainfall_3d_mm": 40.0, "rainfall_24h_mm": 12.0,
        "soil_moisture_pct": 48.0,
        "inclinometer_tilt_rate_mm_day": 0.4,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Tamenglong Cliffside",
        "state": "Manipur",
        "lat": 24.9810, "lng": 93.5120,
        "slope_deg": 36.0, "elevation_m": 920.0,
        "rainfall_3d_mm": 125.0, "rainfall_24h_mm": 48.0,
        "soil_moisture_pct": 76.0,
        "inclinometer_tilt_rate_mm_day": 3.5,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Pallel Hill Climb",
        "state": "Manipur",
        "lat": 24.4600, "lng": 94.0200,
        "slope_deg": 22.0, "elevation_m": 960.0,
        "rainfall_3d_mm": 58.0, "rainfall_24h_mm": 18.0,
        "soil_moisture_pct": 53.0,
        "inclinometer_tilt_rate_mm_day": 0.8,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Moreh Border Gate",
        "state": "Manipur",
        "lat": 24.2483, "lng": 94.3056,
        "slope_deg": 10.0, "elevation_m": 270.0,
        "rainfall_3d_mm": 30.0, "rainfall_24h_mm": 8.0,
        "soil_moisture_pct": 38.0,
        "inclinometer_tilt_rate_mm_day": 0.1,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Senapati-Kangpokpi Pass",
        "state": "Manipur",
        "lat": 25.2670, "lng": 93.8480,
        "slope_deg": 26.0, "elevation_m": 1350.0,
        "rainfall_3d_mm": 85.0, "rainfall_24h_mm": 30.0,
        "soil_moisture_pct": 64.0,
        "inclinometer_tilt_rate_mm_day": 1.9,
        "lithology_type": "Siltstone"
    },

    # ====================================================================
    #  MIZORAM  (7 locations)
    # ====================================================================
    {
        "location_name": "Aizawl Durtlang Hills",
        "state": "Mizoram",
        "lat": 23.7710, "lng": 92.7280,
        "slope_deg": 25.0, "elevation_m": 1130.0,
        "rainfall_3d_mm": 65.0, "rainfall_24h_mm": 22.0,
        "soil_moisture_pct": 56.0,
        "inclinometer_tilt_rate_mm_day": 1.0,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Kolasib Kawnpui Sinking Zone",
        "state": "Mizoram",
        "lat": 24.0150, "lng": 92.6850,
        "slope_deg": 34.0, "elevation_m": 420.0,
        "rainfall_3d_mm": 130.0, "rainfall_24h_mm": 50.0,
        "soil_moisture_pct": 79.0,
        "inclinometer_tilt_rate_mm_day": 4.5,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Lunglei Town Terrace",
        "state": "Mizoram",
        "lat": 22.8870, "lng": 92.7410,
        "slope_deg": 20.0, "elevation_m": 850.0,
        "rainfall_3d_mm": 50.0, "rainfall_24h_mm": 15.0,
        "soil_moisture_pct": 50.0,
        "inclinometer_tilt_rate_mm_day": 0.6,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Champhai Valley Floor",
        "state": "Mizoram",
        "lat": 23.4570, "lng": 93.3250,
        "slope_deg": 10.0, "elevation_m": 900.0,
        "rainfall_3d_mm": 32.0, "rainfall_24h_mm": 8.0,
        "soil_moisture_pct": 40.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Serchhip Bazaar Slope",
        "state": "Mizoram",
        "lat": 23.3150, "lng": 92.8440,
        "slope_deg": 18.0, "elevation_m": 1080.0,
        "rainfall_3d_mm": 45.0, "rainfall_24h_mm": 14.0,
        "soil_moisture_pct": 48.0,
        "inclinometer_tilt_rate_mm_day": 0.5,
        "lithology_type": "Granite / Gneiss"
    },
    {
        "location_name": "Vairengte Border Cut",
        "state": "Mizoram",
        "lat": 24.5021, "lng": 92.7640,
        "slope_deg": 28.0, "elevation_m": 380.0,
        "rainfall_3d_mm": 95.0, "rainfall_24h_mm": 35.0,
        "soil_moisture_pct": 67.0,
        "inclinometer_tilt_rate_mm_day": 2.2,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Mamit Hill Station",
        "state": "Mizoram",
        "lat": 23.9250, "lng": 92.4830,
        "slope_deg": 15.0, "elevation_m": 620.0,
        "rainfall_3d_mm": 38.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 44.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Sandstone"
    },

    # ====================================================================
    #  TRIPURA  (7 locations)
    # ====================================================================
    {
        "location_name": "Agartala Airport Slope",
        "state": "Tripura",
        "lat": 23.8860, "lng": 91.2420,
        "slope_deg": 8.0, "elevation_m": 20.0,
        "rainfall_3d_mm": 25.0, "rainfall_24h_mm": 6.0,
        "soil_moisture_pct": 38.0,
        "inclinometer_tilt_rate_mm_day": 0.1,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Dhalai Ambassa Road",
        "state": "Tripura",
        "lat": 23.9220, "lng": 91.8530,
        "slope_deg": 22.0, "elevation_m": 120.0,
        "rainfall_3d_mm": 70.0, "rainfall_24h_mm": 22.0,
        "soil_moisture_pct": 58.0,
        "inclinometer_tilt_rate_mm_day": 1.2,
        "lithology_type": "Siltstone"
    },
    {
        "location_name": "Unakoti Hill Temple",
        "state": "Tripura",
        "lat": 24.3170, "lng": 92.0720,
        "slope_deg": 28.0, "elevation_m": 280.0,
        "rainfall_3d_mm": 90.0, "rainfall_24h_mm": 32.0,
        "soil_moisture_pct": 68.0,
        "inclinometer_tilt_rate_mm_day": 2.0,
        "lithology_type": "Shale & Siltstone (Fragile)"
    },
    {
        "location_name": "Khowai River Escarpment",
        "state": "Tripura",
        "lat": 24.0640, "lng": 91.6050,
        "slope_deg": 16.0, "elevation_m": 80.0,
        "rainfall_3d_mm": 40.0, "rainfall_24h_mm": 12.0,
        "soil_moisture_pct": 46.0,
        "inclinometer_tilt_rate_mm_day": 0.4,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "Jampui Hills North",
        "state": "Tripura",
        "lat": 24.1200, "lng": 92.2650,
        "slope_deg": 32.0, "elevation_m": 850.0,
        "rainfall_3d_mm": 110.0, "rainfall_24h_mm": 42.0,
        "soil_moisture_pct": 75.0,
        "inclinometer_tilt_rate_mm_day": 3.2,
        "lithology_type": "Weathered Schist / Disang Flysch"
    },
    {
        "location_name": "Dharmanagar Town",
        "state": "Tripura",
        "lat": 24.3830, "lng": 92.1670,
        "slope_deg": 12.0, "elevation_m": 45.0,
        "rainfall_3d_mm": 30.0, "rainfall_24h_mm": 8.0,
        "soil_moisture_pct": 42.0,
        "inclinometer_tilt_rate_mm_day": 0.2,
        "lithology_type": "Sandstone"
    },
    {
        "location_name": "South Tripura Belonia Hill",
        "state": "Tripura",
        "lat": 23.2510, "lng": 91.4520,
        "slope_deg": 14.0, "elevation_m": 60.0,
        "rainfall_3d_mm": 35.0, "rainfall_24h_mm": 10.0,
        "soil_moisture_pct": 45.0,
        "inclinometer_tilt_rate_mm_day": 0.3,
        "lithology_type": "Sandstone"
    },
]
