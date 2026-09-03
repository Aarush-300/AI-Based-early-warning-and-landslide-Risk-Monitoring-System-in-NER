# Comprehensive GIS spatial data for North Eastern Region (NER)

NER_STATES_DATA = [
    {
        "name": "Sikkim",
        "capital": "Gangtok",
        "center": [27.5330, 88.5122],
        "high_risk_districts": ["East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim", "Pakyong", "Soreng"],
        "primary_geology": "Precambrian Daling-Darjeeling Schists, fragile gneisses and quartzites",
        "average_monsoon_rainfall_mm": 2800,
        "vulnerability_score": 92
    },
    {
        "name": "Assam",
        "capital": "Dispur",
        "center": [26.2006, 92.9376],
        "high_risk_districts": ["Dima Hasao (North Cachar Hills)", "Karbi Anglong", "Cachar", "Hailakandi", "Kamrup Metropolitan"],
        "primary_geology": "Disang-Barail shales, tertiary sedimentary rock prone to shearing",
        "average_monsoon_rainfall_mm": 2400,
        "vulnerability_score": 85
    },
    {
        "name": "Meghalaya",
        "capital": "Shillong",
        "center": [25.4670, 91.3662],
        "high_risk_districts": ["East Khasi Hills", "West Jaintia Hills", "East Jaintia Hills", "South West Khasi Hills", "Ri-Bhoi"],
        "primary_geology": "Shillong Plateau sandstones, weathered limestone karst, lateritic soils",
        "average_monsoon_rainfall_mm": 3900,
        "vulnerability_score": 94
    },
    {
        "name": "Arunachal Pradesh",
        "capital": "Itanagar",
        "center": [28.2180, 94.7278],
        "high_risk_districts": ["West Kameng", "Tawang", "Papum Pare", "Kurung Kumey", "Dibang Valley", "Upper Siang"],
        "primary_geology": "Siwalik Group friable sandstones, Main Central Thrust tectonic zone",
        "average_monsoon_rainfall_mm": 3200,
        "vulnerability_score": 90
    },
    {
        "name": "Nagaland",
        "capital": "Kohima",
        "center": [26.1584, 94.5624],
        "high_risk_districts": ["Kohima", "Dimapur", "Phek", "Wokha", "Mokokchung", "Tuensang"],
        "primary_geology": "Disang flysch sequence (thick bedded splintery shales), highly weathered",
        "average_monsoon_rainfall_mm": 2100,
        "vulnerability_score": 89
    },
    {
        "name": "Manipur",
        "capital": "Imphal",
        "center": [24.6637, 93.9063],
        "high_risk_districts": ["Churachandpur", "Kangpokpi", "Tamenglong", "Senapati", "Noney", "Tengnoupal"],
        "primary_geology": "Tertiary sedimentary shales and mudstones, Indo-Burman thrust fold belt",
        "average_monsoon_rainfall_mm": 1950,
        "vulnerability_score": 88
    },
    {
        "name": "Mizoram",
        "capital": "Aizawl",
        "center": [23.1645, 92.9376],
        "high_risk_districts": ["Aizawl", "Kolasib", "Lunglei", "Champhai", "Serchhip", "Mamit"],
        "primary_geology": "Surma and Tipam Group rhythmic sandstone-shale alterations",
        "average_monsoon_rainfall_mm": 2600,
        "vulnerability_score": 87
    },
    {
        "name": "Tripura",
        "capital": "Agartala",
        "center": [23.8315, 91.2868],
        "high_risk_districts": ["Dhalai", "North Tripura", "Unakoti", "Khowai", "South Tripura"],
        "primary_geology": "Unconsolidated Tipam sandstones and Bokabil silty clay",
        "average_monsoon_rainfall_mm": 2200,
        "vulnerability_score": 76
    }
]

# Strategic Highway Corridors across North East
HIGHWAY_CORRIDORS = [
    {
        "corridor_id": "NH-10-SIK",
        "highway_name": "NH-10 (Sikkim Lifeline)",
        "stretch_name": "Sevoke - Teesta Bazaar - Rangpo - Singtam - Gangtok",
        "state": "Sikkim",
        "start_point": "Sevoke (WB)",
        "end_point": "Gangtok (Sikkim)",
        "status": "PARTIALLY_BLOCKED",
        "risk_level": "RED",
        "blockage_cause": "Major debris flow and river erosion near 29th Mile & Teesta Bazaar",
        "clearing_eta_hours": 6.5,
        "stranded_vehicles_estimate": 140,
        "alternate_route": "Via Gorubathan - Lava - Reshi - Rhenock - Singtam (Restricted to Light Vehicles)",
        "alternate_route_extra_km": 48.0,
        "alternate_route_extra_hours": 3.2,
        "response_priority_score": 96.5,
        "coordinates": [
            [26.8821, 88.4735],  # Sevoke
            [27.0601, 88.4312],  # Teesta Bazaar
            [27.1762, 88.5284],  # Rangpo
            [27.2351, 88.4983],  # Singtam
            [27.3389, 88.6065]   # Gangtok
        ]
    },
    {
        "corridor_id": "NH-29-NAG",
        "highway_name": "NH-29 (Kohima-Manipur Corridor)",
        "stretch_name": "Dimapur - Chumukedima - Phesama - Kohima",
        "state": "Nagaland",
        "start_point": "Dimapur",
        "end_point": "Kohima",
        "status": "HIGH_RISK_ADVISORY",
        "risk_level": "ORANGE",
        "blockage_cause": "Active slope sinking and tension cracks at Dzüdza Bridge approach",
        "clearing_eta_hours": 2.0,
        "stranded_vehicles_estimate": 45,
        "alternate_route": "Via Old Tsiesema - Peducha bypass road (Single lane only)",
        "alternate_route_extra_km": 22.5,
        "alternate_route_extra_hours": 1.8,
        "response_priority_score": 88.0,
        "coordinates": [
            [25.9068, 93.7270],  # Dimapur
            [25.8124, 93.7741],  # Chumukedima
            [25.7210, 93.9210],  # Dzüdza
            [25.6751, 94.1086]   # Kohima
        ]
    },
    {
        "corridor_id": "NH-06-MEG",
        "highway_name": "NH-06 (Barak Valley & Mizoram Lifeline)",
        "stretch_name": "Shillong - Jowai - Sonapur Tunnel - Ratacherra - Silchar",
        "state": "Meghalaya",
        "start_point": "Shillong",
        "end_point": "Silchar (Assam)",
        "status": "FULLY_BLOCKED",
        "risk_level": "RED",
        "blockage_cause": "Massive mudslide covering 120m highway near Sonapur Tunnel mouth",
        "clearing_eta_hours": 12.0,
        "stranded_vehicles_estimate": 320,
        "alternate_route": "No immediate heavy vehicular detour; Light vehicles diverted via Umkiang-Lumshnong rural tracks",
        "alternate_route_extra_km": 74.0,
        "alternate_route_extra_hours": 5.5,
        "response_priority_score": 98.2,
        "coordinates": [
            [25.5788, 91.8933],  # Shillong
            [25.4484, 92.2038],  # Jowai
            [25.1320, 92.3680],  # Sonapur Tunnel
            [25.0210, 92.4850],  # Ratacherra
            [24.8333, 92.7789]   # Silchar
        ]
    },
    {
        "corridor_id": "NH-102-MAN",
        "highway_name": "NH-102 (Asian Highway 1)",
        "stretch_name": "Imphal - Thoubal - Pallel - Tengnoupal - Moreh",
        "state": "Manipur",
        "start_point": "Imphal",
        "end_point": "Moreh (Border)",
        "status": "CLEAR",
        "risk_level": "YELLOW",
        "blockage_cause": "Minor gravel spill at Pallel Hill Climb; BRO road crew on standby",
        "clearing_eta_hours": 0.5,
        "stranded_vehicles_estimate": 0,
        "alternate_route": "Standard highway operational",
        "alternate_route_extra_km": 0.0,
        "alternate_route_extra_hours": 0.0,
        "response_priority_score": 62.0,
        "coordinates": [
            [24.8170, 93.9368],  # Imphal
            [24.6382, 93.9961],  # Thoubal
            [24.4600, 94.0200],  # Pallel
            [24.3312, 94.1523],  # Tengnoupal
            [24.2483, 94.3056]   # Moreh
        ]
    },
    {
        "corridor_id": "NH-13-ARU",
        "highway_name": "NH-13 (Trans-Arunachal Highway)",
        "stretch_name": "Bhalukpong - Tenga - Bomdila - Dirang - Tawang",
        "state": "Arunachal Pradesh",
        "start_point": "Bhalukpong",
        "end_point": "Tawang",
        "status": "HIGH_RISK_ADVISORY",
        "risk_level": "ORANGE",
        "blockage_cause": "Shooting stones and waterlogging near Sela Pass descent",
        "clearing_eta_hours": 3.0,
        "stranded_vehicles_estimate": 30,
        "alternate_route": "Via Balemu-Kalaktang-Shergaon road",
        "alternate_route_extra_km": 36.0,
        "alternate_route_extra_hours": 2.4,
        "response_priority_score": 84.5,
        "coordinates": [
            [27.0142, 92.6468],  # Bhalukpong
            [27.1812, 92.4285],  # Tenga
            [27.2645, 92.4230],  # Bomdila
            [27.3562, 92.2410],  # Dirang
            [27.5861, 91.8656]   # Tawang
        ]
    },
    {
        "corridor_id": "NH-54-MIZ",
        "highway_name": "NH-306 / NH-54 (Aizawl Corridor)",
        "stretch_name": "Silchar - Vairengte - Bilkhawthlir - Kolasib - Aizawl",
        "state": "Mizoram",
        "start_point": "Silchar (Assam)",
        "end_point": "Aizawl (Mizoram)",
        "status": "CLEAR",
        "risk_level": "YELLOW",
        "blockage_cause": "Minor soil creeping near Kawnpui; single lane active",
        "clearing_eta_hours": 1.0,
        "stranded_vehicles_estimate": 15,
        "alternate_route": "Via Bairabi - Mamit road for essential supplies",
        "alternate_route_extra_km": 52.0,
        "alternate_route_extra_hours": 3.0,
        "response_priority_score": 74.0,
        "coordinates": [
            [24.8333, 92.7789],  # Silchar
            [24.5021, 92.7640],  # Vairengte
            [24.2250, 92.6820],  # Kolasib
            [23.7271, 92.7176]   # Aizawl
        ]
    },
    {
        "corridor_id": "NH-27-ASM",
        "highway_name": "NH-27 / Dima Hasao Hill Highway",
        "stretch_name": "Lumding - Maibang - Haflong - Jatinga - Harangajao",
        "state": "Assam",
        "start_point": "Lumding",
        "end_point": "Silchar",
        "status": "HIGH_RISK_ADVISORY",
        "risk_level": "ORANGE",
        "blockage_cause": "Subgrade settlement and slope subsidence at Jatinga Valley",
        "clearing_eta_hours": 4.5,
        "stranded_vehicles_estimate": 60,
        "alternate_route": "Restricted movement; Railway goods trains active on upper alignment",
        "alternate_route_extra_km": 30.0,
        "alternate_route_extra_hours": 2.0,
        "response_priority_score": 86.0,
        "coordinates": [
            [25.7500, 93.1700],  # Lumding
            [25.3021, 93.1610],  # Maibang
            [25.1800, 93.0200],  # Haflong
            [25.1200, 92.9800],  # Jatinga
            [24.9500, 92.8500]   # Harangajao
        ]
    }
]

# IoT Geotechnical Sensor Stations deployed on vulnerable slopes
IOT_SENSOR_STATIONS = [
    {
        "sensor_id": "IOT-MEG-01",
        "name": "Sonapur Tunnel Geotech Node Alpha",
        "location_name": "Sonapur Tunnel North Portal (NH-06)",
        "state": "Meghalaya",
        "district": "East Jaintia Hills",
        "lat": 25.1324,
        "lng": 92.3682,
        "highway_corridor": "NH-06 (Barak Valley & Mizoram Lifeline)",
        "pore_water_pressure_kpa": 142.6,
        "soil_moisture_pct": 89.4,
        "inclinometer_tilt_deg": 4.82,
        "displacement_rate_mm_day": 14.5,
        "acoustic_emission_db": 68.2,
        "current_rainfall_mm_h": 28.5,
        "cumulative_24h_rainfall_mm": 194.0,
        "status": "CRITICAL",
        "battery_pct": 94
    },
    {
        "sensor_id": "IOT-SIK-01",
        "name": "Teesta Basin Slope Inclinometer Array",
        "location_name": "29th Mile / Seti Jhora (NH-10)",
        "state": "Sikkim",
        "district": "East Sikkim",
        "lat": 27.0620,
        "lng": 88.4325,
        "highway_corridor": "NH-10 (Sikkim Lifeline)",
        "pore_water_pressure_kpa": 118.0,
        "soil_moisture_pct": 82.1,
        "inclinometer_tilt_deg": 3.45,
        "displacement_rate_mm_day": 9.2,
        "acoustic_emission_db": 54.0,
        "current_rainfall_mm_h": 18.0,
        "cumulative_24h_rainfall_mm": 142.5,
        "status": "WARNING",
        "battery_pct": 88
    },
    {
        "sensor_id": "IOT-NAG-01",
        "name": "Dzüdza Slide Real-Time Deformation Sensor",
        "location_name": "Dzüdza River Valley Bridge Approach (NH-29)",
        "state": "Nagaland",
        "district": "Kohima",
        "lat": 25.7225,
        "lng": 93.9230,
        "highway_corridor": "NH-29 (Kohima-Manipur Corridor)",
        "pore_water_pressure_kpa": 98.5,
        "soil_moisture_pct": 76.8,
        "inclinometer_tilt_deg": 2.65,
        "displacement_rate_mm_day": 6.8,
        "acoustic_emission_db": 49.5,
        "current_rainfall_mm_h": 12.5,
        "cumulative_24h_rainfall_mm": 98.0,
        "status": "WARNING",
        "battery_pct": 91
    },
    {
        "sensor_id": "IOT-ASM-01",
        "name": "Dima Hasao Hill Sentry Node",
        "location_name": "Jatinga Cleft Slope Section (NH-27)",
        "state": "Assam",
        "district": "Dima Hasao (North Cachar Hills)",
        "lat": 25.1215,
        "lng": 92.9820,
        "highway_corridor": "NH-27 / Dima Hasao Hill Highway",
        "pore_water_pressure_kpa": 84.0,
        "soil_moisture_pct": 69.5,
        "inclinometer_tilt_deg": 1.95,
        "displacement_rate_mm_day": 4.1,
        "acoustic_emission_db": 38.0,
        "current_rainfall_mm_h": 9.0,
        "cumulative_24h_rainfall_mm": 76.0,
        "status": "WATCH",
        "battery_pct": 96
    },
    {
        "sensor_id": "IOT-MAN-01",
        "name": "Maram-Senapati Slope Piezometer",
        "location_name": "Maram Bazaar Escarpment (NH-02)",
        "state": "Manipur",
        "district": "Senapati",
        "lat": 25.3210,
        "lng": 94.0320,
        "highway_corridor": "NH-02 Imphal-Kohima Route",
        "pore_water_pressure_kpa": 52.0,
        "soil_moisture_pct": 58.0,
        "inclinometer_tilt_deg": 0.85,
        "displacement_rate_mm_day": 1.2,
        "acoustic_emission_db": 22.0,
        "current_rainfall_mm_h": 3.5,
        "cumulative_24h_rainfall_mm": 32.0,
        "status": "NORMAL",
        "battery_pct": 99
    },
    {
        "sensor_id": "IOT-MIZ-01",
        "name": "Kolasib Slope Telemetry Array",
        "location_name": "Kawnpui Sinking Zone (NH-54)",
        "state": "Mizoram",
        "district": "Kolasib",
        "lat": 24.0150,
        "lng": 92.6850,
        "highway_corridor": "NH-306 / NH-54 (Aizawl Corridor)",
        "pore_water_pressure_kpa": 61.2,
        "soil_moisture_pct": 62.4,
        "inclinometer_tilt_deg": 1.15,
        "displacement_rate_mm_day": 2.4,
        "acoustic_emission_db": 28.5,
        "current_rainfall_mm_h": 5.0,
        "cumulative_24h_rainfall_mm": 45.0,
        "status": "NORMAL",
        "battery_pct": 95
    },
    {
        "sensor_id": "IOT-ARU-01",
        "name": "Sela Pass Geotechnical Watch Node",
        "location_name": "Baisakhi Military Camp Slope (NH-13)",
        "state": "Arunachal Pradesh",
        "district": "West Kameng",
        "lat": 27.5020,
        "lng": 92.1050,
        "highway_corridor": "NH-13 (Trans-Arunachal Highway)",
        "pore_water_pressure_kpa": 88.0,
        "soil_moisture_pct": 74.0,
        "inclinometer_tilt_deg": 2.10,
        "displacement_rate_mm_day": 5.5,
        "acoustic_emission_db": 42.0,
        "current_rainfall_mm_h": 11.0,
        "cumulative_24h_rainfall_mm": 88.0,
        "status": "WATCH",
        "battery_pct": 92
    }
]

# Historical Landslide Records Catalog for NER
HISTORICAL_LANDSLIDES = [
    {
        "id": "LS-HIST-01",
        "location": "Sonapur Tunnel Mudflow",
        "state": "Meghalaya",
        "district": "East Jaintia Hills",
        "lat": 25.1320,
        "lng": 92.3680,
        "date": "2023-06-16",
        "rainfall_trigger_mm": 312.0,
        "fatalities": 0,
        "disruption_days": 6,
        "material_volume_m3": 45000,
        "impact_summary": "Severed road link to Barak Valley (Assam), Mizoram, and Tripura for nearly a week."
    },
    {
        "id": "LS-HIST-02",
        "location": "Phesama Landslide",
        "state": "Nagaland",
        "district": "Kohima",
        "lat": 25.6321,
        "lng": 94.1120,
        "date": "2015-08-18",
        "rainfall_trigger_mm": 240.0,
        "fatalities": 1,
        "disruption_days": 18,
        "material_volume_m3": 85000,
        "impact_summary": "NH-29 completely severed; massive sinking of over 300 meters of highway."
    },
    {
        "id": "LS-HIST-03",
        "location": "South Lhonak Lake GLOF & Teesta Valley Landslides",
        "state": "Sikkim",
        "district": "North Sikkim",
        "lat": 27.6980,
        "lng": 88.2140,
        "date": "2023-10-04",
        "rainfall_trigger_mm": 180.0,
        "fatalities": 42,
        "disruption_days": 45,
        "material_volume_m3": 250000,
        "impact_summary": "Multiple bridges washed away, massive toe erosion triggered over 70 simultaneous slope collapses."
    },
    {
        "id": "LS-HIST-04",
        "location": "Tupul Railway Yard Debris Avalanche",
        "state": "Manipur",
        "district": "Noney",
        "lat": 24.7120,
        "lng": 93.6820,
        "date": "2022-06-30",
        "rainfall_trigger_mm": 285.0,
        "fatalities": 61,
        "disruption_days": 21,
        "material_volume_m3": 180000,
        "impact_summary": "Damming of Ijej river creating artificial lake, massive loss of life at Territorial Army railway camp."
    },
    {
        "id": "LS-HIST-05",
        "location": "Dima Hasao Mass Subsidence",
        "state": "Assam",
        "district": "Dima Hasao",
        "lat": 25.1850,
        "lng": 93.0250,
        "date": "2022-05-15",
        "rainfall_trigger_mm": 410.0,
        "fatalities": 8,
        "disruption_days": 30,
        "material_volume_m3": 120000,
        "impact_summary": "New Haflong railway station submerged in mud, tracks hanging in mid-air."
    },
    {
        "id": "LS-HIST-06",
        "location": "Laipuitlang Mass Movement",
        "state": "Mizoram",
        "district": "Aizawl",
        "lat": 23.7380,
        "lng": 92.7230,
        "date": "2013-05-11",
        "rainfall_trigger_mm": 195.0,
        "fatalities": 17,
        "disruption_days": 12,
        "material_volume_m3": 35000,
        "impact_summary": "Urban slope failure triggered by excessive quarrying and rainwater seepage."
    }
]

# Emergency Evacuation Centers, NDRF/SDRF hubs, and Field Hospitals
EMERGENCY_RESOURCES = [
    {
        "id": "RES-01",
        "name": "12th Battalion NDRF Base Camp",
        "type": "NDRF_BASE",
        "state": "Arunachal Pradesh",
        "district": "Papum Pare",
        "lat": 27.1020,
        "lng": 93.6150,
        "contact": "+91-360-2244100",
        "heavy_equipment": ["Excavators x 4", "Hydraulic Cutters x 6", "Inflatable Boats x 8", "Satellite SATCOM x 2"],
        "capacity_persons": 600
    },
    {
        "id": "RES-02",
        "name": "Meghalaya SDMA Emergency Relief Hub",
        "type": "SDMA_RELIEF_HUB",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "lat": 25.5720,
        "lng": 91.8840,
        "contact": "+91-364-2502098",
        "heavy_equipment": ["Bulldozers x 2", "JCB Earthmovers x 5", "Mobile Field Hospital Tent x 2"],
        "capacity_persons": 1200
    },
    {
        "id": "RES-03",
        "name": "Sikkim State Disaster Response Center",
        "type": "SDRF_BASE",
        "state": "Sikkim",
        "district": "East Sikkim",
        "lat": 27.3290,
        "lng": 88.6120,
        "contact": "+91-3592-202461",
        "heavy_equipment": ["Rock Breakers x 3", "Rescue Canines x 4", "Drone LiDAR Surveillance Unit x 2"],
        "capacity_persons": 800
    },
    {
        "id": "RES-04",
        "name": "Kohima District Relief & Shelter Center",
        "type": "EVACUATION_SHELTER",
        "state": "Nagaland",
        "district": "Kohima",
        "lat": 25.6700,
        "lng": 94.1020,
        "contact": "+91-370-2290455",
        "heavy_equipment": ["Emergency Water Purification Unit x 3", "Solar Gensets x 6"],
        "capacity_persons": 1500
    },
    {
        "id": "RES-05",
        "name": "Silchar Medical College Emergency Trauma Center",
        "type": "HOSPITAL",
        "state": "Assam",
        "district": "Cachar",
        "lat": 24.8120,
        "lng": 92.7950,
        "contact": "+91-3842-240212",
        "heavy_equipment": ["Trauma Beds x 150", "Oxygen Cylinders x 400", "Helipad Active"],
        "capacity_persons": 350
    }
]

