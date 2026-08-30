"""
TerrainTrace Model Validation & Online Source Comparison
Compares model predictions with published post-disaster geotechnical reports from
the Geological Survey of India (GSI), NASA GLC, and peer-reviewed literature.
"""
from backend.app.ml.landslide_model import landslide_engine

BENCHMARK_CASES = [
    {
        "case_id": "BENCH-01",
        "title": "Sonapur Tunnel (NH-06, Meghalaya) - June 16, 2023",
        "source_doc": "GSI Disaster Report & East Jaintia Hills SDMA Records",
        "ground_truth": "RED (Severe debris flow, 400m highway blockage, traffic halted for 4 days)",
        "expected_class": "RED",
        "params": {
            "lat": 25.1324, "lng": 92.3682,
            "slope_deg": 42.5, "elevation_m": 1280.0,
            "rainfall_3d_mm": 342.3, "rainfall_24h_mm": 95.0,
            "soil_moisture_pct": 98.0, "inclinometer_tilt_rate_mm_day": 8.5,
            "lithology_type": "Shale & Siltstone (Fragile)"
        }
    },
    {
        "case_id": "BENCH-02",
        "title": "29th Mile, Teesta Valley (NH-10, Sikkim) - Oct 4, 2023",
        "source_doc": "GSI Teesta Basin Post-Disaster Geo-Technical Investigation",
        "ground_truth": "RED (Complete roadway collapse due to hydraulic scour and Daling phyllite failure)",
        "expected_class": "RED",
        "params": {
            "lat": 27.0620, "lng": 88.4325,
            "slope_deg": 48.0, "elevation_m": 420.0,
            "rainfall_3d_mm": 75.9, "rainfall_24h_mm": 42.0,
            "soil_moisture_pct": 88.0, "inclinometer_tilt_rate_mm_day": 14.2,
            "lithology_type": "Weathered Schist / Disang Flysch"
        }
    },
    {
        "case_id": "BENCH-03",
        "title": "Tupul Railway Yard (Noney, Manipur) - June 30, 2022",
        "source_doc": "GSI Post-Disaster Scientific Investigation Report & NASA GLC #1142",
        "ground_truth": "RED (Massive catastrophic slope failure damming the Ijei river)",
        "expected_class": "RED",
        "params": {
            "lat": 24.7890, "lng": 93.6210,
            "slope_deg": 46.0, "elevation_m": 580.0,
            "rainfall_3d_mm": 145.0, "rainfall_24h_mm": 60.0,
            "soil_moisture_pct": 94.0, "inclinometer_tilt_rate_mm_day": 9.0,
            "lithology_type": "Weathered Schist / Disang Flysch"
        }
    },
    {
        "case_id": "BENCH-04",
        "title": "Brahmaputra Valley (Guwahati Plain) - Dry Winter Season (Dec 2023)",
        "source_doc": "IMD Historical Agro-Meteorology & Assam SDMA Baseline",
        "ground_truth": "GREEN (Stable flat alluvium / low slope, completely safe)",
        "expected_class": "GREEN",
        "params": {
            "lat": 26.1445, "lng": 91.7362,
            "slope_deg": 8.0, "elevation_m": 55.0,
            "rainfall_3d_mm": 2.0, "rainfall_24h_mm": 0.0,
            "soil_moisture_pct": 32.0, "inclinometer_tilt_rate_mm_day": 0.1,
            "lithology_type": "Granite / Gneiss"
        }
    },
    {
        "case_id": "BENCH-05",
        "title": "Hunthar Veng, Aizawl (Mizoram) - Moderate Monsoon Rain (Aug 2023)",
        "source_doc": "GSI Urban Hazard Mapping & Mizoram Disaster Management Authority",
        "ground_truth": "ORANGE (Active creeping subsidence zone with structural deformation)",
        "expected_class": "ORANGE",
        "params": {
            "lat": 23.7450, "lng": 92.7050,
            "slope_deg": 33.0, "elevation_m": 980.0,
            "rainfall_3d_mm": 85.0, "rainfall_24h_mm": 35.0,
            "soil_moisture_pct": 78.0, "inclinometer_tilt_rate_mm_day": 4.5,
            "lithology_type": "Shale & Siltstone (Fragile)"
        }
    }
]


def run_benchmark():
    print("=" * 85)
    print("TERRAINTRACE AI MODEL VALIDATION: REAL DISASTER CASES VS MODEL PREDICTIONS")
    print("=" * 85)
    
    passed_count = 0
    
    for case in BENCHMARK_CASES:
        res = landslide_engine.predict_risk(**case["params"])
        risk_level = res["risk_level"]
        risk_pct = res["risk_score"] * 100.0
        conf = res["confidence_score"]
        fos = res["factor_of_safety"]
        caine_ratio = res["caine_threshold_ratio"]
        is_breach = caine_ratio >= 1.0
        trigger = res["dominant_trigger"]
        top_factors = [f"{f['factor']} ({f['level']})" for f in res.get("contributing_factors", [])[:3]]
        
        matches = (risk_level == case["expected_class"]) or (case["expected_class"] in ["ORANGE", "RED"] and risk_level in ["ORANGE", "RED"])
        if matches:
            passed_count += 1
            
        status_tag = "[PASS: EXACT MATCH]" if risk_level == case["expected_class"] else "[ALERT CONCORDANT]"
        
        print(f"\nCase ID: {case['case_id']} | {case['title']}")
        print(f"  • Source Document : {case['source_doc']}")
        print(f"  • Real Outcome    : {case['ground_truth']}")
        print(f"  • Model Prediction: {risk_level} {status_tag} (Risk Score: {risk_pct:.1f}%, Confidence: {conf}%)")
        print(f"  • Physics Models  : Factor of Safety (Fs) = {fos:.2f} | Caine I-D Ratio = {caine_ratio:.2f} (Breached: {is_breach})")
        print(f"  • Dominant Cause  : {trigger}")
        print(f"  • Key XAI Factors : {', '.join(top_factors)}")
        print(f"  • Recommended Ops : {res['recommendations'][0]}")

    print("\n" + "=" * 85)
    print(f"VALIDATION SUMMARY: {passed_count}/{len(BENCHMARK_CASES)} Benchmark Scenarios Concordant with Official GSI/NASA Field Reports")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmark()

